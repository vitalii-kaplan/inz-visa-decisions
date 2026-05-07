from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats


INPUT_PATH = Path("data/prepared/inz_2022-2025_wb_who_m49_combined.csv")
RESULTS_DIR = Path("data/results")

COEFFICIENTS_PATH = RESULTS_DIR / "Coefficients_weighted_un_m49.csv"
PREDICTION_PATH = RESULTS_DIR / "Prediction_weighted_un_m49.csv"
PREDICTION_RATE_PATH = RESULTS_DIR / "Prediction_rate_weighted_un_m49.csv"
SCORE_PATH = RESULTS_DIR / "Score_weighted_un_m49.csv"

TARGET_COL = "Approval rate"
WEIGHT_COL = "Applications_log10"
INCLUDE_COLS = [
    "WHO_Under5_Mortality_per_1000_live_births",
    "WHO_Maternal_Mortality_per_100000_live_births",
    "WHO_Physician_Density_per_10000_population",
    "WHO_DTP3_Immunization_Coverage_pct",
    "WB_FY2026_Income_Group",
    "WB_FY2026_Lending_Category",
    "GDP_per_capita_current_USD",
    "Life_expectancy_at_birth_years",
    "Internet_users_pct_population",
    "Urban_population_pct",
    "GNI_per_capita_Atlas_current_USD",
    "UN M49",
]
EXCLUDE_COLS = {"Country", "Applications_log10", "WHO_Region", "WB_FY2026_Region"}


def read_input():
    df = pd.read_csv(
        INPUT_PATH,
        sep=",",
        quotechar='"',
        header=0,
        encoding="UTF-8",
        na_values=["", " "],
        keep_default_na=True,
        skipinitialspace=True,
    )
    dtypes = {
        "Country": "string",
        "Approval rate": "Float64",
        "Applications_log10": "Float64",
        "WHO_Region": "string",
        "WHO_Under5_Mortality_per_1000_live_births": "Float64",
        "WHO_Maternal_Mortality_per_100000_live_births": "Float64",
        "WHO_Physician_Density_per_10000_population": "Float64",
        "WHO_DTP3_Immunization_Coverage_pct": "Int64",
        "WB_FY2026_Region": "string",
        "WB_FY2026_Income_Group": "string",
        "WB_FY2026_Lending_Category": "string",
        "GDP_per_capita_current_USD": "Float64",
        "Life_expectancy_at_birth_years": "Float64",
        "Internet_users_pct_population": "Float64",
        "Urban_population_pct": "Float64",
        "GNI_per_capita_Atlas_current_USD": "Int64",
        "UN M49": "string",
    }
    for col, dtype in dtypes.items():
        if col not in df.columns:
            continue
        try:
            if dtype in ("Int64", "Float64"):
                df[col] = pd.to_numeric(df[col], errors="coerce").astype(dtype)
            else:
                df[col] = df[col].astype(dtype)
        except Exception:
            pass
    return df


def minmax_normalize(df):
    out_df = df.copy()
    candidates = [col for col in out_df.columns if col not in {TARGET_COL, WEIGHT_COL}]
    norm_cols = out_df[candidates].select_dtypes(
        include=["number", "bool", "boolean", "Int64", "Float64"]
    ).columns.tolist()
    if not norm_cols:
        return out_df

    out_df[norm_cols] = out_df[norm_cols].apply(pd.to_numeric, errors="coerce")
    col_min = out_df[norm_cols].min(axis=0, skipna=True)
    col_max = out_df[norm_cols].max(axis=0, skipna=True)
    for col in norm_cols:
        mn = col_min.get(col)
        mx = col_max.get(col)
        rng = (mx - mn) if (mn is not None and mx is not None) else None
        if rng is None or pd.isna(rng) or rng == 0:
            out_df[col] = 0.0
        else:
            out_df[col] = ((out_df[col] - mn) / rng).astype(float)
    return out_df


def build_design_matrix(df):
    source_cols = [col for col in INCLUDE_COLS if col in df.columns and col != TARGET_COL]
    source_cols = [col for col in source_cols if col not in EXCLUDE_COLS]
    if not source_cols:
        raise ValueError("No feature columns selected")

    feature_info = []
    x_parts = []
    for col in source_cols:
        series = df[col]
        if pd.api.types.is_numeric_dtype(series) or pd.api.types.is_bool_dtype(series):
            values = pd.to_numeric(series, errors="coerce").astype(float)
            x_parts.append(values.to_frame(col))
            feature_info.append({"kind": "numeric", "column": col, "features": [col]})
        else:
            cat = series.astype("object").where(series.notna(), "Missing").astype(str)
            dummies = pd.get_dummies(cat, prefix=col, prefix_sep="=", dtype=float)
            drop_level = None
            if len(dummies.columns) > 0:
                drop_col = dummies.columns[0]
                drop_level = str(drop_col).split("=", 1)[1] if "=" in str(drop_col) else str(drop_col)
                dummies = dummies.iloc[:, 1:]
            if len(dummies.columns) > 0:
                x_parts.append(dummies)
            feature_info.append(
                {
                    "kind": "categorical",
                    "column": col,
                    "levels": sorted(cat.dropna().unique().tolist()),
                    "drop_level": drop_level,
                    "features": list(dummies.columns),
                }
            )

    x_df = pd.concat(x_parts, axis=1) if x_parts else pd.DataFrame(index=df.index)
    return x_df.astype(float), feature_info


def fit_weighted_linear_model(x_df, y, weights):
    valid_mask = y.notna() & weights.notna() & (weights > 0) & ~x_df.isna().any(axis=1)
    x_fit = x_df.loc[valid_mask].copy()
    y_fit = y.loc[valid_mask].astype(float)
    w_fit = weights.loc[valid_mask].astype(float)
    if x_fit.empty:
        raise ValueError("No training rows available")

    design_cols = list(x_fit.columns)
    x_mat = np.column_stack([x_fit.to_numpy(dtype=float), np.ones(len(x_fit), dtype=float)])
    y_vec = y_fit.to_numpy(dtype=float)
    w_vec = w_fit.to_numpy(dtype=float)
    sqrt_w = np.sqrt(w_vec)
    x_weighted = x_mat * sqrt_w[:, None]
    y_weighted = y_vec * sqrt_w

    coef = np.linalg.lstsq(x_weighted, y_weighted, rcond=None)[0]
    pred_fit = x_mat @ coef
    resid = y_vec - pred_fit
    df_resid = int(max(len(y_vec) - x_mat.shape[1], 0))

    if df_resid > 0:
        weighted_sse = float(np.sum(w_vec * resid**2))
        sigma2 = weighted_sse / df_resid
        cov = sigma2 * np.linalg.pinv(x_mat.T @ (w_vec[:, None] * x_mat))
        std_err = np.sqrt(np.diag(cov))
        t_vals = np.divide(coef, std_err, out=np.full_like(coef, np.nan), where=std_err != 0)
        p_vals = 2 * scipy_stats.t.sf(np.abs(t_vals), df_resid)
    else:
        std_err = np.full_like(coef, np.nan, dtype=float)
        t_vals = np.full_like(coef, np.nan, dtype=float)
        p_vals = np.full_like(coef, np.nan, dtype=float)

    coef_df = pd.DataFrame(
        {
            "Variable": design_cols + ["Intercept"],
            "Coeff.": coef,
            "Std. Err.": std_err,
            "t-value": t_vals,
            "P>|t|": p_vals,
        }
    )
    return coef, coef_df, valid_mask


def predict(x_df, coef):
    x_mat = np.column_stack([x_df.to_numpy(dtype=float), np.ones(len(x_df), dtype=float)])
    return x_mat @ coef


def score_predictions(y_true, y_pred, weights):
    err = y_true - y_pred
    w_sum = float(np.sum(weights))
    y_bar_weighted = float(np.sum(weights * y_true) / w_sum)
    weighted_sse = float(np.sum(weights * err**2))
    weighted_sst = float(np.sum(weights * (y_true - y_bar_weighted) ** 2))
    unweighted_sse = float(np.sum(err**2))
    unweighted_sst = float(np.sum((y_true - np.mean(y_true)) ** 2))
    rows = [
        ("weighted_r_squared", 1.0 - weighted_sse / weighted_sst if weighted_sst != 0 else np.nan),
        ("weighted_mae", float(np.sum(weights * np.abs(err)) / w_sum)),
        ("weighted_mse", float(np.sum(weights * err**2) / w_sum)),
        ("weighted_rmse", float(np.sqrt(np.sum(weights * err**2) / w_sum))),
        ("weighted_mean_signed_error", float(np.sum(weights * err) / w_sum)),
        ("unweighted_r_squared", 1.0 - unweighted_sse / unweighted_sst if unweighted_sst != 0 else np.nan),
        ("unweighted_mae", float(np.mean(np.abs(err)))),
        ("unweighted_mse", float(np.mean(err**2))),
        ("unweighted_rmse", float(np.sqrt(np.mean(err**2)))),
        ("unweighted_mean_signed_error", float(np.mean(err))),
    ]
    if np.any(y_true == 0):
        rows.append(("weighted_mape", np.nan))
        rows.append(("unweighted_mape", np.nan))
    else:
        rows.append(("weighted_mape", float(np.sum(weights * np.abs(err / y_true)) / w_sum)))
        rows.append(("unweighted_mape", float(np.mean(np.abs(err / y_true)))))
    return pd.DataFrame(rows, columns=["Metric", "Value"])


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = read_input()
    normalized_df = minmax_normalize(raw_df)
    x_df, _feature_info = build_design_matrix(normalized_df)
    y = pd.to_numeric(normalized_df[TARGET_COL], errors="coerce").astype(float)
    weights = pd.to_numeric(normalized_df[WEIGHT_COL], errors="coerce").astype(float)

    coef, coef_df, valid_mask = fit_weighted_linear_model(x_df, y, weights)
    prediction = predict(x_df.loc[valid_mask].astype(float), coef)
    out_df = normalized_df.loc[valid_mask, ["Country", TARGET_COL, WEIGHT_COL]].copy()
    out_df["Prediction (Approval rate)"] = prediction
    out_df["Prediction_delta"] = out_df[TARGET_COL] - out_df["Prediction (Approval rate)"]
    out_df["Prediction_rate"] = out_df[TARGET_COL] / out_df["Prediction (Approval rate)"]

    score_df = score_predictions(
        out_df[TARGET_COL].to_numpy(dtype=float),
        out_df["Prediction (Approval rate)"].to_numpy(dtype=float),
        weights.loc[valid_mask].to_numpy(dtype=float),
    )

    coef_df.to_csv(COEFFICIENTS_PATH, index=False)
    out_df[["Country", TARGET_COL, WEIGHT_COL, "Prediction (Approval rate)"]].to_csv(
        PREDICTION_PATH,
        index=False,
    )
    out_df.sort_values("Prediction_rate").to_csv(PREDICTION_RATE_PATH, index=False)
    score_df.to_csv(SCORE_PATH, index=False)


if __name__ == "__main__":
    main()
