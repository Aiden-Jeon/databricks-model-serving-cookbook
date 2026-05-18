"""Feature engineering helpers."""

from __future__ import annotations

import pandas as pd


def add_lifetime_value(df: pd.DataFrame) -> pd.DataFrame:
    """LTV proxy = monthly_charges × tenure_months."""
    df = df.copy()
    df["ltv"] = df["monthly_charges"] * df["tenure_months"]
    return df


def add_risk_bucket(df: pd.DataFrame) -> pd.DataFrame:
    """support_tickets 기반 risk bucket 라벨링."""
    df = df.copy()
    df["risk_bucket"] = pd.cut(
        df["support_tickets"],
        bins=[-1, 3, 9, 1000],
        labels=["low", "medium", "high"],
    ).astype(str)
    return df


def add_tenure_band(df: pd.DataFrame) -> pd.DataFrame:
    """tenure_months 를 단계별 band 로."""
    df = df.copy()
    df["tenure_band"] = pd.cut(
        df["tenure_months"],
        bins=[-1, 12, 36, 60, 1000],
        labels=["new", "growing", "mature", "loyal"],
    ).astype(str)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """전체 feature engineering 파이프라인."""
    return df.pipe(add_lifetime_value).pipe(add_risk_bucket).pipe(add_tenure_band)
