# DatabricksHands-on Session

> **Slides:** 124 | **Source:** https://docs.google.com/presentation/d/12gvoApL_qdhgEKMy19n9pz1x4xrLr5uW/edit | **Images:** 136
>
> **Images are saved alongside this file in `./images/`.** These contain architecture diagrams, flowcharts, and screenshots that are essential context. To analyze a visual, read the image file directly (e.g., `Read ./images/slide07_img01.png`).

---

## Slide 2: Databricks Data Intelligence Platform

소개
< Databricks 논리 아키텍처 >

Databricks Data Intelligence Platform이란?
대규모 엔터프라이즈급 데이터의 수집, 저장, 처리, 공유, 분석을 통합하는 데이터 플랫폼
사용자의 퍼블릭 클라우드 환경에 배포되어 사용자 계정의 저장소 및 보안과 통합
Amazon Web Services, Microsoft Azure, Google Cloud Platform에 배포 지원

데이터 거버넌스Unity Catalog

데이터 과학 & 생성형 AIMosaic AI
ELT & 실시간 분석DLT
오케스트레이션Workflow
데이터 웨어하우징Databricks SQL
Databricks와 Open Technologies
Databricks는 오픈소스 및 개방형 표준을 지향
Databricks주도로 설립된 오픈소스 : Apache Spark, Delta Lake, MLflow, Redash
Databricks는 개방형 기술을 보다 최적화하여 성능향상과 사용편의성 증대를 위한 Workflows, Unity Catalog, Delta Live Tables, Photon 등의 독점적 기능을 제공
머신러닝 모델 운영관리

데이터 처리 엔진

스토리지 프레임워크

Databricks의 주요 용도
엔터프라이즈 데이터 레이크 하우스 구축, ETL 및 데이터 엔지니어링, 데이터 웨어하우스 구축
인공지능 분석, 비즈니스 인텔리전스 분석, 실시간 스트리밍 분석
클라우드 스토리지 (S3, ADLS2, GCS)

---

## Slide 3: Databricks Data Intelligence Platform

사용 주체 별 용도

데이터 엔지니어
데이터의 수집, 저장, 처리 작업을 수행하기위해 데이터 파이프인을 구축하고 데이터의 보안과 활용에 대한 규정을 관리하는 역할
데이터 분석가
정제된 데이터를 활용하여 OLAP 분석 모델을 생성하고 BI도구, 시각화도구, SQL을 통해 데이터의 차원을 회전하며 데이터를 분석하는 역할
데이터 사이언티스트
정제된 데이터를 활용하여 특징변수를 관리하고 추론통계, 머신러닝, 딥러닝 모형을 작성하여 데이터를 분석하는 역할
적용 업무
RDBMS 또는 DW의 데이터를 Databricks로 적재하여 레이크하우스 시스템 구축
비정형 파일을 Databricks 저장소로 적재하여 머신러닝/딥러닝 분석 시스템 구축
배치 업무와 스트리밍 업무를 Databricks 플랫폼으로 통합하여 플랫폼 단일화
ETL / CDC / ML 워크로드를 단일 작업으로 연속성 있게 구성하여 워크플로우 통합
적용 업무
RDBMS, DW, File, NoSQL등의 소스 데이터가 통합된 레이크하우스 시스템에서 SQL을 통한 다차원 분석 시스템 구축
Tableau, Power BI, Microstrategy등 외부 BI 솔루션을 연계한 분석 시스템 구축
자체 대시보드 기능을 통해 업무별 대시보드를 생성하고 공유하는 환경 구성
DW 시스템의 경험과 동일한 SQL개발 환경
적용 업무
과거 데이터로부터 미래의 상황을 예측하는 머신러닝 예측 분석 시스템 구축
비정형 데이터로부터 상황을 인식하고, 분류하는 딥러닝 예측 분석 시스템 구축
GPU를 활용하여 텍스트로부터 텍스트 또는 이미지를 생성하는 생성형 AI 시스템 구축
시티즌 데이터사이언티스트를 위한 AutoML 기반의 대중화된 머신러닝 분석플랫폼 구축

---

## Slide 4: Databricks Machine Learning

개요
Databricks Mosaic AI
Databricks Mosaic AI는 Databricks AI/ML과 MosaicML을 통합한 개념
ML(Machine Learning), DL(Deep Learning), GenAI(Generative AI) 모든 워크로드를 단일 플랫폼에서 개발
Databricks Mosaic AI 기능은 ML워크로드를 개발하고 ML워크플로우를 구축하기위한 다양한 기능을 제공
Data
- Unity Catalog
Model training
- AutoML
- Notebooks
- MLflow experiments
Model management
- Unity Catalog
- Workspace Model Registry
Feature Store
- Feature serving
Lakehouse Monitoring
- Data quality metrics
- Model quality metrics
- Drift
Production
- Model serving
- Batch inference
모델 개발을 위한 Databricks Mosaic AI의 특장점
데이터세트, 피처, 모델에 대한 Unity Catalog 거버넌스 지원
Lakehouse Monitoring을 통한 데이터 모니터링 지원
피처 엔지니어링 지원
모델 생명주기 관리
모델 서빙 지원
워크플로우 생성 지원
Git 통합 지원

---

## Slide 5: Databricks ML Runtime

Machine Learning 개발을 위한 Databricks Runtime ML
Databricks는 All-Purpose Cluster에서 Standard Runtime과 ML Runtime을 지원
Runtime ML은 ML/DL/GenAI 개발을 위한 전용 런타임으로 다양한 ML/DL/GenAI 라이브러리를 지원
Runtime ML은 CPU / GPU 런타임을 지원
Runtime ML은 ML워크로드의 특성으로 인해 공유 클러스터 모드를 지원하지 않음

Databricks Runtime ML과 Photon
Runtime ML에서 Photon을 사용하기 위해서는 15.2ML 이상의 런타임이 필요하며 워크로드에 따라 활성화를 고려
Photon은 Spark SQL, Spark DataFrames, feature engineering, GraphFrames, xgboost4j 에서만 성능향상 효과를 볼 수 있음
Photon이 지원하지 않는 Spark RDD, Pandas UDF에서는 성능 효과를 볼 수 없음
XGBoost, PyTorch, TensorFlow 등의 non-JVM기반의 네이티브 Python 언어에서는 효과를 볼 수 없음

---

## Slide 6: Databricks ML Runtime

딥러닝과 생성형 AI 지원
Deep Learning 개발을 위한 Databricks ML Runtime
Tensorflow, Keras, PyTorch 딥러닝 라이브러리 지원
딥러닝 라이브러리의 MLflow 통합 지원
Petastorm, Hyperopt, Horovod, Ray 분산처리 라이브러리 지원
GPU라이브러리가 사전 구성된 GPU 런타임 제공
딥러닝 모델 서빙을 위한 GPU 엔드포인트 지원(지정 리전)

LLM등 GenAI 개발을 위한 Databricks ML Runtime
GenAI 모델 개발을위해 Hugging Face Transformers, LangChain 라이브러리 지원
Transformers 파이프라인, 모델, 프로세싱 컴포넌트를 위한 MLflow 통합 지원
Hugging Face, DeepSpeed 오픈소스 도구를 사용하여 사용자 데이터세트로 훈련 가능
Databricks가 관리형으로 제공하는 파운데이션 모델 API를 제공(DBRX, Llama3, BGE 등)
타사 서비스에서 제공하는 외부 모델을 등록 가능(OpenAI, Bedrock, Anthropic 등)

---

## Slide 8: Databricks MLflow

딥러닝과 생성형 AI 지원
MLflow란?
ML 모델을 개발의 생명주기에서 모델, 피처, 평가지표를 효율적으로 관리할 수 있도록 지원하는 오픈소스 MLOps 프레임워크
Databricks MLflow는 특정 ML 프레임워크에 종속되지 않고 SparkML, ScikitLearn, XGBoost 등 다양한 프레임워크의 ML관리를 지원
Databricks MLflow는 Databricks에서 관리형으로 서비스 되기 때문에 별도의 MLflow 운영을 위한 호스팅 관리가 필요 없음
Databricks Notebook을 통합하여 ML모델에서 바로 해당되는 Notebook을 확인
Python, Java, R, Rest API를 지원
Unity Catalog 와의 통합으로 모델의 접근에 대한 권한제어를 통해 모델 거버넌스 달성

---

## Slide 9: 소프트웨어 개발과 ML 모델 개발의 비교

목표
소프트웨어 개발
ML모델 개발
기능 스펙 충족
평가지표 최적화
코드 작성
데이터 탐색

유닛 테스트
품질
데이터 전처리
코드의 품질에 좌우
데이터, 코드,
파라미터 품질에 좌우
리뷰 요청
모델 코드 작성
승인 획득
모델 학습 및 평가
도구
코드 커밋
단일 컴파일러, IDE를 활용
다양한 라이브러리와
프레임워크를 활용
모델구조와 하이퍼파라미터 튜닝
릴리즈 테스트
모델 배포
결과물
확정적으로 작동
데이터 트렌드에따라 변화
코드 릴리즈
성능 모니터링 및 재학습

---

## Slide 10: ML Lifecycle Management

Mlflow 가 제공하는 기능
추적(Tracking) : 실험을 추적하여 매개변수와 결과를 기록하고 비교
모델(Models) : 다양한 ML 라이브러리로부터 생성된 모델을 관리 및 배포
프로젝트(Projects) : ML 코드를 재사용 및 재현 가능한 형태로 패키징하여 공유하거나 프로덕션 환경으로 전송
모델 레지스트리(Model Registry) : 스테이징에서 프로덕션까지 모델의 전체 수명주기를 관리하기 위해 모델 저장소를 중앙 집중화
모델 서빙(Model Serving) : MLflow 모델을 REST 엔드포인트로 제공

![Slide 10 image (10.2" x 2.8")](./images/slide10_img01.png)

---

## Slide 11: Databricks’ Model Registry

모델 수명주기 관리
MLflow 모델 레지스트리는 MLflow 모델의 전체 수명주기를 관리하는 중앙 집중식 모델 리포지토리
MLflow 모델 레지스트리 기능은 Unity Catalog내에서 GUI와 API를 통해 활용 가능

모델 레지스트리 개념
모델(Model) : 실험이나 실행에서 기록된 MLflow 모델로 모델 레지스트리에 등록가능한 모델 객체
등록된 모델(Registered Model) : 모델 레지스트리에 등록된 MLflow 모델로 고유한 이름, 버전, 모델 계보, 기타 메타데이터가 포함
모델 버전(Model Version) : 등록된 모델의 버전으로 버전이 증가할때마다 모델의 버전번호 증가
모델 별칭(Model Alias) : 별칭은 등록된 모델의 특정 버전에 대한 변경 가능한 이름
모델 단계(Model Stage) : 모델의 각 단계(None , Staging , Production, Archived)를 지정 및 전환. 모델 단계는 Workspace Model Registry 레거시 기능으로, Unity Catalog환경 에서는 사용되지 않음
설명(Description) : 모델에 대한 설명 또는 추가적인 정보를 기재

---

## Slide 12: Databricks’ Model Deployment

Databricks 모델 서빙
Databricks Model Serving은 AI 모델을 배포, 관리 및 쿼리할 수 있는 통합 인터페이스를 제공
각 모델은 웹 또는 클라이언트 애플리케이션에 통합할 수 있는 REST API로 제공

모델 서빙 유형
커스텀 모델(Custom Models)- MLflow 형식으로 패키지된 사용자가 직접 개발한 Python 모델- Unity Catalog(또는 Workspace Model Registry)에 등록- scikit-learn, XGBoost, PyTorch, Hugging Face Transformer를 활용하여 생성된 모델
Foundation Model API- Databricks가 관리형으로 제공하는 관리형 모델- DBRX Instruct, Meta Llama 3 70B Instruct, Mixtral-8x7B Instruct, GTE Large, BGE Large를 제공- Pay-per-token 방식으로 과금
외부 모델(External Models)- Databricks 외부에서 호스팅되는 모델을 Databricks 모델 서빙에서 등록하여 사용하는 방식- 외부 모델을 Databricks 모델 서빙 엔드포인트로 통합하여 사용량과 권한제어를 중앙 집중 관리식으로 사용- OpenAI GPT-4, Anthropic Claude, Amazon Bedrock, Google Cloud Vertex AI 등을 등록 가능

---

## Slide 13: Databricks’ MLflow

실험(Experiment) 및 실행(Run)관리
모델의 하이퍼파라미터, 평가메트릭, 출력파일(Pickle, Data, Image, etc.), 소스파일들을 등록하여 관리
하이퍼파라미터 혹은 피처들을 달리한 모델의 평가메트릭(정확도, 로스율 등)을 비교하는 기능을 제공
태그를 통한 실험 검색 지원

< Mlflow에의해 등록된 실험 목록 >
< 실험결과의 평가지표들을 비교 >

![Slide 13 image (5.0" x 3.4")](./images/slide13_img01.png)

![Slide 13 image (5.0" x 3.4")](./images/slide13_img02.png)

---

## Slide 14: Databricks’ MLflow

![Slide 14 image (5.0" x 3.4")](./images/slide14_img01.png)

![Slide 14 image (4.9" x 3.4")](./images/slide14_img02.png)

---

## Slide 15: Databricks’ MLflow

![Slide 15 image (5.0" x 3.4")](./images/slide15_img01.png)

![Slide 15 image (5.0" x 3.4")](./images/slide15_img02.png)

---

## Slide 17: Compute Setting

![Slide 17 image (9.3" x 5.8")](./images/slide17_img01.png)

---

## Slide 18: Workspace Setting

3. 다운로드 받은 zip 파일 업로드
1. workspace 에서 더 보기 아이콘 선택

2. Import 선택

4. 업로드

---

## Slide 19: Workspace Setting

![Slide 19 image (8.5" x 5.2")](./images/slide19_img01.png)

---

## Slide 20: Dataset

![Slide 20 image (6.2" x 3.6")](./images/slide20_img01.png)

![Slide 20 image (6.1" x 3.5")](./images/slide20_img02.png)

---

## Slide 21: Dataset

Overview
games.csv - a table of games (or add-ons) information on ratings, pricing in US dollars $, release date, etc. A piece of extra non-tabular details on games, such as descriptions and tags, is in a metadata file;
users.csv - a table of user profiles' public information: the number of purchased products and reviews published;
recommendations.csv - a table of user reviews: whether the user recommends a product. The table represents a many-many relation between a game entity and a user entity.

---

## Slide 22: Dataset

Columns
| games.csv |
| --- |
| app\_id |
| title |
| date\_release |
| win |
| mac |
| linux |
| rating |
| positive\_ratio |
| user\_reviews |
| price\_final |
| price\_original |
| discount |
| stream\_deck |
| users.csv |
| --- |
| user\_id |
| products |
| reviews |
| recommendations.csv |
| --- |
| review\_id |
| app\_id |
| user\_id |
| helpful |
| funny |
| date |
| hours |
| is\_recommended |
| games\_metadata.json |
| --- |
| app\_id |
| description |
| tags |

---

## Slide 23: 00-Download Data

![Slide 23 image (8.5" x 1.9")](./images/slide23_img01.png)

![Slide 23 image (8.5" x 2.2")](./images/slide23_img02.png)

---

## Slide 25: 01-Files to Table

![Slide 25 image (7.9" x 2.6")](./images/slide25_img01.png)

---

## Slide 27: 03-Users Collaborative Filtering

목표
Mlflow model registry 에 대한 이해
SDK 와 UI 를 이용한 모델 서빙
모델 서빙 기능 익히기

---

## Slide 28: 02-Games Content-Based Filtering

| games.csv |
| --- |
| app\_id |
| title |
| date\_release |
| win |
| mac |
| linux |
| rating |
| positive\_ratio |
| user\_reviews |
| price\_final |
| price\_original |
| discount |
| stream\_deck |
| games\_metadata.json |
| --- |
| app\_id |
| description |
| tags |
| games\_sdf |
| --- |
| app\_id |
| title |
| date\_release |
| win |
| mac |
| linux |
| rating |
| positive\_ratio |
| user\_reviews |
| price\_final |
| price\_original |
| discount |
| stream\_deck |
| description |
| tags |

---

## Slide 29: 02-Games Content-Based Filtering

Price
Steam store has both F2P and Premium games available.
The average price for a AAA game is 70$
Products with price of less than 3$ are either low-quality demos or simple DLC's
Rating
Games with rating = overwhelmingly negative or very negative will be filtered out.
These ratings were formed under media influence (Overwatch 2), the game was abandoned by developer (Kinetic Void) or just extremely bad quality product (Wildlands - Narco Road or O2Jam Online)

---

## Slide 30: 02-Games Content-Based Filtering

![Slide 30 image (10.9" x 3.6")](./images/slide30_img01.png)

---

## Slide 31: 02-Games Content-Based Filtering

![Slide 31 image (8.5" x 4.7")](./images/slide31_img01.png)

---

## Slide 32: 02-Games Content-Based Filtering

Feature Architecture
TF-IDF
| games\_sdf |
| --- |
| app\_id |
| description |
| tags |
Multi-label Binarizer

---

## Slide 33: 02-Games Content-Based Filtering

![Slide 33 image (8.5" x 3.4")](./images/slide33_img01.png)

![Slide 33 image (6.4" x 2.9")](./images/slide33_img02.png)

---

## Slide 34: 02-Games Content-Based Filtering

![Slide 34 image (10.3" x 2.1")](./images/slide34_img01.png)

![Slide 34 image (10.3" x 1.5")](./images/slide34_img02.png)

---

## Slide 35: 02-Games Content-Based Filtering

![Slide 35 image (7.7" x 1.9")](./images/slide35_img01.png)

---

## Slide 36: 02-Games Content-Based Filtering

![Slide 36 image (8.5" x 3.7")](./images/slide36_img01.png)

---

## Slide 37: 02-Games Content-Based Filtering

![Slide 37 image (12.4" x 2.9")](./images/slide37_img01.png)

---

## Slide 38: 02-Games Content-Based Filtering

![Slide 38 image (7.0" x 5.0")](./images/slide38_img01.png)

---

## Slide 39: Mlflow Model

Log, load, and register MLflow models
An MLflow Model is a standard format for packaging machine learning models that can be used in a variety of downstream tools
—for example, batch inference on Apache Spark or real-time serving through a REST API.
The format defines a convention that lets you save a model in different flavors (python-function, pytorch, sklearn, and so on), that can be understood by different model serving and inference platforms.

---

## Slide 40: Mlflow Model

![Slide 40 image (1.6" x 4.6")](./images/slide40_img01.png)

---

## Slide 41: Mlflow Model

![Models from code comparison with legacy serialization](./images/slide41_img01.png)

---

## Slide 42: Mlflow Model

Pyfunc Flavors
Building a simple Models From Code model

---

## Slide 43: 02-Games Content-Based Filtering

![Slide 43 image (7.0" x 5.0")](./images/slide43_img01.png)

---

## Slide 44: 02-Games Content-Based Filtering

![Slide 44 image (7.0" x 5.0")](./images/slide44_img01.png)

![Slide 44 image (4.8" x 2.1")](./images/slide44_img02.png)

---

## Slide 45: 02-Games Content-Based Filtering

![Slide 45 image (8.5" x 3.9")](./images/slide45_img01.png)

---

## Slide 46: 02-Games Content-Based Filtering

![Slide 46 image (3.7" x 1.7")](./images/slide46_img01.png)

![Slide 46 image (7.0" x 4.4")](./images/slide46_img02.png)

---

## Slide 47: 02-Games Content-Based Filtering

![Slide 47 image (7.0" x 4.4")](./images/slide47_img01.png)

![Slide 47 image (4.0" x 0.7")](./images/slide47_img02.png)

---

## Slide 48: 02-Games Content-Based Filtering

![Slide 48 image (8.2" x 4.7")](./images/slide48_img01.png)

---

## Slide 49: 02-Games Content-Based Filtering

![Slide 49 image (4.8" x 1.9")](./images/slide49_img01.png)

![Slide 49 image (4.8" x 1.6")](./images/slide49_img02.png)

![Slide 49 image (4.8" x 1.2")](./images/slide49_img03.png)

![Slide 49 image (4.8" x 3.6")](./images/slide49_img04.png)

---

## Slide 50: 02-Games Content-Based Filtering

![Slide 50 image (8.5" x 4.3")](./images/slide50_img01.png)

---

## Slide 51: 02-Games Content-Based Filtering

![Slide 51 image (7.7" x 4.8")](./images/slide51_img01.png)

---

## Slide 53: 03-Users Collaborative Filtering

목표
Surprise 패키지를 사용한 여러 모델 개발
고도화된 Mlflow 의 모델 저장 방법
Load Context
Packages

---

## Slide 54: 03-Users Collaborative Filtering

![Slide 54 image (8.5" x 4.5")](./images/slide54_img01.png)

---

## Slide 55: 03-Users Collaborative Filtering

![Slide 55 image (4.4" x 3.2")](./images/slide55_img01.png)

![Slide 55 image (4.0" x 3.3")](./images/slide55_img02.png)

![Slide 55 image (4.0" x 3.2")](./images/slide55_img03.png)

![Slide 55 image (2.8" x 1.2")](./images/slide55_img04.png)

---

## Slide 56: 03-Users Collaborative Filtering

![Slide 56 image (8.5" x 4.4")](./images/slide56_img01.png)

---

## Slide 57: 03-Users Collaborative Filtering

![Slide 57 image (9.3" x 5.3")](./images/slide57_img01.png)

---

## Slide 58: 03-Users Collaborative Filtering

![Slide 58 image (4.5" x 5.6")](./images/slide58_img01.png)

---

## Slide 59: 03-Users Collaborative Filtering

![Slide 59 image (9.3" x 1.4")](./images/slide59_img01.png)

![Slide 59 image (9.3" x 2.5")](./images/slide59_img02.png)

---

## Slide 60: Mlflow Depdency Management

![Slide 60 image (8.5" x 4.8")](./images/slide60_img01.png)

---

## Slide 61: Mlflow Depdency Management

![Slide 61 image (7.7" x 0.9")](./images/slide61_img01.png)

![Slide 61 image (3.1" x 3.2")](./images/slide61_img02.png)

![Slide 61 image (4.0" x 1.7")](./images/slide61_img03.png)

![Slide 61 image (3.3" x 2.6")](./images/slide61_img04.png)

---

## Slide 62: Mlflow Depdency Management

![Slide 62 image (11.1" x 0.9")](./images/slide62_img01.png)

![Slide 62 image (7.0" x 1.5")](./images/slide62_img02.png)

![Slide 62 image (3.7" x 3.3")](./images/slide62_img03.png)

---

## Slide 63: Mlflow Depdency Management

![Slide 63 image (7.0" x 1.2")](./images/slide63_img01.png)

![Slide 63 image (3.7" x 3.3")](./images/slide63_img02.png)

![Slide 63 image (11.3" x 0.7")](./images/slide63_img03.png)

---

## Slide 64: 03-Users Collaborative Filtering

![Slide 64 image (12.4" x 2.8")](./images/slide64_img01.png)

---

## Slide 66: 04-Feature Store Baseline

목표
Feature Store 사용법에 대한 이해
Mlflow 기본 사용법
Feature Store 와 결합된 모델 사용법
모델 서빙을 이용한 실시간 추론

---

## Slide 67: 04-Feature Store Baseline

![Slide 67 image (7.1" x 4.8")](./images/slide67_img01.png)

---

## Slide 68: 04-Feature Store Baseline

Create Feature Stores
| recommendations\_feature |
| --- |
| review\_id |
| app\_id |
| user\_id |
| helpful |
| funny |
| date |
| hours |
| is\_recommended |
| users\_feature |
| --- |
| user\_id |
| products |
| reviews |
| games\_feature |
| --- |
| app\_id |
| title |
| date\_release |
| win |
| mac |
| linux |
| rating |
| positive\_ratio |
| user\_reviews |
| price\_final |
| price\_original |
| discount |
| stream\_deck |
PK
PK
PK

---

## Slide 69: 04-Feature Store Baseline

![Slide 69 image (4.8" x 1.3")](./images/slide69_img01.png)

![Slide 69 image (6.4" x 3.0")](./images/slide69_img02.png)

---

## Slide 70: 04-Feature Store Baseline

![Slide 70 image (6.4" x 3.9")](./images/slide70_img01.png)

![Slide 70 image (5.8" x 3.3")](./images/slide70_img02.png)

---

## Slide 71: 04-Feature Store Baseline

![Slide 71 image (10.3" x 0.8")](./images/slide71_img01.png)

---

## Slide 72: 04-Feature Store Baseline

![Slide 72 image (3.3" x 4.7")](./images/slide72_img01.png)

![Slide 72 image (5.1" x 2.1")](./images/slide72_img02.png)

![Slide 72 image (5.8" x 0.5")](./images/slide72_img03.png)

---

## Slide 73: 04-Feature Store Baseline

![Slide 73 image (8.5" x 3.9")](./images/slide73_img01.png)

---

## Slide 74: 04-Feature Store Baseline

![Slide 74 image (10.3" x 4.4")](./images/slide74_img01.png)

---

## Slide 75: Key Concepts in Tracking

![Slide 75 image (6.7" x 3.4")](./images/slide75_img01.png)

---

## Slide 76: Mlflow tracking

![Slide 76 image (6.4" x 3.7")](./images/slide76_img01.png)

![Slide 76 image (6.0" x 3.7")](./images/slide76_img02.png)

---

## Slide 77: Mlflow tracking

![Slide 77 image (6.0" x 4.2")](./images/slide77_img01.png)

![Slide 77 image (6.0" x 3.7")](./images/slide77_img02.png)

---

## Slide 78: Mlflow tracking

![Slide 78 image (6.0" x 2.2")](./images/slide78_img01.png)

![Slide 78 image (6.0" x 3.7")](./images/slide78_img02.png)

---

## Slide 79

![Slide 79 image (2.0" x 1.2")](./images/slide79_img01.png)

![Slide 79 image (4.0" x 2.2")](./images/slide79_img02.png)

![Slide 79 image (1.9" x 1.7")](./images/slide79_img03.png)

![Slide 79 image (8.5" x 1.0")](./images/slide79_img04.png)

---

## Slide 80: 04-Feature Store Baseline

![Slide 80 image (10.3" x 4.4")](./images/slide80_img01.png)

---

## Slide 81: 04-Feature Store Baseline

![Slide 81 image (10.3" x 4.4")](./images/slide81_img01.png)

---

## Slide 82: 04-Feature Store Baseline

![Slide 82 image (7.8" x 4.8")](./images/slide82_img01.png)

---

## Slide 83: 04-Feature Store Baseline

Inference with feature engineering with full feature

---

## Slide 84: 04-Feature Store Baseline

![Slide 84 image (8.5" x 4.9")](./images/slide84_img01.png)

---

## Slide 85: 04-Feature Store Baseline

![Slide 85 image (3.7" x 2.6")](./images/slide85_img01.png)

![Slide 85 image (8.5" x 1.4")](./images/slide85_img02.png)

![Slide 85 image (8.5" x 1.4")](./images/slide85_img03.png)

---

## Slide 86: 04-Feature Store Baseline

![Slide 86 image (4.6" x 4.3")](./images/slide86_img01.png)

![Slide 86 image (7.0" x 1.2")](./images/slide86_img02.png)

![Slide 86 image (7.1" x 2.1")](./images/slide86_img03.png)

---

## Slide 87: 04-Feature Store Baseline

![Slide 87 image (7.4" x 4.3")](./images/slide87_img01.png)

---

## Slide 88: 04-Feature Store Baseline

![Slide 88 image (9.3" x 2.2")](./images/slide88_img01.png)

![Slide 88 image (9.3" x 1.9")](./images/slide88_img02.png)

---

## Slide 89: 04-Feature Store Baseline

![Slide 89 image (4.9" x 1.8")](./images/slide89_img01.png)

![Slide 89 image (4.9" x 2.8")](./images/slide89_img02.png)

![Slide 89 image (7.0" x 2.9")](./images/slide89_img03.png)

---

## Slide 90: 04-Feature Store Baseline

![Slide 90 image (7.0" x 4.6")](./images/slide90_img01.png)

---

## Slide 91: 04-Feature Store Baseline

![Slide 91 image (9.3" x 5.1")](./images/slide91_img01.png)

---

## Slide 92: 04-Feature Store Baseline

![Slide 92 image (6.7" x 5.1")](./images/slide92_img01.png)

---

## Slide 93: 04-Feature Store Baseline

![Slide 93 image (8.1" x 5.0")](./images/slide93_img01.png)

---

## Slide 94: 04-Feature Store Baseline

![Slide 94 image (7.1" x 5.0")](./images/slide94_img01.png)

---

## Slide 96: 05-Automl

목표
데이터브릭스 AutoML 을 이용해 분류 모델 고도화
AutoML 사용법에 대한 이해
AutoML 으로 탐색한 모델과 business case 의 결합

---

## Slide 97: Databricks AutoML

A glass-box solution that empowers data teams without taking away control

MLflow experiment
Auto-created MLflow Experiment to track models and metrics
Data exploration notebook
Generated notebook with feature summary statistics and distributions

Reproducible trial notebooks
Generated notebooks with source code for every model
Easily deploy to Model Registry
UI and API to start AutoML training

Iterate further on models from AutoML, adding your expertise

![Slide 97 image (2.1" x 1.6")](./images/slide97_img01.png)

![Slide 97 image (2.1" x 1.7")](./images/slide97_img02.png)

> **Notes:** Databricks AutoML provides a glass-box solution to AutoML.  It provides the benefits of automation, while giving the user full ownership of code and models.
> 
> You can run AutoML from the UI or the API.  This makes it accessible to citizen data scientists, with the power of code for experienced data scientists.
> 
> AutoML will test different models, tune hyperparameters, and return the list of models produced.  Three key artifacts are returned:
> MLflow Experiment: AutoML integrates smoothly with existing MLflow Tracking, automatically creating an experiment listing all of the models created by your AutoML run.
> Data exploration notebook: AutoML generates a notebook exploring your data.  This helps you to visually understand your data and identify potential problems with it.
> Reproducible trial notebooks: For every potential model it trains, AutoML generates a notebook which can reproduce that model training.  This is the key “glass-box” feature: it allows experts to get a quick start to modeling and then to clone the notebook and use their expert knowledge to improve the model further.
> 
> With all models automatically logged to MLflow, it is easy to deploy an AutoML model for batch, streaming, or online inference via the Model Registry.

---

## Slide 98: AutoML on Databricks

![Slide 98 image (1.8" x 0.6")](./images/slide98_img01.png)

> **Notes:** Just to recap
> 
> Most AutoML solutions are an “opaque box”, meaning they don’t know exactly how the model was trained.
> Data scientists aren’t usually comfortable with this because they can’t tell what data preprocessing was done, what feature engineering was done, etc. so they are hesitant to put these models into production. Oftentimes, they ‘reverse engineer’ the returned model so they can tweak it.
> Our solution provides a transparent way for users to see how a model was trained, learn how to use Databricks features like MLflow, and provides the training notebook for easy modification.

---

## Slide 99: Glassbox AutoML

![Slide 99 image (5.8" x 3.4")](./images/slide99_img01.png)

![Slide 99 image (5.3" x 3.1")](./images/slide99_img02.png)

![Slide 99 image (5.8" x 3.5")](./images/slide99_img03.png)

---

## Slide 100: 05-Automl

![Slide 100 image (5.8" x 3.8")](./images/slide100_img01.png)

![Slide 100 image (7.0" x 2.4")](./images/slide100_img02.png)

---

## Slide 101: 05-Automl

![Slide 101 image (7.9" x 4.9")](./images/slide101_img01.png)

---

## Slide 102: 05-Automl

![Slide 102 image (7.7" x 4.8")](./images/slide102_img01.png)

---

## Slide 103: 05-Automl

![Slide 103 image (7.7" x 4.8")](./images/slide103_img01.png)

---

## Slide 104: 05-Automl

![Slide 104 image (7.7" x 4.8")](./images/slide104_img01.png)

---

## Slide 105: 05-Automl

![Slide 105 image (8.5" x 5.1")](./images/slide105_img01.png)

---

## Slide 106: 05-Automl

![Slide 106 image (8.5" x 4.7")](./images/slide106_img01.png)

---

## Slide 107: 05-Automl

![Slide 107 image (6.4" x 4.4")](./images/slide107_img01.png)

![Slide 107 image (6.4" x 2.2")](./images/slide107_img02.png)

---

## Slide 109: 06-Advanced User Cold Start

목표
새로운 유저에 대한 cold start 고도화
기존에 새로운 게임에 대한 추천 여부를 랜덤으로 채움
이 부분을 앞선 챕터에서 학습한 모델을 이용해 고도화

---

## Slide 110: 06-Advanced User Cold Start

![Slide 110 image (8.5" x 4.7")](./images/slide110_img01.png)

---

## Slide 111: 06-Advanced User Cold Start

![Slide 111 image (5.9" x 4.1")](./images/slide111_img01.png)

![Slide 111 image (5.2" x 2.5")](./images/slide111_img02.png)

---

## Slide 113: Databricks Lakehouse Monitoring

Automated insights and out-of-the box metrics on data and ML pipelines
Fully managed so no time wasted managing infrastructure, calculating metrics, or building dashboards from scratch
Frictionless with easy setup and out-of-the-box metrics and generated dashboards
Unified solution for data and models for holistic understanding

![Slide 113 image (6.7" x 3.6")](./images/slide113_img01.png)

---

## Slide 114: Monitor all tables in your lakehouse

Different out-of-the-box analysis metrics based on table type(s)
Snapshot Table
Time Series Table
Model(s)
Inference Table
Bronze/Silver/Gold
Feature table

monitor
monitor
monitor
TimeStamp
Features
Prediction column
Label column
Model ID
Databricks batch scoring pipeline
Databricks Model Serving Endpoint
ETL to ingest from external serving (request logs) or batch pipelines
TimeStamp
Columns/Features
Columns

---

## Slide 115: Monitoring a table in the Lakehouse

How does it work?
Table

Anomaly detection and drift for training-vs-scoring and scoring-vs-scoring
Delta/changes in nulls and counts, PSI, KS divergence, Mean shift, Total Variation distance, L-inf distance, χ2 test, Wasserstein distance, …

Distributional statistics for inputs, outputs
Minimum, maximum, standard deviation, quantiles, top occurring value, …
🔎monitor
Profiling
Table
Drift
Table
Model quality metrics (if labels are provided)
Classification: Accuracy, F1, precision, recall Regression: MSE, RMSE, MAE, R2, …

Dashboard
Custom metrics
Expressed as SQL expressions

Webhooks

Alerts

DBSQL

---

## Slide 116: Built on Unity Catalog

Background service that incrementally processes data in Unity Catalog tables

Calculates profile metrics stored in UC table
Calculates drift metrics stored in UC table
Supports custom metrics as SQL expressions
Auto-generates DBSQL dashboard to visualize metrics over time

![Slide 116 image (6.4" x 4.3")](./images/slide116_img01.png)

![Slide 116 image (4.3" x 2.5")](./images/slide116_img02.png)

---

## Slide 117: Data Drift

![Model Drift Workflow](./images/slide117_img01.png)

---

## Slide 118: Data Drift

![Model Drift Workflow](./images/slide118_img01.png)

---

## Slide 119: 07-Quality Monitoring

![Slide 119 image (7.7" x 4.6")](./images/slide119_img01.png)

---

## Slide 120: 07-Quality Monitoring

![Slide 120 image (7.7" x 4.5")](./images/slide120_img01.png)

---

## Slide 121: 07-Quality Monitoring

![Slide 121 image (7.0" x 4.9")](./images/slide121_img01.png)

---

## Slide 122: 07-Quality Monitoring

![Slide 122 image (6.2" x 4.9")](./images/slide122_img01.png)

![Slide 122 image (4.6" x 4.2")](./images/slide122_img02.png)

---

## Slide 123: 07-Quality Monitoring

![Slide 123 image (6.8" x 4.7")](./images/slide123_img01.png)
