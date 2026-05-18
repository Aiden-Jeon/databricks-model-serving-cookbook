# Databricks Model Serving 배포

## 1. Endpoint 생성

### Prerequisites

| 항목 | 요구사항 |
|---|---|
| 모델 레지스트리 | **Unity Catalog** (`mlflow.set_registry_uri("databricks-uc")`) |
| UC 권한 | endpoint owner/SP에 `USE CATALOG` + `USE SCHEMA` + `EXECUTE` |
| 워크스페이스 | Model Serving 활성화 (Premium+), 지원 region |
| 인증 | PAT 또는 OAuth M2M (`CAN_QUERY` 권한) |
| Endpoint 이름 | 영숫자/하이픈/언더스코어, `databricks-` 접두사 불가 |

### Workload Size / Type

`workload_size`: Small (0-4 concurrency), Medium (8-16), Large (16-64)
`workload_type`: `CPU` (default), `GPU_SMALL` (T4), `GPU_LARGE` (A10G), `MULTIGPU_MEDIUM` (4×A10G), `GPU_MEDIUM_8` (8×A10G)

`scale_to_zero_enabled=True`: idle 시 $0, cold-start 추가 (CPU 수 초, GPU 수십 초). **SLA 있는 prod에선 비권장.**

### Python SDK — `WorkspaceClient.serving_endpoints.create()`

```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import (
    EndpointCoreConfigInput, ServedEntityInput, TrafficConfig, Route,
    AiGatewayConfig, AiGatewayInferenceTableConfig, AiGatewayRateLimit,
)

w = WorkspaceClient()

endpoint = w.serving_endpoints.create_and_wait(
    name="samsung-churn-endpoint",
    config=EndpointCoreConfigInput(
        served_entities=[
            ServedEntityInput(
                name="churn-v3",
                entity_name="main.ml_samsung.churn_model",
                entity_version="3",
                workload_size="Small",
                workload_type="CPU",
                scale_to_zero_enabled=False,
                environment_vars={
                    "AZURE_OPENAI_KEY": "{{secrets/samsung_scope/aoai_key}}",
                },
            )
        ],
        traffic_config=TrafficConfig(
            routes=[Route(served_model_name="churn-v3", traffic_percentage=100)]
        ),
    ),
    # 2026 권장: AI Gateway inference tables (legacy auto_capture_config 대체)
    ai_gateway=AiGatewayConfig(
        inference_table_config=AiGatewayInferenceTableConfig(
            enabled=True,
            catalog_name="main", schema_name="ml_samsung",
            table_name_prefix="churn_inference",
        ),
        rate_limits=[AiGatewayRateLimit(calls=120, key="endpoint", renewal_period="minute")],
    ),
    tags=[{"key": "owner", "value": "samsung"}, {"key": "env", "value": "prod"}],
)
```

`create_and_wait()`: READY 까지 폴링. fire-and-forget은 `create()`.

### REST API

```bash
curl -X POST "$DATABRICKS_HOST/api/2.0/serving-endpoints" \
  -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "samsung-churn-endpoint",
    "config": {
      "served_entities": [{
        "name": "churn-v3",
        "entity_name": "main.ml_samsung.churn_model",
        "entity_version": "3",
        "workload_size": "Small",
        "workload_type": "CPU",
        "scale_to_zero_enabled": false
      }]
    }
  }'
```

### UI

Sidebar → **Serving** → **Create serving endpoint** → 이름 → Entity (UC 모델 + 버전) → Compute (size/type/scale_to_zero) → (선택) Advanced env vars → (선택) AI Gateway → Create. CPU 기준 5-15분.

## 2. 엔드포인트 호출

URL: `https://<workspace>/serving-endpoints/<name>/invocations`

### 입력 포맷

| 포맷 | 용도 |
|---|---|
| `dataframe_split` | **권장** — 컬럼 순서 보장 (pandas) |
| `dataframe_records` | JSON-per-row, 순서 보장 X |
| `instances` | Tensor 모델, row-major |
| `inputs` | Tensor 모델, 컬럼 별 다른 shape |

### `mlflow.deployments` (노트북에서 권장)

```python
import mlflow.deployments
client = mlflow.deployments.get_deploy_client("databricks")
resp = client.predict(
    endpoint="samsung-churn-endpoint",
    inputs={"dataframe_split": {
        "columns": ["age", "tenure_months", "monthly_charges"],
        "data":    [[42, 18, 89.5], [29, 3, 45.0]],
    }},
)
print(resp["predictions"])
```

### REST / requests

```python
import os, requests
url = f"{os.environ['DATABRICKS_HOST']}/serving-endpoints/samsung-churn-endpoint/invocations"
headers = {"Authorization": f"Bearer {os.environ['DATABRICKS_TOKEN']}",
           "Content-Type": "application/json"}
payload = {"dataframe_records": [{"age": 42, "tenure_months": 18, "monthly_charges": 89.5}]}
r = requests.post(url, headers=headers, json=payload, timeout=30)
print(r.json()["predictions"])
```

### Databricks SDK query()

```python
from databricks.sdk.service.serving import DataframeSplitInput
resp = w.serving_endpoints.query(
    name="samsung-churn-endpoint",
    dataframe_split=DataframeSplitInput(
        columns=["age", "tenure_months", "monthly_charges"],
        data=[[42, 18, 89.5]],
    ),
)
```

### Batch 가이드

Model Serving은 low-latency real-time 최적화 (보통 < 1s 왕복, payload **16 MB cap**, request **120s timeout**).

- 소량 배치: 한 요청에 packing
- 대량 (수백만 row): **`mlflow.pyfunc.spark_udf`** 로 클러스터에서 병렬 점수화
- 스트리밍: `foreachBatch` 로 호출

```python
import mlflow
predict_udf = mlflow.pyfunc.spark_udf(
    spark, model_uri="models:/main.ml_samsung.churn_model/3", env_manager="virtualenv"
)
scored = features_df.withColumn("score", predict_udf(*feature_cols))
scored.write.mode("overwrite").saveAsTable("main.ml_samsung.churn_scores")
```

## 3. 환경변수 & 시크릿

`{{secrets/<scope>/<key>}}` 형식. 배포 시 resolve, plaintext 미저장.

```bash
databricks secrets create-scope samsung_scope
databricks secrets put-secret samsung_scope aoai_key
```

```python
ServedEntityInput(
    entity_name="main.ml_samsung.rag_model",
    entity_version="7",
    environment_vars={
        "AZURE_OPENAI_API_KEY": "{{secrets/samsung_scope/aoai_key}}",
        "AZURE_OPENAI_ENDPOINT": "https://samsung-aoai.openai.azure.com",
    },
)
```

UC 접근은 PAT 보다 **endpoint의 service principal + UC grant** 권장.

## 4. 로깅 / 모니터링 / Rate Limits

### AI Gateway Inference Tables (2026 권장)

기존 `auto_capture_config` 는 **2026-04-30 종료**. AI Gateway inference tables 사용:

- 스키마 (`<catalog>.<schema>.<prefix>_payload`):
  `databricks_request_id`, `client_request_id`, `date`, `timestamp_ms`, `status_code`, `execution_time_ms`, `request` (JSON), `response` (JSON), `request_metadata`
- ~1시간 내 로그 도착 → Lakehouse Monitoring 으로 drift 분석

### 메트릭

Serving UI → Metrics 탭: QPS, p50/p95/p99, 4xx/5xx, concurrency, CPU/GPU util.

```python
w.serving_endpoints.export_metrics(name="samsung-churn-endpoint")  # Prometheus
```

### Rate Limits

```python
ai_gateway=AiGatewayConfig(
    rate_limits=[
        AiGatewayRateLimit(calls=600, key="endpoint", renewal_period="minute"),
        AiGatewayRateLimit(calls=60,  key="user",     renewal_period="minute"),
    ],
)
```

기본 한도: workspace 당 200 QPS (지원팀 lift). 단일 entity ~3000 QPS (Large). Payload 16 MB, sync timeout 120s.

## 5. Blue/Green 업데이트

`update_config` 가 active config 교체. 새 config가 READY 될 때까지 old가 서빙.

```python
# Step 1 — v3와 v4를 함께 띄우고 v4에 10% canary
w.serving_endpoints.update_config_and_wait(
    name="samsung-churn-endpoint",
    served_entities=[
        ServedEntityInput(name="churn-v3", entity_name="main.ml_samsung.churn_model",
                          entity_version="3", workload_size="Small"),
        ServedEntityInput(name="churn-v4", entity_name="main.ml_samsung.churn_model",
                          entity_version="4", workload_size="Small"),
    ],
    traffic_config=TrafficConfig(routes=[
        Route(served_model_name="churn-v3", traffic_percentage=90),
        Route(served_model_name="churn-v4", traffic_percentage=10),
    ]),
)

# Step 2 — p95 / drift 확인 후 100% 컷오버
w.serving_endpoints.update_config_and_wait(
    name="samsung-churn-endpoint",
    traffic_config=TrafficConfig(routes=[
        Route(served_model_name="churn-v3", traffic_percentage=0),
        Route(served_model_name="churn-v4", traffic_percentage=100),
    ]),
)

# Step 3 — old entity 제거
```

## 슬라이드와 매핑

| 노트북 섹션 | 슬라이드 |
|---|---|
| Model Serving 개요 / 유형 (Custom/FMAPI/External) | 12 |
| Real-time REST API | 12, 27 |
| Feature Store + Serving 실시간 추론 | 66 |

## 참고

- https://docs.databricks.com/aws/en/machine-learning/model-serving/create-manage-serving-endpoints
- https://docs.databricks.com/aws/en/machine-learning/model-serving/score-custom-model-endpoints
- https://docs.databricks.com/aws/en/machine-learning/model-serving/store-env-variable-model-serving
- https://docs.databricks.com/aws/en/ai-gateway/inference-tables
- https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints
- https://databricks-sdk-py.readthedocs.io/en/latest/workspace/serving/serving_endpoints.html
- https://docs.databricks.com/aws/en/machine-learning/model-serving/model-serving-limits
