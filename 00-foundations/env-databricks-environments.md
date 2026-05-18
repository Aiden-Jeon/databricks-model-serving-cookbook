# Databricks 환경

쿡북 전반에서 가정하는 워크스페이스·런타임·권한·비용 조건을 한 곳에 모았습니다. 챕터 README와 노트북은 이 문서의 가정을 반복하지 않습니다.

## 워크스페이스

| 항목 | 가정 |
|------|------|
| 워크스페이스 등급 | Premium 이상 (Unity Catalog 활성화 필수) |
| Unity Catalog | 활성화. `main` 카탈로그가 기본값 (없으면 [`config.py`](../01-mlflow-logging/config.py) 에서 변경) |
| Model Serving | 활성화 (workspace admin 이 enable 한 상태) |
| Serverless | 03 챕터 02-express-deployment 에서 사용 |

## 런타임

| 노트북 | 권장 런타임 |
|--------|------------|
| 01-mlflow-logging/* | **DBR ML 15.x 이상** (MLflow 2.20+ 사전 설치) |
| 02-code-packaging/* | DBR ML 15.x 이상 |
| 03-model-serving/01-model-serving | DBR ML 15.x 이상 |
| 03-model-serving/02-express-deployment | **Serverless Notebook v3 / v4** + `mlflow>=3.1.0` |

CPU 노드로 충분합니다 (모델은 5K row sklearn). GPU 클러스터는 불필요합니다.

## 권한

`config.py` 의 `catalog="main"` 기준으로 본인 계정에 다음 권한이 필요합니다.

| 동작 | 필요 권한 |
|------|----------|
| Catalog 생성 (없을 시) | metastore admin 또는 `CREATE CATALOG` |
| Schema / Volume / Table 생성 | `USE CATALOG`, `CREATE SCHEMA`, `CREATE VOLUME`, `CREATE TABLE` |
| UC 모델 등록 | `USE SCHEMA`, `CREATE MODEL` (또는 `CREATE FUNCTION`) |
| Serving endpoint 생성 | `CAN_MANAGE` on endpoint, workspace 의 serving entitlement |

권한이 없으면 `config.py` 의 `catalog` 를 본인 권한 있는 카탈로그(예: 개인 sandbox)로 변경하세요.

## 비용

Serving endpoint 가 가장 비싸므로 주의가 필요합니다.

| 리소스 | 비용 가정 |
|--------|----------|
| Serving endpoint (CPU small) | idle 시 `scale_to_zero_enabled=True` 로 $0, traffic 시 시간당 과금 |
| Express Deployment | 동일하게 scale-to-zero. workload size `Small` 기준 |
| UC Volume | 저장 비용만 (wheel 수 MB 수준이라 무시 가능) |
| MLflow experiment / model | 무료 (UC 메타스토어 metadata 만) |

핸즈온 종료 후 반드시 [`03-model-serving/99-cleanup.ipynb`](../03-model-serving/99-cleanup.ipynb) 를 실행해 endpoint 와 등록 모델을 정리하세요.

## 자주 놓치는 지점

쿡북을 처음 돌릴 때 자주 마주치는 함정입니다.

- **Registry URI**: `mlflow.set_registry_uri("databricks-uc")` 를 안 하면 workspace registry(deprecated)에 등록됩니다. `00-setup` 노트북이 이를 강제합니다.
- **Alias vs Stage**: UC 모델은 더 이상 `Staging/Production` stage 가 없습니다. **alias** (`@champion`, `@challenger`)를 씁니다.
- **`code_paths` 평탄화**: `code_paths=["a/b/foo.py"]` 를 줘도 모델 안에는 `code/foo.py` 로만 들어갑니다. nested package 가 깨지는 원인 ([`concepts-mlflow-logging.md`](concepts-mlflow-logging.md) §code_paths).
- **Endpoint 이름은 workspace-unique**: 같은 워크스페이스에 다른 사용자가 같은 endpoint 이름을 만들면 충돌합니다. `config.py` 에서 prefix 를 본인 이름으로 바꿔도 됩니다.
- **Serverless Notebook v3/v4**: Express Deployments 노트북은 일반 클러스터에서는 동작하지 않습니다. Notebook 우측 상단의 compute 선택에서 **Serverless** 를 선택.
