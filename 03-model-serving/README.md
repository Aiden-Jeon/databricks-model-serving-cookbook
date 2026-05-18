# 03 · Model Serving

> 등록된 UC 모델을 **Serving endpoint** 로 띄우고, 호출·Blue/Green 롤아웃·Serverless Express 배포를 다룹니다. 핸즈온 종료 후에는 반드시 `99-cleanup` 으로 endpoint 를 정리합니다.

## 🧭 노트북 흐름

번호 순서대로 실행하는 흐름입니다.

| 순서 | 파일 | 역할 | 사전 조건 |
|------|------|------|----------|
| 01 | [`01-model-serving.ipynb`](01-model-serving.ipynb) | Endpoint 생성, 호출 4방법, AI Gateway, Blue/Green 트래픽 | 02 챕터 02-uv-wheel 까지 (등록 모델 `churn_wheel@champion`) |
| 02 | [`02-express-deployment.ipynb`](02-express-deployment.ipynb) | Serverless CPU `EnvPackConfig` 원클릭 배포. Notebook v3/v4 + `mlflow>=3.1.0` 필요. | 01 챕터 00-setup |
| 99 | [`99-cleanup.ipynb`](99-cleanup.ipynb) | 생성된 endpoint, 등록 모델, UC table 정리 (선택) | — |

## 🔀 매트릭스

두 deploy 방식의 차이를 한눈에 보여 줍니다.

| 측면 | 01-model-serving (Classic) | 02-express-deployment (Express) |
|------|---------------------------|-----------------------------------|
| Provisioning API | `databricks.sdk.WorkspaceClient().serving_endpoints.create` | `mlflow.deployments.get_deploy_client("databricks").create_endpoint` + `EnvPackConfig` |
| 컴퓨트 | Classic CPU pool | Serverless CPU |
| Scale-to-zero | `scale_to_zero_enabled=True` | 기본 활성 |
| 배포 시간 | 5~10 분 | 1~3 분 (이미지 캐시 시) |
| Blue/Green 트래픽 분배 | ✅ `traffic_config` | 기본 단일 served entity (수동 split 필요) |
| AI Gateway (rate limit / log) | ✅ | △ (메뉴는 동일하지만 일부 옵션 제한) |
| 권장 시점 | 운영, 트래픽 분배 필요 | PoC, 빠른 검증, 단일 모델 |

## 🖥️ 클러스터 세팅

| 노트북 | 컴퓨트 |
|--------|--------|
| 01-model-serving | DBR ML 15.x 이상 (CPU). Endpoint 자체는 Databricks 가 호스팅 |
| 02-express-deployment | **Serverless Notebook v3 / v4** + `mlflow>=3.1.0` |
| 99-cleanup | 아무 클러스터 |

02 노트북은 일반 클러스터에서는 동작하지 않습니다. Notebook 우측 상단 compute 에서 **Serverless** 를 선택하세요.

## 📊 기대 결과

각 노트북 종료 시 워크스페이스 상태입니다.

| 노트북 | 생성 endpoint | 호출 검증 |
|--------|---------------|----------|
| 01-model-serving | `churn-wheel-endpoint` (`scale_to_zero=True`) | REST / SDK / requests / curl 4종 호출 모두 동일 응답 |
| 02-express-deployment | `churn-express-endpoint` | REST 호출 ms 단위 응답 |
| 99-cleanup | 위 두 endpoint 삭제 | UC 모델·table 도 선택적으로 삭제 |

Endpoint 가 처음 cold start 할 때 1~2분 걸리는 게 정상입니다.

## ⚠️ 제약·비용

본 챕터에서 운영비가 발생할 수 있는 부분입니다.

- **Endpoint 가 가장 비쌉니다**. `scale_to_zero_enabled=True` 라도 traffic 이 있는 동안 시간당 과금. 핸즈온 종료 후 반드시 [`99-cleanup`](99-cleanup.ipynb) 실행.
- **Workspace-unique 이름**: `config.py` 의 `endpoint_wheel`, `endpoint_express` 가 다른 사용자와 충돌하면 endpoint 생성이 실패합니다. prefix 를 본인 이름으로 변경하세요.
- **Express Deployment 는 single served entity**: 01 의 Blue/Green 패턴이 그대로 적용되지 않습니다. 트래픽 분배가 필요하면 Classic 으로 가세요.
- **AI Gateway 의 일부 옵션**(예: PII masking)은 enterprise tier 에서만 활성화됩니다.

## ➡️ 다음

핸즈온이 끝났다면 [`99-cleanup`](99-cleanup.ipynb) 을 실행한 뒤 [루트 매트릭스](../index.qmd)로 돌아갑니다.
