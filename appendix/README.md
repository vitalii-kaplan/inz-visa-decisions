# Supplementary Appendix

This directory contains the standalone supplementary appendix for:

> Vitalii Kaplan, “Modelling New Zealand Student Visa Approval Rates with
> Country-Level Indicators.”

## Files

- `appendix.tex` — LaTeX source.
- `appendix.pdf` — publication-ready rendered appendix.

The source expects the article bibliography at `../article/bibliography.bib`.

## Build

From the repository root:

```sh
cd appendix
latexmk -pdf -interaction=nonstopmode -halt-on-error appendix.tex
```

Compile the appendix before compiling `article/article.tex` when the main
article imports appendix labels through `xr`.

## Main article integration

In `article/article.tex`, import the appendix labels with:

```tex
\usepackage{xr}
\externaldocument[appendix-]{../appendix/appendix}
```

Reference an appendix label by adding the import prefix, for example:

```tex
Appendix~\ref{appendix-app:student-visa-preparation}
Appendix Table~\ref{appendix-tab:appendix-excluded-countries}
```

Add this entry to `article/bibliography.bib`:

```bibtex
@misc{KaplanINZAppendix,
  author = {Kaplan, Vitalii},
  title = {Supplementary Appendix to ``Modelling New Zealand Student Visa Approval Rates with Country-Level Indicators''},
  howpublished = {GitHub repository},
  year = {2026},
  note = {Supplementary appendix},
  url = {https://github.com/vitalii-kaplan/inz-visa-decisions/blob/main/appendix/appendix.pdf}
}
```

The public PDF URL is:

<https://github.com/vitalii-kaplan/inz-visa-decisions/blob/main/appendix/appendix.pdf>
