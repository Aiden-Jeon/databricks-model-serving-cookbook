# MLflow Model Logging

(MLflow 2.20+ / 3.x, as of May 2026)

## 1. PyFunc 로깅 기본

### `mlflow.pyfunc.log_model()` 시그니처 (MLflow 3.x)

```python
mlflow.pyfunc.log_model(
    name=None,                    # MLflow 3.x — artifact_path 대체
    python_model=None,            # PythonModel instance / callable / .py path
    artifacts=None,               # {"key": "uri/path"} — 모델과 함께 번들
    code_paths=None,              # list[str] — .py / dir / .whl
    infer_code_paths=False,       # MLflow 2.13+: import 자동 탐색
    conda_env=None,
    pip_requirements=None,        # 추론된 목록을 REPLACE
    extra_pip_requirements=None,  # 추론된 목록에 APPEND
    signature=None,
    input_example=None,           # 시그니처 추론 + dep 캡처 트리거
    registered_model_name=None,   # 로그 + 등록 한 번에
    model_config=None,            # context.model_config 로 노출
    resources=None,               # serving endpoint resources (UC fn, VS index 등)
    streamable=None,              # predict_stream 지원 여부
    metadata=None, tags=None,
)
```

### PythonModel — `load_context` + `predict`

- `load_context(context)`: `mlflow.pyfunc.load_model()` 시 **한 번** 실행. 무거운 artifact 로드용.
- `predict(context, model_input, params=None)`: 매 요청마다 실행. MLflow 2.20+ 부터 context 안 쓰면 생략 가능.

```python
import mlflow, pandas as pd
from mlflow.pyfunc import PythonModel
from mlflow.models import infer_signature

class SentimentModel(PythonModel):
    def load_context(self, context):
        import joblib
        self.vectorizer = joblib.load(context.artifacts["vectorizer"])
        self.classifier = joblib.load(context.artifacts["classifier"])

    def predict(self, context, model_input: pd.DataFrame, params=None):
        X = self.vectorizer.transform(model_input["text"])
        return pd.DataFrame({"label": self.classifier.predict(X)})

input_example = pd.DataFrame({"text": ["great", "terrible"]})
signature = infer_signature(input_example, pd.DataFrame({"label": ["pos","neg"]}))

with mlflow.start_run():
    info = mlflow.pyfunc.log_model(
        name="sentiment",
        python_model=SentimentModel(),
        artifacts={
            "vectorizer": "/Volumes/main/ml/artifacts/tfidf.joblib",
            "classifier": "/Volumes/main/ml/artifacts/logreg.joblib",
        },
        signature=signature,
        input_example=input_example,
        pip_requirements=["scikit-learn==1.4.2", "joblib==1.4.0"],
    )
```

### Flavor-specific vs PyFunc

- `mlflow.sklearn.log_model`, `mlflow.transformers.log_model` 등 flavor 로거는 native object를 직렬화. `python_function` flavor도 자동 등록되어 pyfunc로 load 가능.
- PyFunc는 (1) 멀티 모델 래핑 (2) flavor 없는 프레임워크 (3) pre/post processing 포함 시 사용.

## 2. Dependency 관리

### pip_requirements vs extra_pip_requirements vs conda_env

- 셋 중 **하나만** 사용 가능 (mutually exclusive).
- `pip_requirements`: 추론된 목록을 **완전히 대체**. lockdown 시 사용.
- `extra_pip_requirements`: 추론된 목록에 **추가**. 기본 권장.
- `conda_env`: dict 또는 YAML — Python 버전 + 시스템 라이브러리 제어 필요할 때.

```python
# 권장: 추론 + top-up
mlflow.pyfunc.log_model(
    name="model", python_model=MyModel(), input_example=ex,
    extra_pip_requirements=["transformers==4.41.0", "sentencepiece==0.2.0"],
)

# Locked-down 전체 교체
mlflow.pyfunc.log_model(
    name="model", python_model=MyModel(),
    pip_requirements=[
        "mlflow-skinny==2.20.0",
        "cloudpickle==3.0.0",
        "scikit-learn==1.4.2",
        "pandas==2.2.2",
    ],
)
```

### Private 인덱스, git URL, wheel

`pip_requirements`는 모든 pip 스펙을 받음:

```python
extra_pip_requirements=[
    "--index-url https://pypi.org/simple",
    "--extra-index-url https://__token__:${PAT}@gitlab.example.com/...",
    "internal-utils==0.3.1",
    "git+https://github.com/org/repo.git@v1.2.3",
    "/Volumes/main/ml/wheels/mypkg-0.1-py3-none-any.whl",
]
```

### 자동 추론

`input_example` 제공 시 MLflow가 로깅 중 모델 한 번 실행 → 사용된 모듈 검사 → `requirements.txt` 작성. 없으면 flavor 기본값으로 fallback.

```bash
MLFLOW_LOCK_MODEL_DEPENDENCIES=true  # transitive 까지 완전 lock
```

### Air-gapped 서빙용: 모든 deps 번들

```python
mlflow.models.utils.add_libraries_to_model("models:/main.ml.my_model/1")
# 모든 dep wheel을 모델 아티팩트로 포함시켜 새 버전 생성
```

## 3. Custom 코드 패키징

### `code_paths`

- 로컬 .py / 디렉토리 / .whl 리스트
- MLflow가 `<model>/code/` 로 복사 → load 시 `sys.path` 앞에 추가

```python
mlflow.pyfunc.log_model(
    name="model",
    python_model=MyModel(),
    code_paths=["preprocessing.py", "featurizers"],
)

class MyModel(PythonModel):
    def load_context(self, context):
        from preprocessing import clean         # code/ 가 sys.path에 있음
        from featurizers.text import tokenize
```

### code_paths 제약

- 지정 파일/디렉토리는 **모델 스크립트와 같은 디렉토리**에 있어야 함
- `src/utils.py` → `code/utils.py` 로 **평탄화** — 중첩 패키지의 relative import는 깨짐
- relative import 사용하려면 **패키지 디렉토리 전체**를 하나의 entry로 전달
- `infer_code_paths=True` (2.13+): cwd 기준 import 분석, parent dir은 못 잡음

→ 중첩 패키지나 C-extension은 **wheel 빌드 권장** (research 04 참고)

## 4. Unity Catalog 등록

```python
import mlflow
from mlflow import MlflowClient

mlflow.set_registry_uri("databricks-uc")   # 로컬 IDE/Connect 시 명시 필수

with mlflow.start_run() as run:
    info = mlflow.pyfunc.log_model(
        name="sentiment",
        python_model=SentimentModel(),
        artifacts={...},
        signature=signature, input_example=input_example,
        registered_model_name="main.ml_team.sentiment",  # 3-level UC
    )

# 또는 사후 등록
mv = mlflow.register_model(
    model_uri=f"runs:/{run.info.run_id}/sentiment",
    name="main.ml_team.sentiment",
)

# UC는 Stages 없음 — Aliases 사용
client = MlflowClient()
client.set_registered_model_alias("main.ml_team.sentiment", "Champion", mv.version)
client.set_registered_model_alias("main.ml_team.sentiment", "Challenger", mv.version - 1)

# Alias로 load
model = mlflow.pyfunc.load_model("models:/main.ml_team.sentiment@Champion")
```

UC에서는 Workspace Model Registry의 Staging/Production stage가 **없어졌고**, 대신 **mutable alias**(Champion/Challenger 등) + tag를 사용.

## 5. Anti-patterns

1. **버전 미고정** — `transformers` 만 쓰면 endpoint 빌드 시 latest로 resolve. 항상 `==` 핀.
2. **테스트 로드 생략** — 항상 검증:
   ```python
   loaded = mlflow.pyfunc.load_model(info.model_uri)
   loaded.predict(input_example)
   mlflow.models.predict(model_uri=info.model_uri, input_data=input_example, env_manager="uv")
   ```
3. **하드코딩 경로** — `/Workspace/...`, `/dbfs/...` 직접 참조 X. 항상 `context.artifacts["key"]` 경유.
4. **`predict` 안에서 artifact 로드** — load_context로 옮길 것 (요청마다 재로드 = 레이턴시 파괴).
5. **pip_requirements / extra_pip_requirements 동시 사용** — MLflow raise.
6. **input_example 누락** — dep 추론 약화 + signature 수동.
7. **중첩 패키지에 code_paths** — wheel 사용.
8. **UC workspace에서 legacy registry로 등록** — non-Databricks runtime에서 `set_registry_uri("databricks-uc")` 명시.

## 슬라이드와의 매핑

| 노트북 섹션 | 슬라이드 |
|---|---|
| MLflow란 / Components | 8, 10 |
| Model Registry & UC | 11, 13-15 |
| Mlflow Model 포맷 (MLmodel, flavors) | 39-42, 60 |
| Models from Code vs Legacy | 41 |
| Dependency 파일들 (python_env.yaml, requirements.txt, conda.yaml) | 60-63 |
| Load Context / Packages | 53 (목표) |

## 참고

- [mlflow.org/docs/latest/python_api/mlflow.pyfunc.html](https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html)
- [mlflow.org/docs/latest/ml/model/python_model/](https://mlflow.org/docs/latest/ml/model/python_model/)
- [mlflow.org/blog/custom-pyfunc/](https://mlflow.org/blog/custom-pyfunc/)
- [mlflow.org/docs/latest/ml/model/dependencies/](https://mlflow.org/docs/latest/ml/model/dependencies/)
- [mlflow.org/docs/latest/ml/model/signatures/](https://mlflow.org/docs/latest/ml/model/signatures/)
- [docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)
- [docs.databricks.com/aws/en/mlflow/log-model-dependencies.html](https://docs.databricks.com/aws/en/mlflow/log-model-dependencies.html)
- [docs.databricks.com/aws/en/machine-learning/model-serving/private-libraries-model-serving](https://docs.databricks.com/aws/en/machine-learning/model-serving/private-libraries-model-serving)
