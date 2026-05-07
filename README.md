# INZ Visa Decisions Research Workspace

This repository is a computational research workspace for studying Immigration New Zealand student visa decision data. It contains data, KNIME workflows, Python support code, intermediate outputs, model results, notes, and article drafts needed to develop a journal article.

The final goal is not a blog post or a general essay. The final goal is a defensible scientific article: a clear research question, reproducible data preparation, transparent statistical analysis, cautious interpretation, and a manuscript suitable for submission to an academic journal.

## Research Purpose

The project should answer a narrow empirical question about INZ student visa decisions. Every dataset, workflow, script, result table, figure, and manuscript section should support that question directly.

The working research direction is:

- collect and preserve INZ student visa decision data for 2022-2025;
- unify yearly decision data into a consistent analytical dataset;
- join visa decision data with country and region classifications;
- evaluate patterns in decision outcomes across region systems;
- test statistical relationships using reproducible models;
- report findings with appropriate limits and uncertainty.

Do not treat current files as final truth. Treat them as the current state of the research pipeline. Correct assumptions, names, methods, and article framing as the project develops.

## Repository Layout

```text
data/
  original/     Source data and reference tables preserved as inputs.
  prepared/     Cleaned or joined datasets produced from source inputs.
  results/      Model outputs, scores, coefficients, predictions, and analysis exports.

INZ_visa_decisions_unification/
  KNIME workflow for combining yearly INZ decision data.

INZ_visa_decisions_combined/
  KNIME workflow for joining INZ decisions with region/classification data.

INZ_visa_decisions_model/
  KNIME workflow for statistical modeling and prediction outputs.

src/
  Python support code for project maintenance and reproducibility.

README.md
  Human-facing project guide.

AGENTS.md
  Durable instructions for future AI and coding/writing agents.
```

All files that are part of the research should live in this repository: source data snapshots, derived data, workflow definitions, scripts, notebooks if added later, figures, tables, manuscript drafts, reviewer notes, and submission material.

## Reproducibility Rules

- Preserve original data files. Do not edit files in `data/original/` manually.
- Put generated datasets in `data/prepared/` or `data/results/`.
- Make each transformation reproducible through KNIME, Python, or documented manual steps.
- Keep workflow exports clean enough to review and move between machines.
- Record where each external dataset came from, when it was downloaded, and what columns were used.
- Distinguish descriptive results from model-based claims.
- Do not overwrite result files without understanding which workflow or script produced them.

## Current Assets

Current data inputs include yearly INZ student visa decision CSV files for 2022, 2023, 2024, and 2025, plus reference tables for World Bank regions, WHO regions, and UN M49 regions.

Current prepared outputs include:

- unified INZ student visa decisions for 2022-2025;
- combined INZ decision data with region classifications.

Current model outputs include:

- coefficient tables;
- model scores;
- prediction tables;
- prediction-rate tables.

These outputs should be checked before they are used as evidence in the article. A result is not article-ready until the input data, transformation path, model specification, and interpretation are all clear.

## Scientific Article Structure

Use a journal-article structure unless a target journal requires a different format.

1. **Title**
   - State the empirical subject and method or comparison clearly.

2. **Abstract**
   - Include the research question, data period, method, main result, and limitation.

3. **Introduction**
   - Explain why student visa decision patterns matter.
   - State the research question early.
   - Avoid broad immigration commentary unless it directly motivates the empirical analysis.

4. **Data**
   - Identify INZ decision data and all region/reference tables.
   - Describe units of analysis, time period, variables, exclusions, and missingness.

5. **Methods**
   - Describe data cleaning, joins, statistical models, validation approach, and software.
   - Explain why each regional classification is used.

6. **Results**
   - Separate descriptive findings from model estimates.
   - Report effect sizes, uncertainty where available, and model performance.

7. **Robustness / Sensitivity**
   - Test whether findings depend on regional classification, exclusions, transformations, or model specification.

8. **Discussion**
   - Interpret findings cautiously.
   - Connect results to the practical question without claiming more than the analysis supports.

9. **Limitations**
   - Address data quality, aggregation, omitted variables, causal limits, and classification choices.

10. **Conclusion**
    - State the main empirical contribution and what future work should verify.

## Analysis Standards

Before using a result in the manuscript, check:

- What exact input files produced it?
- What transformations were applied?
- What is the unit of observation?
- Are rates, counts, and proportions clearly distinguished?
- Are region classifications mutually consistent or intentionally different?
- Are missing countries or unmatched joins documented?
- Is the model descriptive, predictive, or causal?
- Does the text avoid causal language unless the design supports it?
- Can another researcher reproduce the table or figure?

## Writing Standards

The writing should be direct, serious, and scientific.

- Make the research question visible early.
- Prefer narrow, testable claims over broad political or policy claims.
- Report uncertainty and limitations plainly.
- Use concrete tables, figures, and examples instead of assertion.
- Avoid corporate-blog phrasing, hype, and decorative language.
- Do not use results as evidence until the computation path is verified.
- Keep the reader oriented: data, method, result, implication.

## Practical Workflow

1. Preserve source data in `data/original/`.
2. Build or revise the data pipeline in KNIME and/or Python.
3. Export prepared datasets to `data/prepared/`.
4. Run statistical analysis and export outputs to `data/results/`.
5. Inspect results for errors, missing joins, and unstable claims.
6. Draft article sections from verified outputs.
7. Record limitations and robustness checks while writing, not after.

The article should emerge from the research record. If the article says something, the repository should contain the data, workflow, code, or note that justifies it.
