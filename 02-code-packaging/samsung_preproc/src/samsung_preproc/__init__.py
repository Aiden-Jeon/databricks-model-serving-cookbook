"""samsung_preproc — customer churn preprocessing utilities."""

from samsung_preproc.features import (
    add_lifetime_value,
    add_risk_bucket,
    add_tenure_band,
    preprocess,
)

__all__ = [
    "add_lifetime_value",
    "add_risk_bucket",
    "add_tenure_band",
    "preprocess",
]

__version__ = "0.1.0"
