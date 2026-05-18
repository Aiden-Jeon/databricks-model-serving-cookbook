# 01 · MLflow Model Logging

> MLflow 모델을 **flavor / PyFunc** 두 방식으로 logging 하고, dependency 를 캡처하는 패턴을 학습합니다. Model Serving 으로 가기 전의 기초 챕터입니다.

## 🧭 노트북 흐름

번호 순서대로 실행하는 흐름입니다. `00-setup` 은 쿡북 전체에서 한 번만 실행하면 됩니다 (다른 챕터도 같은 UC 리소스를 공유).

| 순서 | 파일 | 역할 | 사전 조건 |
|------|------|------|----------|
| 00 | [`00-setup.ipynb`](00-setup.ipynb) | UC catalog/schema/volume + synthetic customer churn 데이터 생성 + MLflow registry 설정 | — |
| 01 | [`01-flavor-logging.ipynb`](01-flavor-logging.ipynb) | sklearn flavor `log_model`, signature 추론, UC 등록, alias (`@champion`) | 00 |
| 02 | [`02-pyfunc-custom.ipynb`](02-pyfunc-custom.ipynb) | `PythonModel` 서브클래스, `load_context`, `artifacts`, 멀티모델 wrapper | 00 |
| 03 | [`03-dependencies.ipynb`](03-dependencies.ipynb) | `pip_requirements` vs `extra_pip_requirements` vs `conda_env`, lock 전략 | 00 |

`config.py` 는 catalog / schema / 모델·endpoint 이름을 모두 정의합니다. 모든 노트북이 `%run ./config` 으로 import 합니다.

## 🔀 매트릭스

각 노트북이 logging 의 어떤 축을 다루는지 한 줄로 보여 줍니다.

| 노트북 | 직렬화 | UC 등록 | Dependency 캡처 |
|--------|--------|---------|----------------|
| 01-flavor-logging | sklearn flavor (`mlflow.sklearn.log_model`) | `registered_model_name=...` | 자동 추론 (signature + input_example) |
| 02-pyfunc-custom | PyFunc (`mlflow.pyfunc.log_model` + `PythonModel`) | 동일 | `artifacts` 로 추가 파일 번들 |
| 03-dependencies | 두 방식 모두 | — | `pip_requirements` REPLACE / `extra_pip_requirements` APPEND / `conda_env` |

## 🖥️ 클러스터 세팅

CPU 노드로 충분합니다. 노트북은 5K row sklearn 모델만 학습합니다.

| 항목 | 값 |
|------|---|
| Cluster mode | Single user |
| Databricks Runtime | **DBR 15.x ML 이상** (CPU) |
| Driver type | `i3.xlarge` 등 일반 CPU |
| Workers | 0 (single-node) 또는 소수 — Spark 사용 거의 없음 |

`00-setup` 첫 셀이 `%pip install -q "mlflow>=2.20.0" "databricks-sdk>=0.30.0"` 으로 의존성을 명시합니다.

## 📊 기대 결과

각 노트북 종료 시 워크스페이스 상태입니다.

| 노트북 | 등록 모델 | Experiment runs |
|--------|----------|----------------|
| 00-setup | — | `/Users/<you>/model_serving_cookbook` experiment 생성 |
| 01-flavor-logging | `main.model_serving_cookbook.churn_basic@champion` | 1 run |
| 02-pyfunc-custom | `main.model_serving_cookbook.churn_pyfunc@champion` | 1 run |
| 03-dependencies | `main.model_serving_cookbook.churn_deps` (alias 미부여) | 3 runs (방식 비교) |

학습 시간은 노트북당 1~2분 (sklearn `RandomForest`/`GradientBoosting` on 5K row).

## ⚠️ 제약

본 챕터에서 의도적으로 비워 둔 부분입니다.

- **Endpoint 배포는 03 챕터에서**. 본 챕터는 logging 까지만 다룹니다.
- **wheel 빌드는 02 챕터에서**. `code_paths` 의 평탄화 문제는 [`concepts-mlflow-logging.md` §code_paths](../00-foundations/concepts-mlflow-logging.md) 에서 개념만 다루고, 실습은 [`02-code-packaging/`](../02-code-packaging/README.md) 으로 넘어갑니다.

## ➡️ 다음

Custom Python 코드를 모델과 함께 묶는 패턴은 [`02-code-packaging/`](../02-code-packaging/README.md) 에서 이어집니다.
