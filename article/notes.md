# Notes for Article Draft

## Project Focus

This work is a statistical analysis of data combined from public datasets. The core data are Immigration New Zealand (INZ) decisions on fee-paying student visa applications for 2022-2025:

- [inz_student_visa_decisions_2022.csv](../data/original/inz_student_visa_decisions_2022.csv)
- [inz_student_visa_decisions_2023.csv](../data/original/inz_student_visa_decisions_2023.csv)
- [inz_student_visa_decisions_2024.csv](../data/original/inz_student_visa_decisions_2024.csv)
- [inz_student_visa_decisions_2025.csv](../data/original/inz_student_visa_decisions_2025.csv)

## Why Use INZ Student Visa Decision Data?

The application process for a fee-paying student visa to New Zealand requires substantial preparation. These are not spontaneous applications. Each application is submitted by a person who intends to study in New Zealand and has already completed several difficult supporting steps.

To apply for this type of visa, a person needs to:

- find an educational organisation, send documents to it, and receive approval for study;
- pay for at least one year of study or the full course price;
- receive confirmation from the educational organisation about the payment and offer of place;
- pay for medical insurance;
- pay the INZ application fee.

The application must also include:

- a history of all previous education, with supporting documents;
- a full work history, including role descriptions, activities, supervisor names, and supervisor contact details;
- explanations for gaps of more than one month in education or work history;
- a bank statement showing enough money for education and living costs in New Zealand for the full period of study;
- an explanation of the source of funds and explanations of incoming money transfers;
- medical examination documents from approved medical offices;
- travel history, including visa scans and booking confirmations for at least five years;
- confirmation of relationships with relatives, not only through marriage certificates but also through additional evidence such as rental contracts;
- confirmation of valuable ties to the home country, such as property ownership.

INZ does not give an upper estimate for application assessment time. The mean time is three weeks, but at least one known case took more than five months.

Based on the information INZ requires, it is reasonable to say that applicants genuinely intended to apply. This is not a scientific claim, but it explains why the original data are unlikely to contain records of people who decided to apply spontaneously. In all application cases, substantial preparation had to be completed before submission.

## Official INZ Sources

- 2022 offshore student visa application decisions: <https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/offshore-student-visa-application-decisions-for-2022/>
- 2023 offshore student visa application decisions: <https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/offshore-student-visa-application-decisions-for-2023/>
- 2024 overseas student visa application decisions: <https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/overseas-student-visa-application-decisions-for-2024/>
- 2025 overseas student visa application decisions: <https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/overseas-student-visa-application-decisions-for-2025/>

The original INZ datasets are stored in [data/original](../data/original/).

## Data Unification

The original INZ datasets are in different formats, so the first task is to prepare them for analysis.

The [INZ_visa_decisions_unification](../INZ_visa_decisions_unification/) directory contains the KNIME workflow for this task. The `knime2py` export created:

- [INZ_visa_decisions_unification.ipynb](../INZ_visa_decisions_unification.ipynb)
- [INZ_visa_decisions_unification.py](../INZ_visa_decisions_unification.py)

The prepared file [inz_student_visa_decisions_2022-2025.csv](../data/prepared/inz_student_visa_decisions_2022-2025.csv) contains a table of countries and total decisions for the four-year period, grouped by country.

## Combined Data

The next part of the work is [INZ_visa_decisions_combined](../INZ_visa_decisions_combined/).

Using only the decision data, we can already see patterns in the data. After adding a column with the base-10 logarithm of the total number of applications and plotting it against approval rate, the scatter plot shows countries with:

- a low number of applications and a high approval rate;
- a high number of applications and a high approval rate;
- a low number of applications and a low approval rate.

However, there are no countries with many applications and a low approval rate.

The first possible result statement can therefore be formulated as: if people from a country sent many applications, they had better chances of approval.

Figure: [applicationslog10_to_approval_rate.svg](../data/results/applicationslog10_to_approval_rate.svg)

TODO: Add statistical confirmation of this statement with a p-value.

## Additional Country-Level Data

To move further, more data are needed. Public sources provide additional country-level data. This work uses:

- [wb_countries_with_references.csv](../data/original/wb_countries_with_references.csv), with data from the World Bank;
- [who_countries_with_references.csv](../data/original/who_countries_with_references.csv), with data from WHO;
- [un_m49_regions.csv](../data/original/un_m49_regions.csv), with the division of countries into regions by the UN M49 standard.

TODO: Add tables describing the fields in these CSV files, the sources, and how the tables were collected.

The `INZ_visa_decisions_combined` workflow combines all sources into one table and prepares the data for statistical analysis. Unusable columns are removed, missing string values are set to `"Missing"`, and rows with missing numerical values are removed.

## Correlation Results

After combining the data, we can compute correlation coefficients between approval rate and other columns. The result is presented in [Combined-correlation-output.csv](../data/results/Combined-correlation-output.csv).

The table includes the following relationships:

| First column | Second column | Correlation value | p-value | Degrees of freedom |
| --- | --- | ---: | ---: | ---: |
| Approval rate | WHO_Under5_Mortality_per_1000_live_births | -0.7463912567244537 | 1.241840046867718e-30 | 163 |
| Approval rate | WHO_Maternal_Mortality_per_100000_live_births | -0.6810031760429003 | 7.970072882995464e-24 | 163 |
| Approval rate | WHO_Physician_Density_per_10000_population | 0.5518212739090577 | 1.5647218827604752e-14 | 163 |
| Approval rate | GDP_per_capita_current_USD | 0.5007404688044488 | 7.422166272261268e-12 | 163 |
| Approval rate | Life_expectancy_at_birth_years | 0.7147964432080487 | 4.1876037009030604e-27 | 163 |
| Approval rate | Internet_users_pct_population | 0.6328189562092257 | 7.624912868459913e-20 | 163 |
| Approval rate | GNI_per_capita_Atlas_current_USD | 0.5200245366165622 | 8.175162336504677e-13 | 163 |

These results show correlations between approval rate and several country-level metrics from WHO and the World Bank, with very low p-values.

The `INZ_visa_decisions_combined` workflow also adds a column with UN M49 regions for each country. The combined table also includes regional divisions from the World Bank and WHO. These regional classifications will later be used in models of approval rate and country-level metrics.

## Model Construction

The next step is the creation of a model for the combined data.

A linear regression hyperplane was created to approximate approval rate. This is an explanatory approximation, not a predictive model. The aim is not to predict future decisions, but to assess how well the independent parameters explain the dependent variable.

TODO: Add a description of the computational process: linear regression, prediction, coefficients, and metrics.

Three experiments were conducted using different country-to-region classifications:

- UN M49;
- WHO;
- World Bank.

The approximation results are stored in the `Score_*` files. Model coefficients are stored in the `Coefficients_*` files.

The best results are shown by the model with UN M49 regional divisions. This is probably because UN M49 uses a more detailed division of countries into regions, with 22 regions.

The approximation results are in [Prediction_un_m49.csv](../data/results/Prediction_un_m49.csv).

Based on these results, approval rate can be fitted by data from WHO, the World Bank, and the UN.

TODO: Add an explanation of the approximation metrics.

## Approximation Evaluation

The scatter plot [approximation_evaluation.svg](../data/results/approximation_evaluation.svg) shows the approximation result by comparing real approval rate with predicted approval rate.

If the prediction is perfect, all points should lie on the `y = x` line. If the prediction is arbitrary, the points should be scattered across the field.

In this case, most points are close to the `y = x` line, so the prediction is correct. Some points are not close to `y = x` and look like outliers.

Countries outside the region between `y = 0.8x` and `y = 1.2x` should be discussed separately. For these countries, the real approval rate is lower than 80% of the model value or higher than 120% of the model value.

TODO: Add the list of countries outside this region.

These cases are not outliers in the technical sense. They indicate that additional parameters may influence approval decisions, but this work cannot state what those parameters are. Identifying those parameters can be a topic for future research.

## Note on Multicollinearity Diagnostics

The file [Combined-correlation-output.csv](../data/results/Combined-correlation-output.csv) already shows strong pairwise correlations among several country-level development indicators. This is enough for the current article to state a limitation: the numerical predictors overlap substantially, so individual coefficients should not be overinterpreted as independent effects.

A full variance inflation factor (VIF) analysis would be a stronger multicollinearity diagnostic, especially for the full regression design matrices with categorical variables. However, for the current article this may be more detailed than necessary. The article can use the existing correlation output to explain the limitation and reserve VIF or other full design-matrix diagnostics for a later methodological extension.
