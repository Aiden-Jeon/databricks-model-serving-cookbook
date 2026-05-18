# Databricks Model Serving Cookbook

Databricks 환경에서 MLflow 모델 logging · custom 코드 packaging · Model Serving 배포 패턴을 정리한 쿡북.

## 행동 가이드라인

속도보다 정확성을 우선한다. 사소한 작업에서는 계획·설명의 길이만 줄이되, 아래 원칙 자체는 유지한다.

### 1. 먼저 생각하기

가정하지 않는다. 혼란을 숨기지 않는다. 트레이드오프를 드러낸다.

- 관련 코드, 테스트, 설정을 먼저 읽고 기존 패턴을 파악한 뒤 변경한다.
- 작업 전 가정을 명시한다. 불확실하면 질문한다.
- 해석이 여러 가지 가능하면 제시하고 선택을 구한다. 임의로 고르지 않는다.
- 더 단순한 방법이 있으면 말한다. 필요하면 반론을 제기한다.
- 불명확한 점이 있으면 멈추고, 무엇이 불명확한지 명시하고, 질문한다.

### 2. 단순성 우선

문제를 해결하는 최소한의 코드만 작성한다. 추측성 확장은 하지 않는다.

- 요청된 범위 밖의 기능을 추가하지 않는다.
- 한 번만 쓰이는 코드에 과도한 추상화를 만들지 않는다.
- 요청되지 않은 "유연성"이나 "확장성"을 위한 구조를 만들지 않는다.
- 실제 호출 경로에서 관측 가능한 실패만 다룬다. 이론적으로만 가능한 시나리오에 방어 코드를 추가하지 않는다.
- 더 짧고 더 읽기 쉬운 방법이 있으면 단순화한다.

기준: "시니어 엔지니어가 보고 과도하다고 할 것인가?" 그렇다면 단순화한다.

### 3. 최소 변경

건드려야 할 것만 건드린다. 정리는 자기가 만든 혼란에 대해서만 한다.

- 요청을 만족시키기 위해 필요한 범위에서만 수정한다. 인접한 코드, 주석, 포매팅을 임의로 "개선"하지 않는다.
- 문제가 없는 코드를 리팩터링하지 않는다. 단, 변경의 정합성을 위해 필요하면(타입 수정, 테스트 갱신 등) 수반 변경은 한다.
- 기존 스타일에 맞춘다. 본인이 다르게 하고 싶어도.
- 관련 없는 문제를 발견하면 언급만 하고 수정하지 않는다.
- 본인의 변경으로 발생한 미사용 임포트, 변수, 함수는 정리한다.

기준: 변경된 모든 줄이 사용자의 요청으로 직접 추적 가능해야 한다.

### 4. 목표 중심 실행

성공 기준을 정의하고, 검증될 때까지 반복한다.

작업을 검증 가능한 목표로 변환한다:
- "유효성 검사 추가" → "잘못된 입력에 대한 테스트 작성 → 테스트 통과시키기"
- "버그 수정" → "재현 테스트 작성 → 수정 → 테스트 통과 확인"
- "리팩터링" → "기존 테스트 통과 확인 → 변경 → 테스트 재확인"

복수 단계 작업은 간략한 계획을 먼저 서술한다:
```
1. [단계] → 확인: [검증 방법]
2. [단계] → 확인: [검증 방법]
3. [단계] → 확인: [검증 방법]
```

명확한 성공 기준이 있으면 자율적으로 진행한다. 모호한 기준("알아서 해줘")이면 먼저 명확화한다.

검증이 불가능한 환경(테스트 미구축, 외부 의존성 등)에서는 가능한 가장 강한 검증을 수행하되, 미검증 범위와 잔여 리스크를 명시한다.

---

## 프로젝트 개요

Databricks 에서 **MLflow 모델 logging → custom 코드 packaging → Model Serving 배포** 전 과정을 **학습 단계 × logging 방식** 매트릭스로 정리한 쿡북.

- 학습 단계 (행): 01-mlflow-logging / 02-code-packaging / 03-model-serving / 04-gpu-torch-serving
- Logging 방식 (열): sklearn flavor / PyFunc (`PythonModel`) / custom code 번들 (`code_paths`, wheel)
- 배포 토폴로지는 03 챕터 내부 노트북에서 비교: Classic CPU + Blue/Green vs Serverless Express. 04 챕터는 Classic GPU (`workload_type=GPU_SMALL`).
- 데이터·모델 (01·02·03): synthetic customer churn 5K row, sklearn RandomForest/GradientBoosting. 04 챕터는 같은 데이터에 PyTorch MLP. UC 카탈로그·schema·volume·endpoint 이름은 [`config.py`](01-mlflow-logging/config.py) 한 곳에서 관리.

## 기술 스택

| 영역 | 사용 |
|------|------|
| 언어 | Python 3.10+ |
| ML 프레임워크 | scikit-learn (01·02·03), PyTorch 2.x (04 챕터) |
| 실험·등록 | MLflow 2.20+ (UC registry, alias). 03 챕터 Express 노트북은 mlflow 3.1+ |
| 실행 환경 | Databricks (DBR ML 15.x 이상; 04 챕터는 GPU 인스턴스 필요; Serverless Notebook v3/v4 for Express) |
| 데이터 | Synthetic customer churn (`sklearn.datasets.make_classification`, 5K row) |
| 패키징 | `uv` + `hatchling` (02-code-packaging/02-uv-wheel 의 wheel 빌드) |
| 노트북 포맷 | `.ipynb` (Jupyter) — Databricks Repos 에서 그대로 열림 |

**사용 안 함**: LLM fine-tuning · Foundation Model APIs · GPU serving · Feature Store / Vector Search 결합 · Lakehouse Monitoring.

## 디렉토리 구조

```
.
├── README.md                                   # 쿡북 메인, 매트릭스 + 네비게이션
├── _quarto.yml                                 # Quarto 사이트 설정
├── index.qmd                                   # Quarto home (README.md include)
├── theme.scss                                  # SCSS 테마
├── 00-foundations/                             # 그룹 prefix: concepts- / env-
│   ├── concepts-mlflow-logging.md
│   ├── concepts-model-serving.md
│   ├── concepts-uv-wheel.md
│   ├── concepts-express-deploy.md
│   └── env-databricks-environments.md
├── 01-mlflow-logging/                          # 행 1: logging 패턴
│   ├── config.py                               # %run ./config 으로 import
│   ├── 00-setup.ipynb                          # UC + customer table (전체 쿡북 공유)
│   ├── 01-flavor-logging.ipynb
│   ├── 02-pyfunc-custom.ipynb
│   └── 03-dependencies.ipynb
├── 02-code-packaging/                          # 행 2: custom 코드 번들링
│   ├── config.py
│   ├── churn_preproc/                        # 02 노트북이 빌드할 샘플 패키지
│   ├── 01-code-paths.ipynb
│   └── 02-uv-wheel.ipynb
├── 03-model-serving/                           # 행 3: endpoint 배포·호출
│   ├── config.py
│   ├── 01-model-serving.ipynb                  # Classic + Blue/Green
│   ├── 02-express-deployment.ipynb             # Serverless Express
│   └── 99-cleanup.ipynb                        # 핸즈온 마무리 (endpoint_torch_gpu 도 정리)
├── 04-gpu-torch-serving/                       # 행 4: GPU torch end-to-end
│   ├── config.py
│   └── 01-train-and-serve.ipynb                # GPU train → PyFunc log → GPU_SMALL endpoint
└── docs/                                       # 슬라이드, 외부 자료 인덱스
    └── slides/250530_Hadns-on_Sessionpptx.md
```

## 개발 명령어

이 레포는 **레퍼런스 코드 모음**이며, 노트북 실행은 모두 Databricks 워크스페이스에서 일어납니다. 로컬에서 동작하는 빌드는 Quarto site 렌더링뿐입니다.

| 동작 | 명령 |
|------|------|
| Quarto 사이트 로컬 렌더 | `quarto preview` |
| GitHub Pages 배포 | main 브랜치에 push → `.github/workflows/publish.yml` 실행 |
| wheel 빌드 (노트북 안에서) | `uv build` (02-code-packaging/02-uv-wheel 셀 안) |

## 코딩 컨벤션

- 한국어로 작성한다.
- 이모지는 섹션 헤더에만 쓴다. 본문에서는 쓰지 않는다.
- 비교/매핑이 등장하면 표(table)를 적극 사용한다.
- 각 챕터 디렉터리의 README 는 100~200줄을 목표로 한다. 너무 길어지면 분할한다.
- 노트북은 `.ipynb` 포맷. 매직(`%pip`, `%run`, `%sh`, `%sql`)은 첫 줄에 두고 cell 분리.
- "Generated by Claude" 같은 메타 코멘트는 작성하지 않는다.

## 테스트 규칙

- 이 쿡북에는 단위 테스트가 없다.
- 검증 기준은 **각 노트북이 명시된 Databricks 클러스터 사양에서 끝까지 실행됨**이다.
- 변경 시 최소한 영향을 받는 챕터 README 의 "노트북 흐름" 을 따라가 재현 가능성을 확인한다.

## Git 규칙

- 커밋은 챕터 단위 또는 노트북 단위로 작게 끊는다 (e.g. `feat(02-code-packaging): uv-wheel 노트북 추가`).
- 메인 브랜치는 `main`. 큰 변경은 별도 브랜치 + PR.

## 운영 제약

- **LLM fine-tuning / Foundation Model APIs / multi-GPU 분산 학습은 추가하지 않는다** (별도 [distributed training cookbook](https://github.com/Aiden-Jeon/databricks-distributed-training) 으로 분리). 단일 GPU 학습·서빙은 04 챕터에서 다룬다.
- 데이터는 단일(`make_classification` customer churn)을 유지한다. 다른 데이터셋을 도입하지 않는다. 모델은 sklearn (01·02·03) 과 PyTorch MLP (04) 두 가지만 허용.
- 등록소는 UC 한 가지(`databricks-uc`)만 다룬다. workspace registry(deprecated)는 다루지 않는다.
- Stage(`Staging/Production`) 개념은 사용하지 않는다. UC 모델의 **alias** 만 사용한다.
- 02-code-packaging 의 `churn_preproc` 은 src-layout (`src/churn_preproc/`) 을 유지한다. 02-uv-wheel 노트북이 이 레이아웃을 가정한다.
- 비용이 비싼 endpoint 는 모두 `scale_to_zero_enabled=True` 로 만든다. 핸즈온 종료 후 `99-cleanup` 으로 정리한다.
