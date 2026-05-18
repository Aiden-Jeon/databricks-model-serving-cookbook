# 04 · GPU PyTorch — Train · Log · Serve

> 작은 PyTorch MLP 를 **단일 GPU** 에서 학습 → MLflow PyFunc 로 logging → `workload_type=GPU_SMALL` (T4) Serving endpoint 로 배포까지 한 노트북에서 다룹니다. CPU sklearn 흐름(01·02·03)을 GPU torch 로 확장하는 미니 체험판입니다.

## 🧭 노트북 흐름

| 순서 | 파일 | 역할 | 사전 조건 |
|------|------|------|----------|
| 01 | [`01-train-and-serve.ipynb`](01-train-and-serve.ipynb) | torch MLP 학습(GPU) → PyFunc logging → UC alias → GPU endpoint 생성·호출 | 01 챕터 [`00-setup`](../01-mlflow-logging/00-setup.ipynb) (customer table 필요) |

`config.py` 는 다른 챕터와 동일한 내용을 복제해 사용합니다.

## 🔀 다른 챕터와의 비교

| 측면 | 01-mlflow-logging | 04-gpu-torch-serving |
|------|-------------------|----------------------|
| ML 프레임워크 | scikit-learn | PyTorch |
| 컴퓨트 | CPU | **GPU** (T4 권장) |
| Logging API | `mlflow.sklearn.log_model` / PyFunc | `mlflow.pyfunc.log_model` + `code_paths` 기반 클래스 외부화 |
| Endpoint workload_type | (default CPU) | **`GPU_SMALL`** |
| 표준화 | sklearn pipeline 가 처리 | PyFunc `load_context` 안에서 numpy 로 직접 처리 |

PyTorch 모델은 클래스 정의가 endpoint container 안에 있어야 pickle 이 복원되므로, **노트북 안에서 `/tmp/churn_torch_code/churn_model.py` 를 생성해 `code_paths` 와 같은 효과**를 냅니다. 02 챕터의 wheel 패턴(`02-code-packaging/02-uv-wheel`)이 production 권장입니다.

## 🖥️ 클러스터 세팅

| 항목 | 값 |
|------|---|
| Cluster mode | Single user |
| Databricks Runtime | **DBR 15.x ML 이상** (GPU CUDA 포함) |
| Driver type | `g4dn.xlarge` (1× T4) 또는 `g5.xlarge` (1× A10G) |
| Workers | 0 (single-node) |

GPU 가 보이지 않으면 노트북 첫 셀의 `torch.cuda.is_available()` assert 에서 멈춥니다.

## 📊 기대 결과

| 단계 | 산출물 |
|------|--------|
| 학습 (10 epoch, 5K row) | `val/acc` ≈ 0.80~0.90, 학습 시간 < 30초 |
| Logging | `main.model_serving_cookbook.churn_torch_gpu@champion` |
| Endpoint | `churn-torch-gpu-endpoint` (`workload_type=GPU_SMALL`, `scale_to_zero=True`) |
| 첫 호출 | cold start 30~60초, 이후 ms 단위 |

Endpoint provisioning 은 image build + GPU 노드 할당으로 **5~15분** 걸리는 게 정상입니다.

## ⚠️ 제약·비용

- **GPU endpoint 는 CPU 보다 시간당 비용이 큽니다**. `scale_to_zero_enabled=True` 가 idle 비용을 0 으로 만들지만, traffic 이 있는 동안은 CPU 의 수 배. 핸즈온 종료 후 반드시 [`../03-model-serving/99-cleanup.ipynb`](../03-model-serving/99-cleanup.ipynb) 실행 (`endpoint_torch_gpu` 도 포함됨).
- **모델은 작습니다**. GPU 필요성 자체는 약하지만 패턴 설명용입니다. 실제 LLM/CV 모델은 `GPU_MEDIUM`/`GPU_LARGE` 와 더 큰 image 가 필요할 수 있습니다.
- **클래스 정의 pickle 경로**: 노트북 셀에 직접 정의된 `nn.Module` 은 endpoint 에서 복원이 안 되므로 `/tmp/.../churn_model.py` 를 생성해 `code_paths` 처럼 첨부합니다. 운영에서는 02 챕터의 wheel 패턴을 권장합니다.

## ➡️ 다음

- 호출 방식 비교(REST / Spark UDF / AI Gateway)는 [`../03-model-serving/01-model-serving.ipynb`](../03-model-serving/01-model-serving.ipynb) 의 Step 6 이후가 그대로 적용됩니다 (CPU/GPU endpoint 인터페이스 동일).
- 핸즈온이 끝났다면 [`../03-model-serving/99-cleanup.ipynb`](../03-model-serving/99-cleanup.ipynb).
