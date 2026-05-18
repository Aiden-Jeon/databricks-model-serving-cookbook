# uv + Wheel 패키징

**결론:** 사용자 가설이 맞음. 중첩 패키지 / relative import / 재현성 필요할 때 `uv build` 로 wheel 만들어 `code_paths` + `extra_pip_requirements` 로 함께 올리는 패턴이 정석.

## 1. uv 로 wheel 빌드

```bash
uv init --lib churn_preproc   # --lib 면 src/ 레이아웃 + 패키지화
cd churn_preproc
```

생성된 구조:

```
churn_preproc/
├── .python-version
├── pyproject.toml
└── src/
    └── churn_preproc/
        ├── py.typed
        └── __init__.py
```

`pyproject.toml` (native `uv_build` 백엔드):

```toml
[project]
name = "churn-preproc"
version = "0.1.0"
description = "Churn preprocessing utilities"
requires-python = ">=3.11"
dependencies = [
    "numpy>=1.26",
    "pandas>=2.2",
]

[build-system]
requires = ["uv_build>=0.11.14,<0.12"]
build-backend = "uv_build"
```

빌드 + 스모크 테스트:

```bash
uv build                          # dist/churn_preproc-0.1.0-py3-none-any.whl + .tar.gz
uv pip install ./dist/churn_preproc-0.1.0-py3-none-any.whl
python -c "from churn_preproc import preprocess; print('ok')"
```

C-extension / dynamic version 필요하면 `hatchling` 백엔드 사용.

## 2. MLflow에 wheel 포함

**정석 패턴 (Databricks 공식 권장):**

```python
mlflow.pyfunc.log_model(
    name="model",
    python_model=ChurnModel(),
    code_paths=["dist/churn_preproc-0.1.0-py3-none-any.whl"],
    extra_pip_requirements=["code/churn_preproc-0.1.0-py3-none-any.whl"],
    input_example=example_df,
)
```

핵심: `code_paths` 가 wheel을 `<model>/code/` 로 복사 → `extra_pip_requirements` 에 **`code/` prefix** 가 붙은 상대경로로 참조. 서빙 시 unpacked 모델 루트 기준으로 pip가 해결.

### 흔한 함정 — 작동하지 않는 패턴

```python
# X — artifacts 는 pip resolver가 보지 않음
mlflow.pyfunc.log_model(
    name="model",
    artifacts={"wheel": "./mypkg.whl"},
    pip_requirements=["./artifacts/mypkg.whl"],
)
```

`artifacts` 는 `context.artifacts["wheel"]` 로 predict 안에서 접근하는 용도. pip resolver가 검사하지 않음.

### 대안: UC Volume 경로 직접 참조

```python
mlflow.pyfunc.log_model(
    name="model",
    python_model=ChurnModel(),
    extra_pip_requirements=[
        "/Volumes/main/ml/wheels/churn_preproc-0.1.0-py3-none-any.whl",
    ],
)
```

→ Endpoint의 service principal이 Volume에 READ 권한 필요.

### Air-gapped: 모든 deps 번들

```python
mlflow.models.utils.add_libraries_to_model("models:/main.ml.my_model/1")
```

현재 환경의 모든 transitive dep을 wheel로 캡처해서 새 버전으로 재로깅.

## 3. code_paths (raw) vs wheel 비교

| 측면 | `code_paths=["mypkg/"]` (raw source) | `code_paths=["dist/mypkg-x.y.z-...whl"]` (wheel) |
|---|---|---|
| 빌드 스텝 | 없음 | `uv build` 필요 |
| 중첩 패키지 | **깨짐** — MLflow 평탄화 (`code/utils.py`, NOT `code/src/utils.py`) | 정상 — pip 설치 |
| Relative import (`from .x import y`) | 빈번히 깨짐 (sys.path 해킹) | 정상 (proper site-packages) |
| Transitive deps | 미캡처 — 각 dep 직접 listing 필요 | pyproject.toml 에서 캡처 |
| 버전 관리 | 없음 | semver 가 wheel 파일명에 |
| 반복 속도 | 수정 → 재로그 | 수정 → `uv build` → 재로그 |
| Production | 비권장 | 권장 |

## 4. End-to-End 예제

**`src/churn_preproc/__init__.py`**

```python
import math
import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["amount_log"] = df["amount"].map(lambda x: math.log1p(x))
    return df.dropna()
```

**빌드:**

```bash
cd churn_preproc && uv build
# → dist/churn_preproc-0.1.0-py3-none-any.whl
```

**노트북 셀 — log_model:**

```python
import mlflow
import mlflow.pyfunc
from churn_preproc import preprocess  # 학습 시에도 사용

class ChurnModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        import joblib
        self.model = joblib.load(context.artifacts["sk_model"])

    def predict(self, context, model_input):
        from churn_preproc import preprocess  # 설치된 wheel에서 import
        cleaned = preprocess(model_input)
        return self.model.predict(cleaned)

WHEEL = "dist/churn_preproc-0.1.0-py3-none-any.whl"

with mlflow.start_run():
    mlflow.pyfunc.log_model(
        name="churn_model",
        python_model=ChurnModel(),
        artifacts={"sk_model": "models/sk_pipeline.joblib"},
        code_paths=[WHEEL],
        extra_pip_requirements=[f"code/{WHEEL.split('/')[-1]}"],
        input_example=example_df,
        registered_model_name="main.demo.preproc_model",
    )
```

서빙 시 cold-start에 `code/churn_preproc-0.1.0-py3-none-any.whl` 가 pip install → `from churn_preproc import preprocess` 정상.

## 5. 함정들

- **Python ABI 태그** — `py3-none-any` (pure Python) 면 어디서나 OK. C-extension 의존성이 있으면 `manylinux2014_x86_64` wheel 필요. `pip download --platform manylinux2014_x86_64 ...` 로 사전 검증.
- **Python 버전 drift** — `requires-python` 을 serving image runtime과 매칭 (DBR ML 15.x = 3.11). 3.12 빌드는 3.11에 설치 거부.
- **버전 미증가 시 캐싱** — wheel은 스냅샷. 매 반복마다 `0.1.0 → 0.1.1` 로 bump해야 pip cache 가 신선한 wheel 사용. `extra_pip_requirements` 는 name으로 dedup, content X.
- **Wheel resolution 위치** — Serving은 모델 내 `requirements.txt` 기반 env 빌드. `code/foo.whl` 은 unpacked 모델 루트 기준 — 모델 bundle 밖 경로 불가.
- **UC Volume 권한** — `/Volumes/.../foo.whl` 참조 시 endpoint SP에 Volume READ grant.
- **`add_libraries_to_model`** — PyPI 접근 어려운 air-gapped 고객에게 유용. 저장 비용 ↑, 재현성 ↑.
- **code_paths 디렉토리 + wheel 혼합 금지** — import shadowing 발생 (flatten source가 설치된 wheel을 가림).

## 참고

- [docs.databricks.com/aws/en/machine-learning/model-serving/private-libraries-model-serving](https://docs.databricks.com/aws/en/machine-learning/model-serving/private-libraries-model-serving)
- [docs.databricks.com/en/mlflow/log-model-dependencies.html](https://docs.databricks.com/en/mlflow/log-model-dependencies.html)
- [mlflow.org/docs/latest/ml/model/dependencies/](https://mlflow.org/docs/latest/ml/model/dependencies/)
- [docs.astral.sh/uv/guides/package/](https://docs.astral.sh/uv/guides/package/)
- [docs.astral.sh/uv/concepts/projects/init/](https://docs.astral.sh/uv/concepts/projects/init/)
- [docs.astral.sh/uv/concepts/build-backend/](https://docs.astral.sh/uv/concepts/build-backend/)
