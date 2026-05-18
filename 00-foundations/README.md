# 00 · Foundations

챕터 노트북을 따라가기 전에 알아 두면 좋은 **MLflow logging · Model Serving · packaging 공통 개념**을 이 폴더에 모아 두었습니다. 챕터 README 가 짧게 유지될 수 있도록 반복되는 설명을 이쪽으로 끌어냈습니다.

## 📂 인덱스

파일명은 `<group>-<topic>.md` 형식이며, 그룹 의미는 다음과 같습니다.

| 그룹 | 의미 |
|------|------|
| `concepts-` | MLflow / Serving / packaging 핵심 개념과 API 사용법 |
| `env-` | Databricks 런타임·UC·권한 등 환경 가정 |

### concepts-

| 문서 | 내용 |
|------|------|
| [concepts-mlflow-logging.md](concepts-mlflow-logging.md) | `mlflow.pyfunc.log_model` 시그니처, `PythonModel`, `code_paths`, `pip_requirements` vs `extra_pip_requirements`, signature/input_example |
| [concepts-model-serving.md](concepts-model-serving.md) | Serving endpoint 생성/호출 4가지 방법, AI Gateway, Blue/Green |
| [concepts-uv-wheel.md](concepts-uv-wheel.md) | `uv build` 로 wheel 만들기 → `code_paths` + `extra_pip_requirements` production 권장 패턴 |
| [concepts-express-deploy.md](concepts-express-deploy.md) | Serverless CPU `EnvPackConfig` 원클릭 배포 (Express Deployments) |

### env-

| 문서 | 내용 |
|------|------|
| [env-databricks-environments.md](env-databricks-environments.md) | DBR ML 런타임, UC 권한, Serving endpoint 비용 가정 |

## 🧭 어디서부터 읽나

상황에 맞춰 다음 순서로 읽으면 됩니다.

- Databricks · UC 첫 셋업: `env-databricks-environments.md`
- 모델 logging 작성 전: `concepts-mlflow-logging.md`
- Custom 코드를 모델과 함께 묶어야 할 때: `concepts-mlflow-logging.md`(§code_paths) → `concepts-uv-wheel.md`
- Endpoint 띄우기 직전: `concepts-model-serving.md`
- Serverless로 한 번에 배포: `concepts-express-deploy.md`

## ➡️ 다음

읽기를 마쳤다면 [루트 매트릭스](../index.qmd)로 돌아가 챕터를 고릅니다.
