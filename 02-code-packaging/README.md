# 02 · Custom Code Packaging

> 모델과 함께 배포할 **사용자 정의 Python 코드**를 어떻게 묶을지 두 가지 패턴으로 다룹니다. `code_paths` 의 한계와 **uv + wheel** 베스트프랙티스를 비교합니다.

## 🧭 노트북 흐름

번호 순서대로 실행하는 흐름입니다. `00-setup` 은 [`../01-mlflow-logging/00-setup.ipynb`](../01-mlflow-logging/00-setup.ipynb) 을 먼저 실행했다고 가정합니다 (UC 리소스 공유).

| 순서 | 파일 | 역할 | 사전 조건 |
|------|------|------|----------|
| 01 | [`01-code-paths.ipynb`](01-code-paths.ipynb) | `code_paths` 패턴, 평탄화 동작, nested package 제약, `infer_code_paths` | 01 챕터 00-setup |
| 02 | [`02-uv-wheel.ipynb`](02-uv-wheel.ipynb) | `uv build` → wheel → `code_paths` + `extra_pip_requirements` (production 권장) | 01, [`churn_preproc/`](churn_preproc/) |

`churn_preproc/` 은 02 노트북에서 wheel 빌드 대상으로 쓰는 샘플 패키지입니다. `pyproject.toml` + `src/churn_preproc/` (src-layout).

## 🔀 매트릭스

두 노트북이 같은 문제(전처리 코드를 모델에 번들링)를 어떻게 다르게 푸는지 비교합니다.

| 측면 | 01-code-paths | 02-uv-wheel |
|------|---------------|-------------|
| 코드 전달 수단 | `.py` 파일 / 디렉토리 | `.whl` wheel |
| MLflow 인자 | `code_paths=[...]` | `code_paths=["dist/*.whl"]` + `extra_pip_requirements=["code/*.whl"]` |
| 모델 안 위치 | `code/<flat>` (평탄화) | `code/<wheel>` |
| Import 방식 | `import <flat_module>` | `pip install` 후 `import <pkg>` |
| Nested package | ❌ 평탄화로 깨짐 | ✅ wheel 이 그대로 설치됨 |
| Production 권장 | △ 단일 파일이면 OK | ✅ 권장 |
| Dependency 자동 해결 | ❌ 본인이 직접 명시 | ✅ wheel 의 `pyproject.toml` 이 해결 |

자세한 동작 메커니즘은 [`concepts-mlflow-logging.md` §code_paths](../00-foundations/concepts-mlflow-logging.md) 와 [`concepts-uv-wheel.md`](../00-foundations/concepts-uv-wheel.md) 를 참고하세요.

## 🖥️ 클러스터 세팅

01 챕터와 동일. CPU 노드 + DBR 15.x ML 이상이면 충분합니다. 추가 요구사항은 없습니다.

`uv` 는 02 노트북이 `pip install uv` 로 설치합니다. wheel 빌드는 `/tmp/wheels/` 에서 일어나므로 cluster restart 시 사라집니다.

## 📊 기대 결과

각 노트북 종료 시 워크스페이스 상태입니다.

| 노트북 | 등록 모델 | 추가 산출물 |
|--------|----------|------------|
| 01-code-paths | `main.model_serving_cookbook.churn_codepaths` | `/tmp/work/preprocessing.py`, `/tmp/work/featurizers/` (예제용) |
| 02-uv-wheel | `main.model_serving_cookbook.churn_wheel@champion` | `/tmp/wheels/churn_preproc-0.1.0-py3-none-any.whl` |

학습 시간은 노트북당 1~2분.

## ⚠️ 제약

본 챕터에서 의도적으로 비워 둔 부분입니다.

- **Endpoint 배포 비교는 03 챕터에서**. 02 노트북에서 만든 wheel 모델을 endpoint 로 띄우는 흐름은 [`../03-model-serving/01-model-serving.ipynb`](../03-model-serving/01-model-serving.ipynb) 에서 다룹니다.
- **Private PyPI**: 본 챕터는 wheel 파일을 직접 번들링하는 패턴만 다룹니다. `extra_pip_requirements=["--index-url ..."]` 로 private index 를 쓰는 패턴은 [`concepts-mlflow-logging.md`](../00-foundations/concepts-mlflow-logging.md) 의 메모만 참고하세요.

## ➡️ 다음

만든 모델을 endpoint 로 띄우고 호출하는 패턴은 [`03-model-serving/`](../03-model-serving/README.md) 에서 이어집니다.
