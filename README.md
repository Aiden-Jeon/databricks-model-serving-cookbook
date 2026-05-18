# Databricks Model Serving Cookbook

Databricks 환경에서 **MLflow 모델 logging → custom 코드 packaging → Model Serving 배포**까지 end-to-end 패턴을 **단계 × 방식** 매트릭스로 정리한 쿡북입니다.

## 🎯 누구를 위한 쿡북인가

이런 분들을 가정하고 썼습니다.

- MLflow 로 모델을 logging 하고 Databricks Model Serving 으로 배포하려는 ML 엔지니어
- `code_paths` 의 평탄화·nested package 함정으로 한 번이라도 고생해 본 팀
- PoC 의 빠른 PyFunc → production 의 wheel 패키징 → Serverless Express 까지, 전환 경로를 한 곳에서 보고 싶은 팀

## 🧭 매트릭스

각 셀이 어떤 노트북에 매핑되는지 한눈에 보여 줍니다.

|                  | Flavor (sklearn) | PyFunc (`PythonModel`) | Custom code 번들 |
|------------------|------------------|------------------------|-------------------|
| **01-mlflow-logging** | [01 · Flavor logging + alias](01-mlflow-logging/01-flavor-logging.ipynb) | [02 · PyFunc + `load_context` + artifacts](01-mlflow-logging/02-pyfunc-custom.ipynb)<br>[03 · Dependencies (`pip_requirements` vs `extra_*` vs conda)](01-mlflow-logging/03-dependencies.ipynb) | — (코드 번들 없이) |
| **02-code-packaging** | — | — | [01 · `code_paths` 평탄화·한계](02-code-packaging/01-code-paths.ipynb)<br>[02 · `uv build` → wheel (production 권장)](02-code-packaging/02-uv-wheel.ipynb) |
| **03-model-serving** | Endpoint 호출 대상 | Endpoint 호출 대상 | [01 · Endpoint 4가지 호출, Blue/Green](03-model-serving/01-model-serving.ipynb)<br>[02 · Serverless Express 원클릭 배포](03-model-serving/02-express-deployment.ipynb) |
| **04-gpu-torch-serving** | — | [01 · GPU PyTorch — train · log · serve (`workload_type=GPU_SMALL`)](04-gpu-torch-serving/01-train-and-serve.ipynb) | (같은 노트북에서 `code_paths` 패턴 사용) |

`00-setup` (01 챕터) 은 모든 챕터가 공유하는 UC 리소스(catalog/schema/volume/customer table)와 MLflow registry 를 준비합니다. 한 번만 실행하면 다른 챕터의 사전 조건이 끝납니다. 챕터별 노트북 목록은 [`01-mlflow-logging/README.md`](01-mlflow-logging/README.md), [`02-code-packaging/README.md`](02-code-packaging/README.md), [`03-model-serving/README.md`](03-model-serving/README.md), [`04-gpu-torch-serving/README.md`](04-gpu-torch-serving/README.md) 에서 확인하세요.

### 행: 학습 단계

행마다 다루는 핵심은 다음과 같습니다.

| 행 | 차별점 |
|----|--------|
| 01-mlflow-logging | 모델을 MLflow 에 logging 하고 UC 에 등록하는 패턴. flavor / PyFunc / dependency 캡처 비교. |
| 02-code-packaging | Custom Python 코드(전처리·feature 함수 등)를 모델과 함께 묶는 두 방식 — `code_paths` 직접 첨부 vs `uv` wheel. |
| 03-model-serving | 등록 모델을 Serving endpoint 로 띄우고 호출. Classic Blue/Green vs Serverless Express. |
| 04-gpu-torch-serving | PyTorch MLP 를 GPU 에서 학습 → PyFunc logging → `workload_type=GPU_SMALL` (T4) endpoint 로 배포하는 GPU end-to-end 미니 체험판. |

### 열: 모델·코드 logging 방식

열별로 logging API 선택이 다음과 같이 갈립니다.

| 열 | 직렬화 | API |
|----|--------|-----|
| Flavor | sklearn / pytorch 등 네이티브 | `mlflow.<flavor>.log_model(model, name=..., signature=...)` |
| PyFunc | `PythonModel` 서브클래스 | `mlflow.pyfunc.log_model(name=..., python_model=..., artifacts=...)` |
| Custom code 번들 | flavor 또는 PyFunc 위에서 | `code_paths=[...]` 또는 `code_paths=["dist/*.whl"] + extra_pip_requirements=[...]` |

### 배포 토폴로지 (03 챕터 내부)

> **표기 규칙**: 모든 endpoint 는 scale-to-zero 활성, 동일 모델(`churn_wheel@champion`)을 띄웁니다.

| 노트북 | 컴퓨트 | 트래픽 분배 | 권장 시점 |
|--------|--------|------------|----------|
| 01-model-serving | Classic CPU pool | ✅ Blue/Green | 운영, multi-version A/B |
| 02-express-deployment | Serverless CPU | △ 단일 served entity | PoC, 빠른 검증 |

## 🧱 공통 스택

쿡북 전반에서 사용하는 기술 스택입니다.

- 모델: sklearn 분류기 (Random Forest / Gradient Boosting) on customer churn 데이터, 04 챕터는 PyTorch MLP
- 라이브러리: `mlflow>=2.20`, `databricks-sdk>=0.30`, `scikit-learn`, `uv`, `torch>=2.0` (04 챕터만)
- 데이터: synthetic customer churn (5K row, `sklearn.datasets.make_classification`)
- 등록소: Unity Catalog (`databricks-uc` registry URI)
- 모델 alias: `@champion` / `@challenger`
- Serving: Databricks Model Serving (Classic CPU + Serverless Express + Classic GPU `workload_type=GPU_SMALL`)

## 🗺️ 시작 가이드

다음 순서로 따라가는 것을 권장합니다.

1. 처음이라면 [`00-foundations/`](00-foundations/README.md) 부터 읽습니다. MLflow logging API, `code_paths` 의 평탄화, uv+wheel 패턴, Express Deployment, Databricks 환경 가정을 모두 다룹니다.
2. [`01-mlflow-logging/00-setup.ipynb`](01-mlflow-logging/00-setup.ipynb) 을 실행해 UC 리소스와 sample 데이터를 준비합니다 (전체 핸즈온 통틀어 한 번만).
3. 매트릭스에서 자신의 시나리오에 가장 가까운 셀(노트북)을 엽니다.
4. 해당 행 README 의 "노트북 흐름" 을 따라 순차 실행합니다.
5. 핸즈온 종료 후 [`03-model-serving/99-cleanup.ipynb`](03-model-serving/99-cleanup.ipynb) 으로 endpoint·모델을 정리합니다.

### 🧗 추천 학습 동선

처음 따라가는 경우 다음 순서로 학습 시간을 최소화하면서 점진적으로 확장할 수 있습니다.

| 단계 | 셀 | 목표 | 검증 포인트 |
|------|----|----|------------|
| 1 | `01-mlflow-logging/00-setup` | UC 리소스 + customer table 준비 | `main.model_serving_cookbook.customers` 에 5K row |
| 2 | `01-mlflow-logging/01-flavor-logging` | sklearn flavor logging + UC 등록 + alias | `models:/main.model_serving_cookbook.churn_basic@champion` 로 load 가능 |
| 3 | `01-mlflow-logging/02-pyfunc-custom` | PyFunc + `load_context` + `artifacts` 패턴 | `PythonModel` 서브클래스가 endpoint 호환 |
| 4 | `01-mlflow-logging/03-dependencies` | dep 캡처 3방식 비교 | 같은 모델·3 run, requirements.txt 차이 확인 |
| 5 | `02-code-packaging/01-code-paths` | `code_paths` 평탄화 동작 체득 | nested package 가 깨지는 케이스 직접 확인 |
| 6 | `02-code-packaging/02-uv-wheel` | wheel 패키징 production 패턴 | `churn_preproc==0.1.0` wheel 빌드 + 모델 안 번들링 |
| 7 | `03-model-serving/01-model-serving` | endpoint 생성 + 4가지 호출 + Blue/Green | endpoint 가 200 응답, REST·SDK·Spark UDF·UI 모두 동작 |
| 8 | `03-model-serving/02-express-deployment` | Serverless Express 비교 | Express endpoint 가 1~3 분 안에 ready |
| 9 | `04-gpu-torch-serving/01-train-and-serve` | torch GPU 학습 + GPU endpoint | `torch.cuda.is_available()=True`, `workload_type=GPU_SMALL` endpoint 가 ready |

단계를 넘어갈 때 얻는 학습 효과는 다음과 같이 누적됩니다.

- **01 → 02**: PyFunc 가 한계에 부딪치는 시점(custom 모듈 import) 을 `code_paths` 로 풀어 보고, 평탄화 제약을 직접 만난 뒤 wheel 패턴으로 넘어갑니다.
- **02 → 03**: wheel 로 packaging 된 모델이 endpoint 환경에서 그대로 install·import 되는 흐름을 확인합니다. Classic vs Express 의 trade-off 도 같은 모델로 비교합니다.
- **03 → 04**: 같은 logging·serving 패턴을 PyTorch + GPU 로 확장합니다. `workload_type=GPU_SMALL` 만 다를 뿐 endpoint 호출 인터페이스는 그대로입니다.

## 📚 참고

- [`docs/`](docs/README.md) — Model Serving 핸즈온 슬라이드, 외부 자료 인덱스.

## ⚠️ 본 쿡북의 스코프

다루는 범위와 다루지 않는 범위를 분명히 해 둡니다.

- **다룹니다**: MLflow flavor·PyFunc logging, `code_paths` / `pip_requirements` / `extra_pip_requirements` / wheel packaging, UC 모델 등록·alias, Classic Model Serving endpoint (CPU + GPU `GPU_SMALL`), Serverless Express Deployments, PyTorch 단일 GPU 학습.
- **다루지 않습니다**: LLM fine-tuning, Foundation Model APIs, multi-GPU / 분산 학습 (별도 [distributed training cookbook](https://github.com/Aiden-Jeon/databricks-distributed-training) 참고), Feature Store / Vector Search 와의 결합, Lakehouse Monitoring (model monitoring).
- **목표 학습 시간**: 각 노트북 5~10분. GPU endpoint provisioning 만 5~15분 추가.
