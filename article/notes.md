This work is about statistical analysis of data combined from public datasets.
Core data are from INZ decisions for fee paying student visas statistics for years 2022-2025.
(../data/original/inz_student_visa_decisions_2022.csv)
(../data/original/inz_student_visa_decisions_2023.csv)
(../data/original/inz_student_visa_decisions_2024.csv) 
(../data/original/inz_student_visa_decisions_2025.csv)

Why do we used data from INZ?
As we know the process of the application to fee paying student visa to NZ, there are not spontaneus applications here. All application was submitted with intentions to study in NZ with many difficult supporting activity. To apply for this type of visa one needs:
- Find an educational organization, sent his document to it, get an approve for education
- Pay for at least 1 year of study or full price for the couse
- Recieve confirmation from the educattional organization about the payment and offer of place.
- Pay for a medical insurance
- Pay INZ fee

In the application it also should be mentioned:
- History of all previous educations with confirmaition documents
- All work history with description of role, activities, name of superviser and a contacts of a superviser. (Yes if there are 10 yers work history, with several places of work, for each place the supervicer name and his contacts should be mentioned. And the fields are obligatory).
- If there were gaps in the history of education or work more than 1 month they should be described.
- A bank statement with money enough for education and life in NZ for the entire period of the education. (yes for bachelor degree, for example, it is money for 3 years)
- Explaination about the source of money. And explaination of money transfers for all incoming transactions. As you may see it can be relatevly large amount of money so it should be obvoius for an officer that the money are from legal source).
- Medical examination documents from UN medical offices.
- History of travel with scans of visas and booking confirmatioin for at least 5 years.
- Confirmation of reletionship with relatives. Not only marige cirtificate, but in addition contracts of rent for both persons or like it.
- Confirmation that you have somethong valuable like an apartment in your home country.

INZ don't give upper estimation of the application assessment. The mean time is 3 weeks, but we know at least one case with more than 5 months assessment. 

So, on base of the information INZ requires we can state that anyone who applied really wanted to do it. It is not scientific statement, but explains that original data don't contain recourds about people who decided to apply spontaneusly. In all application cases hard preparations should be done before it. 

Official INZ links:

2022 offshore student visa application decisions: https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/offshore-student-visa-application-decisions-for-2022/
2023 offshore student visa application decisions: https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/offshore-student-visa-application-decisions-for-2023/
2024 overseas student visa application decisions: https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/overseas-student-visa-application-decisions-for-2024/
2025 overseas student visa application decisions: https://www.immigration.govt.nz/study/for-education-providers/data-and-processing-times-for-international-student-visas/offshore-student-visa-application-decision-data/overseas-student-visa-application-decisions-for-2025/

Original datasets from INZ are in data/original

These datasets are in different formates. So the first task is to prepare the data for analysis. 
INZ_visa_decisions_unification directory contains KNIME workflow for this task.
For this workflow knime2py created files 
INZ_visa_decisions_unification.ipynb
INZ_visa_decisions_unification.py
(../data/prepared/inz_student_visa_decisions_2022-2025.csv) contains the table with countries and total decisions for 4 years (grouped by country).

Next part is INZ_visa_decisions_combined
Having only data about decisions we already can have insites about the data. Adding a column with log10 of total number of application and print them as Scatter plot, we can see that theare are countries with low number of applications with high value of appruval, high number of applications and high level of approval, with low level of application and low level of applical, but no countries with many applications and low level of approval.
So the first result statement of the work can be formulate as: if people from a country sent many requests, they got better chanses of approval.  
data/results/applicationslog10_to_approval_rate.svg

(here I need statistical confirmation of this statement with p value)

To move furver we need more data. In public sources we can find additional data for countries. This work contains files
data/original/wb_countries_with_references.csv
with data from World bank,
data/original/who_countries_with_references.csv
with data from WHO, and
data/original/un_m49_regions.csv
with division of countries to regions by standard UN M49 method.

(Here we need tables with description of fileds from .csv files and description of sources and how the tables were collected).

INZ_visa_decisions_combined combines all sources to one table and prepares data for statistical analyses. Unusable columns removed, missed values strings set to "Missed" and rows with missed numerical values removed.

Having the data combined we can compute correlation coefficients between Appraval and other columns. The result of this copputation is presented in 
data/results/Combined-correlation-output.csv

In this table we see
"First column name","Second column name","Correlation value","p value","Degrees of freedom"
"Approval rate","WHO_Under5_Mortality_per_1000_live_births",-0.7463912567244537,1.241840046867718e-30,163
"Approval rate","WHO_Maternal_Mortality_per_100000_live_births",-0.6810031760429003,7.970072882995464e-24,163
"Approval rate","WHO_Physician_Density_per_10000_population",0.5518212739090577,1.5647218827604752e-14,163
"Approval rate","GDP_per_capita_current_USD",0.5007404688044488,7.422166272261268e-12,163
"Approval rate","Life_expectancy_at_birth_years",0.7147964432080487,4.1876037009030604e-27,163
"Approval rate","Internet_users_pct_population",0.6328189562092257,7.624912868459913e-20,163
"Approval rate","GNI_per_capita_Atlas_current_USD",0.5200245366165622,8.175162336504677e-13,163

So there are correlation between approval raning and several county metrics from WHO and WB with very low p-value.

In addition INZ_visa_decisions_combined adds a column with UN M49 regions for each country.
There are two disision to regions from WB and WHO in this table. Later we will use them for approval rating to country metrics model.

Next step of the work is creation of model for the combined data. 
Linear regerssion hyper plane was created to approximate Approvel rating.
It is axplanatory approximation, not a model for prediction. The aim is not to predict, but to find how good are independent parameters in expaination of the dependent one. 

(here I need description of the computational process. Linear Regression, Prediction, coefficients and metrics)

Three experiments were conducted for different division of counties to regions: UN M49, WHO, and WB.
The results of approximations are in 
Score_* files
Coefficients of models are in Coefficients_* files

The best results shows the model with UN M49 divisions to regions. Probably because it uses more detailed division of countires to regions (22 regions).

Results of approximation are in data/results/Prediction_un_m49.csv
On base of the results we can state that Approvel rating can be fitted by data from WHO, WB, and UN. 

(here I need explaination about metrics of approximation)

Scatter plot data/results/approximation_evaluation.svg shows the result of approximation with real Approval to Predicted approval. 
If the prediction is perfect all points should be on y=x line. If the prediction is arbitrary, all dots should be scattered across the filed. 
In out case most of dots are close to line y=x so the prediction is correct.
Some dots  are not close to y=x and looks like outliers.
Let's separately discuss counties which are out of y=0.8x and y=1.2x region.
So their real Approval is lower than 80% of the model's or higher than 120% of the model's.  
(here I need countries list which are out).
They are not outliers in tichnical meaning. And it means that should be more parameters about which we can state nothing here which influence the approvel decisions. Finding of these parameters can be the topic of the next reseach.


