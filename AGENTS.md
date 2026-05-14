# AGENTS.md

This repository is a computational research workspace for a journal article about Immigration New Zealand student visa decisions. Treat it as a scientific project that includes data, KNIME workflows, Python support code, statistical outputs, manuscript drafts, notes, figures, and submission material.

## Core Purpose

Help produce a defensible scientific article. The work should support:

- reproducible data preparation;
- transparent statistical analysis;
- cautious interpretation of empirical results;
- clear documentation of data provenance and limitations;
- disciplined manuscript composition for journal submission.

The final output is a journal article, but the article must be grounded in the repository's research assets.

## Working Principles

- Treat data, workflows, code, and writing as one research record.
- Prefer narrow, testable empirical claims over broad commentary.
- Make the research question visible early in drafts.
- Preserve source data and make derived data reproducible.
- Distinguish raw data, cleaned data, joined data, and model outputs.
- Distinguish descriptive, predictive, and causal claims.
- Verify computation paths before strengthening article language.
- Record limitations as part of the science, not as an afterthought.
- Preserve the author's direct, serious voice.
- Remove filler, vague framing, hype, and corporate-blog phrasing.

## Repository Conventions

Expected organization:

```text
data/
  original/     Source data and reference tables. Do not edit manually.
  prepared/     Cleaned, unified, or joined datasets.
  results/      Analysis outputs, scores, coefficients, predictions, and export tables.

INZ_visa_decisions_unification/
  KNIME workflow for unifying yearly INZ student visa decision data.

INZ_visa_decisions_combined/
  KNIME workflow for joining visa decision data with reference classifications.

INZ_visa_decisions_model/
  KNIME workflow for modeling, scoring, and prediction outputs.

src/
  Python support code for cleaning, validation, automation, or reproducibility.
```

All project-relevant files should live here. Manuscript work is a LaTeX project under `article/`. Treat `article/article.tex` as the active manuscript source, `article/bibliography.bib` as the bibliography source, and `article/imgs/` or `article/figures/` as the place for manuscript figures. `article/article.txt` may be used as notes or legacy drafting material, but do not treat it as the source of record when `article/article.tex` exists.

```text
article/
  article.tex
  bibliography.bib
  notes.md
  imgs/
  figures/
  tables/
```

If adding computational notebooks or scripts, place them where their role is obvious and document the inputs and outputs.

## Data Handling Standards

- Do not manually edit files in `data/original/`.
- Put generated datasets in `data/prepared/` or `data/results/`.
- Keep external reference tables with enough provenance to identify source, download date, and meaning.
- Document joins, keys, filters, exclusions, recoding, and aggregation.
- Check row counts before and after joins or filters.
- Report unmatched countries, missing values, and classification conflicts.
- Use structured tools for CSV/data transformations where possible; avoid fragile ad hoc edits.
- Be careful with names that look similar but represent different quantities, such as counts, rates, scores, predictions, and coefficients.

## KNIME Workflow Standards

The repository currently contains KNIME workflow directories. Preserve workflow integrity:

- `workflow.knime` belongs at the workflow root.
- node directories should preserve their `settings.xml`.
- generated or temporary KNIME artifacts may be cleaned only when the workflow remains reusable.
- do not rename KNIME node directories casually; names may encode workflow structure.
- when changing a workflow, document what input files it expects and what outputs it writes.

The Python cleaner in `src/clean/cli.py` is support tooling for cleaning KNIME workflow exports. Treat it as project maintenance code, not as part of the statistical model unless it later becomes part of the analysis pipeline.

## Statistical Analysis Standards

Before using an output as evidence, answer:

- What exact input files produced this result?
- What transformations were applied?
- What is the unit of observation?
- Is the quantity a count, proportion, rate, prediction, coefficient, or score?
- What model was used and why?
- Is the result descriptive, predictive, or causal?
- What assumptions does the model require?
- What uncertainty, validation result, or robustness check is available?
- What missingness, unmatched joins, or classification choices could affect the result?

Avoid causal claims unless the design actually supports causal inference. Most visa decision analysis will likely support descriptive or predictive claims unless a stronger identification strategy is added.

## Scientific Article Structure

Use this structure unless a target journal requires another format:

1. Title
2. Abstract
3. Introduction and research question
4. Data
5. Methods
6. Results
7. Robustness or sensitivity checks
8. Discussion
9. Limitations
10. Conclusion
11. References
12. Appendices or supplementary material

The article should do three things:

- identify a specific empirical problem;
- show a reproducible analysis path;
- state findings with proper limits.

## Section Guidance

### Title

Use a specific scientific title. It should name the empirical subject and, where useful, the method or comparison.

### Abstract

Include the research question, data period, data source, method, main result, and principal limitation. Do not write a promotional abstract.

### Introduction

Start with the practical or scientific problem. State the research question early. Avoid broad background unless it directly explains why this analysis is needed.

### Data

Describe:

- data source;
- time period;
- unit of observation;
- variables used;
- exclusions and missingness;
- reference classifications such as World Bank, WHO, and UN M49 regions;
- known limits in source data.

### Methods

Describe the data pipeline and statistical model clearly enough that another researcher could reproduce it. Include software and workflow information when relevant.

### Results

Separate descriptive statistics from model outputs. Avoid interpreting coefficients, prediction scores, or correlations without naming the model and scale.

### Robustness / Sensitivity

Check whether the main finding changes under different region classifications, filters, transformations, or model specifications.

### Discussion

Interpret what the results imply and what they do not imply. Keep policy or institutional interpretation proportionate to the evidence.

### Limitations

Address omitted variables, aggregation, data quality, model assumptions, regional classification choices, and causal limits.

### Conclusion

Do not end with "In conclusion." End with the empirical contribution and the next question the work makes visible.

## Writing Style

- Be direct, serious, and practical.
- Prefer precise claims over broad claims.
- Keep paragraphs focused on one point.
- Use tables, figures, and concrete examples where they clarify the analysis.
- Define technical terms only when needed.
- Do not add history unless it directly serves the research question.
- Avoid hype, inevitability language, and decorative phrasing.
- Do not overstate what the data can show.

## Revision Checklist

Before considering a manuscript section ready, check:

- Is the research question clear?
- Does the claim match the evidence?
- Can the result be traced to data, workflow, code, or notes in the repository?
- Are data preparation steps documented?
- Are variables and units of observation defined?
- Are limitations and uncertainty visible?
- Are descriptive, predictive, and causal statements separated?
- Is there at least one concrete table, figure, or example supporting the claim?
- Would another researcher understand how to reproduce the result?

## Agent Behavior

When assisting in this repository:

- inspect the actual files before assuming the project structure;
- preserve original data and user-authored changes;
- make narrow edits that improve reproducibility, analysis clarity, or manuscript quality;
- when editing writing, strengthen scientific precision rather than making it sound generic;
- when editing code or workflows, explain how the change affects the research pipeline;
- when uncertain about a result, flag the uncertainty instead of polishing it away.
