# Unemployment, Economic Growth, Inflation and FDI: Panel VAR Evidence for Central and Eastern European Union Countries

This presentation explores the dynamic relationships between unemployment, economic growth, inflation, and Foreign Direct Investment (FDI) in 11 Central and Eastern European (CEE) member countries of the European Union. We will examine how these key macroeconomic variables interact and influence each other, particularly focusing on their impact on unemployment, using a robust panel VAR approach.

---

## Context & Motivation

The Central and Eastern European countries underwent a profound transformation in the 1990s, shifting from centralized to market economies. This period was characterized by significant structural changes, often leading to high unemployment and inflation. Foreign Direct Investment (FDI) was widely regarded as a crucial catalyst for economic growth, employment generation, and successful integration into the European Union.

These economies experienced substantial FDI inflows post-1990s, but their unique economic journey also made them vulnerable to global shocks. The 2008 global economic crisis severely impacted their labor markets, and more recently, the COVID-19 pandemic presented new challenges. This study focuses on 11 CEE EU member countries (Poland, Romania, Bulgaria, Hungary, Latvia, Lithuania, Estonia, Croatia, Czech Republic, Slovenia, and Slovakia) from 2000 to 2020, aiming to provide a comprehensive understanding of these complex macroeconomic interdependencies.

---

## Methodology / Approach

To analyze these dynamic relationships, we employed a Panel Vector Autoregression (PVAR) model, which is well-suited for panel data (multiple countries over time) and accounts for endogenous interactions between variables.

Our dataset covers annual observations from 2000 to 2020 for the 11 CEE EU countries, sourced from Eurostat and the World Bank. The key variables included are:
*   **Unemployment rate** (%)
*   **GDP growth rate** (constant 2010 prices)
*   **Foreign Direct Investment** (% of GDP)
*   **Inflation** (CPI growth rate, constant 2010 prices)
*   Dummy variables for the 2008 economic crisis and the COVID-19 health crisis were also incorporated.

The analytical steps involved:
1.  **Stationarity Tests:** We first confirmed that all variables were stationary in levels using second-generation panel unit root tests (Levin, Lin & Chu; Im, Pesaran and Shin) to ensure the validity of the VAR model and avoid spurious regressions.
2.  **Optimal Lag Selection:** The appropriate number of lags for the VAR model was determined using information criteria, with the Hannan-Quinn criterion suggesting a VAR(3) model.
3.  **Granger Causality Tests:** These tests were performed to identify the direction of causal relationships between the variables.
4.  **Impulse Response Functions (IRFs):** Using Cholesky decomposition, IRFs illustrated the dynamic response of unemployment to shocks in GDP growth, inflation, and FDI over time.
5.  **Variance Decomposition Analysis:** This technique quantified the proportion of the forecast error variance of unemployment explained by shocks in the other variables.
6.  **Model Stability Tests:** We ensured the reliability of the VAR model by confirming its stability, with all inverse roots of the characteristic polynomial lying within the unit circle.

---

## Key Findings

Our panel VAR analysis revealed several important dynamic relationships among unemployment, economic growth, inflation, and FDI in CEE countries:

*   **Unidirectional Causality to Unemployment:** We found a clear one-way Granger causality from both GDP growth and inflation to the unemployment rate. This means changes in economic growth and inflation can predict changes in unemployment, but not vice-versa.
*   **Negative Unemployment Response to GDP Growth Shocks:** A positive shock to GDP growth leads to a statistically significant decrease in the unemployment rate. Specifically, a one standard deviation shock in GDP growth causes unemployment to decrease for approximately two years, with a maximum reduction of 0.2% in the second year.
*   **Positive Unemployment Response to Inflation Shocks:** Conversely, an increase in inflation generates a positive response in the unemployment rate. A one standard deviation shock to inflation leads to an increase in unemployment, peaking at 0.8% after three years, and this positive relationship persists throughout the analyzed period.
*   **Insignificant Influence of FDI on Unemployment:** A crucial finding is that Foreign Direct Investment (FDI) does not have a statistically significant influence on the unemployment rate in these CEE economies. While an initial, slight decrease in unemployment might be observed following an FDI shock, this effect is not statistically significant.
*   **Variance Decomposition Insights:** Inflation shocks account for a substantial portion of unemployment volatility, explaining 23.39% of its variation over 10 periods. GDP growth shocks contribute 5.4%, while FDI shocks explain a minor 1.63% of unemployment variation over the same period, reinforcing its limited direct impact.
*   **Model Stability:** The estimated VAR model was confirmed to be stable and correctly specified, ensuring the reliability of our impulse response functions and variance decomposition results.

---

## Evolution of Key Macroeconomic Variables in CEE Countries

To understand the context of our findings, let's first look at the historical trends of the variables in the CEE region.

![](data/documents/ssrn-5233576/images/image_1_page_6.png)
**Figure 1 — The evolution of unemployment rate in the CEE countries**
This figure presents 11 individual line charts, each showing the annual unemployment rate for one of the CEE countries from 2000 to 2020. It clearly illustrates the significant impact of major economic events, such as the global financial crisis around 2008-2010, which led to a general increase in unemployment, and the slight uptick in 2020 due to COVID-19. The diverse experiences across countries, with Estonia, Latvia, and Lithuania showing dramatic peaks post-2008, provide crucial background for understanding the study's motivation.

![](data/documents/ssrn-5233576/images/image_2_page_7.png)
**Figure 2 — The evolution of GDP growth rate in the CEE countries**
Similar to the unemployment trends, this figure displays the annual GDP growth rate for each CEE country from 2000 to 2020. It prominently features the sharp decline in GDP growth, often into negative territory, during the 2008-2009 global financial crisis, followed by recovery and another significant dip in 2020 due to the COVID-19 pandemic. This visualization is vital for establishing the economic context and trends in GDP growth, which is a key input variable in our Panel VAR model.

![](data/documents/ssrn-5233576/images/image_3_page_8.png)
**Figure 3 — The evolution of consumer price index growth (inflation) in the CEE countries (reference year 2010=100)**
This figure shows the annual inflation rate for the CEE countries over the study period. It highlights higher and more volatile inflation rates in the early 2000s, with notable spikes around the 2008-2009 crisis. Post-2009, inflation generally became more moderate, though some variations and a slight increase in 2020 are visible. This historical context of inflation is critical for understanding the economic environment and its potential influence on unemployment.

![](data/documents/ssrn-5233576/images/image_4_page_9.png)
**Figure 4 — The evolution FDI in the CEE countries**
This figure illustrates the annual Foreign Direct Investment as a percentage of GDP for each CEE country from 2000 to 2020. It reveals significant fluctuations in FDI inflows, with peaks in the mid-2000s, and instances of negative FDI indicating divestment. This visualization helps us understand the patterns of foreign investment, which was hypothesized to influence employment, despite our eventual finding of its statistically insignificant impact.

---

## Panel VAR Model Results

Before diving into the dynamic responses, we first ensured the statistical properties of our data and model.

**Table 1 — The results of panel unit root tests**
This table presents the results of panel unit root tests (Levin, Lin & Chu and Im, Pesaran and Shin) for all four variables: Unemployment rate, GDP growth rate, CPI growth rate, and FDI. The very low probability values (mostly 0.000***) indicate a strong rejection of the null hypothesis of a unit root. This is crucial as it confirms that all variables are stationary in levels, a fundamental prerequisite for applying the Panel VAR methodology and ensuring the validity of subsequent analyses.


| Unnamed: 0        | Model              |   LLC.Stat. test | LLC.Prob.   |   IPS.Stat. test | IPS.Prob.   |
|:------------------|:-------------------|-----------------:|:------------|-----------------:|:------------|
| Unemployment rate | Constant           |            -4.97 | 0.000***    |            -3.99 | 0.000***    |
| Unemployment rate | Constant and trend |            -3.93 | 0.000***    |            -3.88 | 0.000***    |
| GDP               | Constant           |            -3.66 | 0.000***    |            -3.87 | 0.000***    |
| GDP               | Constant and trend |            -3.09 | 0.001***    |            -2.77 | 0.003***    |
| nan               | Constant           |            -5    | 0.000***    |            -4.29 | 0.000***    |
| nan               | Constant and trend |            -4.86 | 0.000***    |            -3.28 | 0.001***    |
| nan               | Constant           |            -2.21 | 0.014**     |            -3.19 | 0.001***    |
| nan               | Constant and trend |            -1.63 | 0.051*      |            -2.3  | 0.011**     |



**Table 2 — Lag length criteria**
This table displays the values of three information criteria (Akaike, Schwarz, and Hannan-Quinn) for different lag lengths of the Panel VAR model. These criteria help determine the optimal number of lags to include. While different criteria suggested varying lag lengths, the study proceeded with a VAR(3) model based on the Hannan-Quinn criterion. This choice is essential for accurately capturing the dynamic relationships between variables without overfitting or underfitting the model.


|   Lag | AIC       | SC        | HQ        |
|------:|:----------|:----------|:----------|
|     0 | 23.99048  | 24.21636  | 24.08217  |
|     1 | 21.27422  | 21.80129  | 21.48817  |
|     2 | 20.86073  | 21.68898* | 21.19694  |
|     3 | 20.69976  | 21.82919  | 21.15823* |
|     4 | 20.76087  | 22.19149  | 21.34161  |
|     5 | 20.69231  | 22.42411  | 21.39531  |
|     6 | 20.55633* | 22.58931  | 21.38158  |



### Granger Causality

**Table 3 — Granger causality test**
This table presents the results of the Granger causality test, which examines whether one variable can predict another. The results clearly show that GDP growth rate and inflation rate Granger cause unemployment (Prob. 0.0000), indicating a unidirectional relationship. Crucially, FDI does not Granger cause unemployment (Prob. 0.7666), and unemployment does not Granger cause any of the other variables. This table provides direct evidence for the causal relationships, or lack thereof, between our key macroeconomic variables.


| Null Hypothesis:                                                     |    Chi-sq |   Prob. |
|:---------------------------------------------------------------------|----------:|--------:|
| GDP growth rate does not Granger Cause                               | 25.2334   |  0      |
| Unemployment rate Inflation rate does not Granger Cause Unemployment | 42.2884   |  0      |
| rate FDI does not Granger Cause Unemployment rate                    |  1.14351  |  0.7666 |
| Unemployment rate does not Granger Cause GDP                         |  3.65018  |  0.3018 |
| growth rate Unemployment rate does not Granger Cause Inflation       |  5.34779  |  0.148  |
| rate Unemployment rate does not Granger Cause FDI                    |  0.954303 |  0.8123 |



### Impulse Response Functions

![](data/documents/ssrn-5233576/images/image_5_page_11.png)
**Figure 5 — Impulse response functions**
This figure is central to our empirical findings, illustrating the dynamic effect of a one standard deviation shock from GDP growth, inflation, and FDI on the unemployment rate over 10 periods.
*   **Unemployment to GDP Growth Shock:** Unemployment responds negatively, decreasing for about two years with a maximum reduction of 0.2% in the second year, before stabilizing. This shows that economic growth helps reduce unemployment in the short to medium term.
*   **Unemployment to FDI Shock:** A shock to FDI leads to a slight, temporary decrease in unemployment for about four years. However, the confidence bands (dashed lines) indicate that this effect is **not statistically significant**, meaning we cannot confidently say FDI directly impacts unemployment.
*   **Unemployment to Inflation Shock:** An increase in inflation generates a positive response in the unemployment rate, peaking at an increase of 0.8% after three years. This positive relationship persists throughout the analyzed period, suggesting that higher inflation is associated with higher unemployment.

### Variance Decomposition

**Table 4 — Variance decomposition analysis of unemployment**
This table quantifies the proportion of the forecast error variance of the unemployment rate that is attributable to shocks from each variable over 10 periods. In the short term (period 2), inflation shocks account for 6.43% of unemployment volatility, while GDP growth shocks account for 1.03%. FDI shocks contribute only 0.15%, reinforcing its statistically insignificant impact. Over 10 periods, inflation's contribution rises to 23.39%, GDP growth's to 5.4%, and FDI's remains minor at 1.63%. This analysis highlights that inflation is a significant external driver of unemployment fluctuations, while FDI's role is very limited.


|   Period |    S.E. |   UNEMPLOYMENT |   GDP_GROWTH |   INFLATION |   FDI |
|---------:|--------:|---------------:|-------------:|------------:|------:|
|        1 | 1.16018 |         100    |         0    |        0    |  0    |
|        2 | 1.97358 |          92.39 |         1.03 |        6.43 |  0.15 |
|        3 | 2.48016 |          82.93 |         0.85 |       16.01 |  0.21 |
|        4 | 2.77564 |          78.51 |         1.74 |       19.57 |  0.17 |
|        5 | 2.95641 |          76.9  |         2.47 |       20.45 |  0.18 |
|        6 | 3.08291 |          74.98 |         3.25 |       21.41 |  0.35 |
|        7 | 3.17476 |          72.94 |         4.02 |       22.32 |  0.71 |
|        8 | 3.23604 |          71.57 |         4.6  |       22.84 |  0.99 |
|        9 | 3.27839 |          70.55 |         5.04 |       23.17 |  1.24 |
|       10 | 3.31155 |          69.58 |         5.4  |       23.39 |  1.63 |



### Model Stability

![](data/documents/ssrn-5233576/images/image_6_page_13.png)
**Figure 6 — Testing the stability of the VAR model - Unit circle**
This figure displays the inverse roots of the AR characteristic polynomial. All roots are positioned inside the unit circle, which is a crucial indicator that the estimated VAR model is stable and correctly specified. This confirms the reliability and validity of the impulse response functions and variance decomposition derived from our model.

---

## Conclusions & Policy Implications

This study provides robust panel VAR evidence on the dynamic relationships between unemployment, economic growth, inflation, and FDI in 11 CEE EU countries from 2000 to 2020.

**Core Messages:**
*   **Economic growth is a key driver for reducing unemployment:** Strong GDP growth significantly and negatively impacts unemployment, with effects lasting for about two years.
*   **Inflation exacerbates unemployment:** Higher inflation rates are consistently associated with increased unemployment, challenging traditional Phillips curve assumptions in this context.
*   **FDI's direct impact on unemployment is statistically insignificant:** Despite its perceived importance for transition economies, our findings suggest that FDI does not directly or significantly influence the unemployment rate in these CEE countries.

**Limitations:**
*   The primary limitation is the statistically insignificant impact of FDI on unemployment, suggesting that while FDI may have other benefits, it is not a direct lever for reducing unemployment in this specific group of countries during the study period.

**Policy Implications:**
*   **Prioritize policies for sustainable economic growth:** Governments in CEE countries should focus on fostering robust and stable economic growth, as this is the most effective macroeconomic tool identified for reducing unemployment.
*   **Maintain price stability:** Controlling inflation is crucial, as rising prices are shown to contribute to higher unemployment. Monetary and fiscal policies aimed at maintaining moderate and stable inflation levels are essential.
*   **Re-evaluate FDI's role in job creation:** While FDI is important for overall economic development, policymakers should not solely rely on it as a direct strategy for unemployment reduction. Other factors or conditional effects of FDI might be at play, warranting further investigation. Future research could explore how FDI might indirectly affect unemployment through other channels or under specific conditions (e.g., sector-specific FDI, institutional quality).