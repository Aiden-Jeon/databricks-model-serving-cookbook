# Databricks notebook source
# MAGIC %md
# MAGIC # Config
# MAGIC
# MAGIC 모든 노트북에서 `%run ./config` 로 import 합니다.
# MAGIC catalog / schema / volume / model / endpoint 이름을 한 곳에서 관리합니다.

# COMMAND ----------

catalog = "main"
schema = "model_serving_cookbook"
volume = "artifacts"

# Volume path — wheel, joblib, image 등 모든 binary artifact 저장
volume_path = f"/Volumes/{catalog}/{schema}/{volume}"

# 모델 이름들 — 노트북 챕터별로 별도 모델 생성
model_basic = f"{catalog}.{schema}.churn_basic"
model_pyfunc = f"{catalog}.{schema}.churn_pyfunc"
model_deps = f"{catalog}.{schema}.churn_deps"
model_codepaths = f"{catalog}.{schema}.churn_codepaths"
model_wheel = f"{catalog}.{schema}.churn_wheel"
model_express = f"{catalog}.{schema}.churn_express"

# Serving endpoint 이름들 — workspace에서 유일해야 하므로 prefix 추가 권장
endpoint_basic = "churn-basic-endpoint"
endpoint_wheel = "churn-wheel-endpoint"
endpoint_express = "churn-express-endpoint"

# Experiment path — 워크스페이스 사용자별 분리
import os
try:
    user = (
        dbutils.notebook.entry_point.getDbutils()
        .notebook()
        .getContext()
        .userName()
        .get()
    )
except Exception:
    user = os.environ.get("USER", "unknown")

experiment_path = f"/Users/{user}/model_serving_cookbook"

print(f"catalog       : {catalog}")
print(f"schema        : {schema}")
print(f"volume_path   : {volume_path}")
print(f"experiment    : {experiment_path}")
