from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd


RESULTS_DIR = Path("data/results")
SUPPORT_DIR = Path("data/support")
ARTICLE_IMGS_DIR = Path("article/imgs")

MODELS = {
    "un_m49": RESULTS_DIR / "Prediction_un_m49.csv",
    "wb": RESULTS_DIR / "Prediction_wb.csv",
    "who": RESULTS_DIR / "Prediction_who.csv",
    "no_region": RESULTS_DIR / "Prediction_no_region.csv",
}

PREDICTION_RATE_MODELS = {
    "un_m49": RESULTS_DIR / "Prediction_rate_un_m49.csv",
    "wb": RESULTS_DIR / "Prediction_rate_wb.csv",
    "who": RESULTS_DIR / "Prediction_rate_who.csv",
    "no_region": RESULTS_DIR / "Prediction_rate_no_region.csv",
}

APPROXIMATION_PLOTS = {
    "un_m49": {
        "input": RESULTS_DIR / "Prediction_un_m49.csv",
        "svg": RESULTS_DIR / "approximation_sp_m49.svg",
        "pdf": ARTICLE_IMGS_DIR / "approximation_sp_m49.pdf",
        "title": "UN M49 regions\nR-squared = 0.867, MAE = 0.069, RMSE = 0.090",
    },
    "wb": {
        "input": RESULTS_DIR / "Prediction_wb.csv",
        "svg": RESULTS_DIR / "approximation_sp_wb.svg",
        "pdf": ARTICLE_IMGS_DIR / "approximation_sp_wb.pdf",
        "title": "World Bank regions\nR-squared = 0.812, MAE = 0.082, RMSE = 0.107",
    },
    "who": {
        "input": RESULTS_DIR / "Prediction_who.csv",
        "svg": RESULTS_DIR / "approximation_sp_who.svg",
        "pdf": ARTICLE_IMGS_DIR / "approximation_sp_who.pdf",
        "title": "WHO regions\nR-squared = 0.786, MAE = 0.087, RMSE = 0.114",
    },
    "no_region": {
        "input": RESULTS_DIR / "Prediction_no_region.csv",
        "svg": RESULTS_DIR / "approximation_sp_no_region.svg",
        "pdf": ARTICLE_IMGS_DIR / "approximation_sp_no_region.pdf",
        "title": "No regional classification\nR-squared = 0.706, MAE = 0.100, RMSE = 0.134",
    },
}


def load_prediction(path):
    df = pd.read_csv(path)
    required = [
        "Country",
        "Approval rate",
        "Prediction (Approval rate)",
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{path} is missing required columns: {missing}")

    df = df.copy()
    for col in ["Approval rate", "Prediction (Approval rate)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Approval rate", "Prediction (Approval rate)"])
    df["Prediction_delta"] = df["Approval rate"] - df["Prediction (Approval rate)"]
    return df


def load_prediction_rate(path):
    df = pd.read_csv(path)
    required = [
        "Country",
        "Approval rate",
        "Prediction (Approval rate)",
        "Prediction_delta",
        "Prediction_rate",
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{path} is missing required columns: {missing}")

    df = df.copy()
    for col in ["Approval rate", "Prediction (Approval rate)", "Prediction_delta", "Prediction_rate"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["Prediction_rate"])


def residual_summary(model_name, df):
    residuals = df["Prediction_delta"]
    fitted = df["Prediction (Approval rate)"]
    observed = df["Approval rate"]
    return {
        "model": model_name,
        "n": len(df),
        "observed_mean": observed.mean(),
        "fitted_mean": fitted.mean(),
        "residual_mean": residuals.mean(),
        "residual_std": residuals.std(ddof=1),
        "residual_min": residuals.min(),
        "residual_q25": residuals.quantile(0.25),
        "residual_median": residuals.median(),
        "residual_q75": residuals.quantile(0.75),
        "residual_max": residuals.max(),
        "residual_abs_mean": residuals.abs().mean(),
        "residual_abs_max": residuals.abs().max(),
    }


def plot_residuals_vs_fitted(model_name, df, output_path):
    width, height = 800, 600
    left, right, top, bottom = 90, 35, 55, 80
    plot_w = width - left - right
    plot_h = height - top - bottom

    x_min, x_max = 0.0, 1.2
    y_min, y_max = -0.5, 0.5

    def sx(value):
        return left + (float(value) - x_min) / (x_max - x_min) * plot_w

    def sy(value):
        return top + (y_max - float(value)) / (y_max - y_min) * plot_h

    x_ticks = [0.0, 0.3, 0.6, 0.9, 1.2]
    y_ticks = [-0.5, -0.25, 0.0, 0.25, 0.5]
    zero_y = sy(0.0)

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text { font-family: Arial, Helvetica, sans-serif; fill: #222; }",
        ".axis { stroke: #333; stroke-width: 1.2; }",
        ".grid { stroke: #d8d8d8; stroke-width: 0.8; }",
        ".zero { stroke: #444; stroke-width: 1.3; }",
        ".point { fill: #2b6f8f; fill-opacity: 0.82; }",
        "</style>",
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="18">Residuals vs fitted values: {model_name}</text>',
    ]

    for tick in x_ticks:
        px = sx(tick)
        parts.append(f'<line class="grid" x1="{px:.2f}" y1="{top}" x2="{px:.2f}" y2="{top + plot_h}"/>')
        parts.append(f'<line class="axis" x1="{px:.2f}" y1="{top + plot_h}" x2="{px:.2f}" y2="{top + plot_h + 5}"/>')
        parts.append(f'<text x="{px:.2f}" y="{top + plot_h + 24}" text-anchor="middle" font-size="12">{tick:.2f}</text>')

    for tick in y_ticks:
        py = sy(tick)
        parts.append(f'<line class="grid" x1="{left}" y1="{py:.2f}" x2="{left + plot_w}" y2="{py:.2f}"/>')
        parts.append(f'<line class="axis" x1="{left - 5}" y1="{py:.2f}" x2="{left}" y2="{py:.2f}"/>')
        parts.append(f'<text x="{left - 10}" y="{py + 4:.2f}" text-anchor="end" font-size="12">{tick:.2f}</text>')

    parts.extend(
        [
            f'<line class="zero" x1="{left}" y1="{zero_y:.2f}" x2="{left + plot_w}" y2="{zero_y:.2f}"/>',
            f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}"/>',
            f'<line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>',
            f'<text x="{left + plot_w / 2}" y="{height - 28}" text-anchor="middle" font-size="14">Prediction (Approval rate)</text>',
            f'<text x="22" y="{top + plot_h / 2}" text-anchor="middle" font-size="14" transform="rotate(-90 22 {top + plot_h / 2})">Prediction delta</text>',
        ]
    )

    for _, row in df.iterrows():
        px = sx(row["Prediction (Approval rate)"])
        py = sy(row["Prediction_delta"])
        country = str(row["Country"]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        parts.append(f'<circle class="point" cx="{px:.2f}" cy="{py:.2f}" r="3.2"><title>{country}</title></circle>')

    parts.append("</svg>")
    output_path.write_text("\n".join(parts), encoding="utf-8")


def plot_observed_vs_fitted(df, title, svg_path, pdf_path):
    x_col = "Prediction (Approval rate)"
    y_col = "Approval rate"
    color_col = "Applications_log10"

    required = ["Country", x_col, y_col, color_col]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"{svg_path} input is missing required columns: {missing}")

    plot_df = df.copy()
    x = pd.to_numeric(plot_df[x_col], errors="coerce")
    y = pd.to_numeric(plot_df[y_col], errors="coerce")
    color_values = pd.to_numeric(plot_df[color_col], errors="coerce")
    valid = x.notna() & y.notna()
    plot_df = plot_df.loc[valid].copy()
    x = x.loc[valid]
    y = y.loc[valid]
    color_values = color_values.loc[valid]

    green_red = LinearSegmentedColormap.from_list(
        "inz_applications_log10_green_red",
        ["#2ca25f", "#d73027"],
    )

    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    sc = ax.scatter(
        x,
        y,
        c=color_values,
        cmap=green_red,
        s=30,
        alpha=0.85,
        edgecolors="none",
    )
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label(color_col)

    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_xlim(0.0, 1.2)
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, linewidth=0.5, alpha=0.35)
    fig.tight_layout()

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(svg_path, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)


def generate_approximation_plots():
    for spec in APPROXIMATION_PLOTS.values():
        df = pd.read_csv(spec["input"])
        plot_observed_vs_fitted(
            df=df,
            title=spec["title"],
            svg_path=spec["svg"],
            pdf_path=spec["pdf"],
        )


def format_relative_residual_row(row):
    return (
        f"{row['Country']} "
        f"(rate={row['Prediction_rate']:.3f}, "
        f"delta={row['Prediction_delta']:.3f})"
    )


def relative_residual_table(direction, limit=15):
    columns = {}
    for model_name, path in PREDICTION_RATE_MODELS.items():
        df = load_prediction_rate(path)
        if direction == "positive":
            selected = df[df["Prediction_rate"] > 1].sort_values("Prediction_rate", ascending=False)
        elif direction == "negative":
            selected = df[df["Prediction_rate"] < 1].sort_values("Prediction_rate", ascending=True)
        else:
            raise ValueError(f"Unknown direction: {direction}")
        columns[model_name] = selected.head(limit).apply(format_relative_residual_row, axis=1).reset_index(drop=True)
    return pd.DataFrame(columns)


def main():
    SUPPORT_DIR.mkdir(parents=True, exist_ok=True)
    generate_approximation_plots()

    summaries = []
    for model_name, path in MODELS.items():
        df = load_prediction(path)
        summaries.append(residual_summary(model_name, df))
        plot_residuals_vs_fitted(
            model_name,
            df,
            SUPPORT_DIR / f"residuals_vs_fitted_{model_name}.svg",
        )

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(SUPPORT_DIR / "Residual_summary_by_model.csv", index=False)
    relative_residual_table("positive").to_csv(
        SUPPORT_DIR / "Relative_residuals_positive_by_model.csv",
        index=False,
    )
    relative_residual_table("negative").to_csv(
        SUPPORT_DIR / "Relative_residuals_negative_by_model.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
