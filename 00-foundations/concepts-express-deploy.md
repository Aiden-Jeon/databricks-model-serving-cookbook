# Express Deployment

## 정답: Express Deployments (이전명 Serverless Optimized Deployments)

사용자가 말한 "데이터브릭스 CPU serverless 에서 실행하면 바로 서빙하는 기능" = **Express Deployments**.

## 동작 방식

Serverless Notebook 에서 모델을 등록하면, Databricks가 **등록 시점**에 모델 아티팩트 + serverless 노트북 환경을 함께 staging. Serving endpoint 는 이 pre-staged 환경을 재사용 → **container build 단계 스킵**.

- Event log 에서 "Container build" phase 사라짐
- Endpoint READY 시간: ~10분 → **1-2분**

## Prerequisites

- Custom model (FMAPI 아님)
- **Serverless Notebook v3 또는 v4** 에서 logging + registration
- `mlflow >= 3.1`
- Unity Catalog 등록
- **CPU serving** (GPU 미지원)
- Environment size ≤ 1 GB

## 코드 (register-and-ready macro)

```python
import mlflow
from mlflow.utils.env_pack import EnvPackConfig

mlflow.set_registry_uri("databricks-uc")

with mlflow.start_run():
    model_info = mlflow.sklearn.log_model(model, name="model")

# 핵심: env_pack 이 serverless env 를 serving 용으로 staging
mlflow.register_model(
    model_info.model_uri,
    name="main.ml.my_model",
    env_pack=EnvPackConfig(name="databricks_model_serving"),
)
```

이후 UC 모델 UI 에서 **"Use model for inference → Serving endpoint"** 클릭 → ~1분 안에 CPU 엔드포인트 query 가능.

## CPU workload_type + scale_to_zero 비용/성능

`workload_type` CPU 옵션:
- `CPU` (default)
- `CPU_MEDIUM` / `CPU_LARGE` (Beta — 더 많은 메모리, 같은 하드웨어에서 낮은 concurrency)

`workload_size`: Small (~4 qps), Medium, Large

```python
from mlflow.deployments import get_deploy_client
client = get_deploy_client("databricks")
client.create_endpoint(
    name="my-endpoint",
    config={"served_entities": [{
        "entity_name": "main.ml.my_model",
        "entity_version": "1",
        "workload_type": "CPU",
        "workload_size": "Small",
        "scale_to_zero_enabled": True,
    }]},
)
```

### scale_to_zero 비용 프로파일

- Idle 시: **0 replica → $0 DBU**
- Idle 후 첫 요청: cold start (보통 30-60s CPU custom; Express는 더 짧음)
- Warm 시: active replica-hour 당 CPU Model Serving DBU rate 청구
- Databricks **production SLA에는 비권장** (scaled-to-zero 일 때 capacity 보장 X)

### vs Provisioned Throughput

Provisioned (FMAPI / high-throughput LLM 용)는 minimum concurrency commit 필요 → 진정한 0 X. CPU custom + scale-to-zero 가 **"always-available but pay-only-on-use"** 가장 저렴한 옵션.

## "Register and deploy" 매크로

2026-05 기준 **단일 SDK 호출은 없음**. 가장 근접한 매크로:

1. Serverless Notebook 에서 `mlflow.<flavor>.log_model(...)`
2. `mlflow.register_model(..., env_pack=EnvPackConfig(name="databricks_model_serving"))`
3. **UI 원클릭**: UC 모델 페이지 → "Serve this model" (CPU + scale-to-zero default)

MLflow 3 **Deployment Jobs** (UC governed) 로 2→3 자동화 가능 — 진정한 one-shot 파이프라인에 가장 가까움.

## 노트북 데모 추천 (피치)

> "Serverless 노트북에서 학습 → `env_pack` 으로 등록 → UC에서 한 번 클릭 → 1분 안에 CPU 엔드포인트, 유휴 시 $0."

## 참고

- [docs.databricks.com/aws/en/machine-learning/model-serving/express-deployments](https://docs.databricks.com/aws/en/machine-learning/model-serving/express-deployments)
- [docs.databricks.com/aws/en/machine-learning/model-serving/serverless-optimized-deployments](https://docs.databricks.com/aws/en/machine-learning/model-serving/serverless-optimized-deployments)
- [docs.databricks.com/aws/en/machine-learning/model-serving/create-manage-serving-endpoints](https://docs.databricks.com/aws/en/machine-learning/model-serving/create-manage-serving-endpoints)
- [docs.databricks.com/aws/en/mlflow/models](https://docs.databricks.com/aws/en/mlflow/models)
- [www.databricks.com/product/pricing/model-serving](https://www.databricks.com/product/pricing/model-serving)
