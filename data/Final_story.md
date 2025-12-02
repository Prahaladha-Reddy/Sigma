# Slide 1: Rethinking the Trinity: A Global Analysis of Inflation, Unemployment, and Interest Rates

Classic economic models, such as the Phillips Curve, provide a foundational framework for macroeconomic policy. However, recent global data suggests these textbook relationships are under strain.

This analysis challenges the conventional wisdom by examining empirical data from the United States and 11 Central and Eastern European (CEE) countries. Our objective is to determine if these long-held theories hold, or if a new economic paradigm is emerging.

---

# Slide 2: The US Case Study: Initial Investigation

We begin with the United States, the world's largest economy. The Phillips Curve posits a stable, inverse relationship between inflation and unemployment. A visual inspection of the long-term data, however, reveals an inconsistent and noisy signal. While some periods hint at the expected trade-off, the overall pattern is far from clear.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell16_out1.png)


*Caption: A visual comparison of US inflation and unemployment trends. Note the lack of a consistent inverse relationship across the entire timeframe, suggesting the influence of other structural factors.*

---

# Slide 3: Deconstructing the Phillips Curve by Decade

When we disaggregate the data by decade, the theoretical Phillips Curve breaks down entirely. The relationship between inflation and unemployment is not stable; instead, it appears to be regime-dependent, shifting significantly from one decade to the next. This structural instability challenges its reliability as a predictive tool.
![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell5_out0.png)


*Caption: Unemployment vs. Inflation, colored by decade. The scattered nature of the plot indicates the absence of a strong, persistent inverse relationship over the long term.*

---

# Slide 4: Quantitative Analysis: No Significant Linear Relationship

Visual intuition is confirmed by quantitative tests. A Pearson's correlation coefficient is calculated to be near zero (0.17 in one analysis, 0.000 in another), indicating no statistically significant linear relationship between US inflation and unemployment.

To account for potential time lags, Dynamic Time Warping (DTW) was applied. The high DTW distance further supports the conclusion of a weak mathematical connection.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell25_out1.png)


*Caption: The DTW warping path shows significant deviation from a linear relationship. The distance of 100.27 confirms a poor fit between the two time series.*

---

# Slide 5: The Inflation-Interest Rate Dynamic

We next examine the relationship between inflation and interest rates. Economic theory suggests a direct link, as lenders demand higher nominal rates to offset inflation. In the US, this relationship was pronounced before 2000 but has become more complex, heavily influenced by central bank interventions like quantitative easing.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell45_out1.png)


*Caption: DTW path for US Real Interest Rate and Inflation. While a visual correlation exists in earlier periods, the relationship has been increasingly mediated by policy responses to crises since 2000.*

---

# Slide 6: Isolating the Signal: Correlation Matrix

A correlation matrix provides a clearer quantitative signal. The data reveals a moderate negative correlation (-0.54) between the inflation rate and the *real* interest rate.

This is an expected economic relationship: higher-than-anticipated inflation erodes the real, inflation-adjusted returns on lending, resulting in a lower real interest rate. This confirms that while policy complicates the nominal relationship, the underlying economic logic holds.
![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell8_out0.png)


*Caption: Correlation heatmap of key US economic variables. The key signal is the -0.54 correlation between Inflation and Real Interest Rate, confirming a core economic principle.*

---

# Slide 7: A Contrasting View: The CEE Region

Shifting our analysis to 11 Central and Eastern European countries (2000-2020) reveals a starkly different economic environment. These transitioning economies exhibit significant volatility shaped by EU integration, global crises, and unique post-Soviet legacies. This provides a natural experiment to test our assumptions in a different context.
![](data/documents/ssrn-5233576/images/image_1_page_6.png)


*Caption: The evolution of the unemployment rate in CEE countries. Note the high volatility and the structural break corresponding with the 2008 global financial crisis.*

---

# Slide 8: The Analytical Engine: Panel VAR and Causality

To analyze the CEE data, we employ a Panel Vector Autoregression (PVAR) model, a robust method for examining dynamic interrelationships in panel data.

Granger causality tests are used to determine predictive relationships. The results are unambiguous: GDP growth and inflation have a unidirectional causal effect on unemployment. Unemployment, however, does not Granger-cause these variables.

| Null Hypothesis: | Chi-sq | Prob. |
| :--- | ---: | ---: |
| GDP growth rate does not Granger Cause Unemployment rate | 25.2334 | **0.000** |
| Inflation rate does not Granger Cause Unemployment rate | 42.2884 | **0.000** |
| Unemployment rate does not Granger Cause GDP growth rate | 3.65018 | 0.3018 |
| Unemployment rate does not Granger Cause Inflation rate | 5.34779 | 0.1480 |

*Caption: Granger causality test results. The statistically significant p-values (Prob. < 0.05) show that GDP and Inflation are leading indicators for unemployment in the CEE region.*

---

# Slide 9: The "Aha" Insight: An Inverted Phillips Curve

The most critical finding from the CEE analysis directly contradicts traditional theory. An inflationary shock leads to a *positive* and persistent increase in the unemployment rate.

This suggests a stagflationary dynamic where rising prices are associated with a weaker, not stronger, labor market. This is the opposite of the relationship predicted by the Phillips Curve.
![](data/documents/ssrn-5233576/images/image_5_page_11.png)


*Caption: Impulse Response Functions from the PVAR model. Note the positive and statistically significant response of unemployment to a one-standard-deviation shock in inflation.*

---

# Slide 10: Quantifying the Impact: Variance Decomposition

To measure the magnitude of this effect, we use variance decomposition. This technique isolates how much of the future variance in unemployment can be explained by shocks to other variables.

The analysis reveals that inflation is a primary driver of unemployment volatility, explaining over 23% of its variation over a 10-period horizon. This confirms that the stagflationary effect is not only statistically significant but also economically substantial.

| Period | UNEMPLOYMENT | GDP_GROWTH | INFLATION | FDI |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 92.39 | 1.03 | 6.43 | 0.15 |
| 5 | 76.90 | 2.47 | 20.45 | 0.18 |
| 10 | 69.58 | 5.40 | **23.39** | 1.63 |

*Caption: Variance decomposition of unemployment. The contribution of inflation (highlighted) grows over time, becoming a dominant factor in explaining unemployment fluctuations.*

---

# Slide 11: The Unifying Principle: Economic Growth Drives Employment

While the inflation-unemployment relationship is context-dependent, the CEE analysis confirms a more universal economic law.

A positive shock to GDP growth leads to a statistically significant decrease in the unemployment rate. This aligns with Okun's Law and demonstrates that regardless of regional specifics, sustainable economic growth remains the most powerful and reliable lever for improving labor market outcomes.

---

# Slide 12: A Note on Heterogeneity: The Case of Japan

Further analysis underscores the importance of local context. Japan, with its unique history of persistent low inflation and deflation, shows an even weaker relationship between inflation and unemployment than the US.

The DTW distance of 191.95 is nearly double that of the US, indicating a near-total decoupling of these two variables in Japan's modern economy. This reinforces that a "one-size-fits-all" macroeconomic model is inadequate.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell30_out1.png)


*Caption: DTW warping path for Japan. The extreme distance between the series highlights a unique economic reality where inflation and unemployment move almost independently.*

---

# Slide 13: The Role of Foreign Investment

A common hypothesis, particularly for developing economies, is that Foreign Direct Investment (FDI) is a primary driver of job creation.

However, the CEE analysis finds no statistically significant causal link from FDI to unemployment. While FDI may boost productivity and technology transfer, the data shows it is not a direct or reliable tool for reducing unemployment in this regional context. This challenges a widely held policy assumption.

---

# Slide 14: Synthesis & Strategic Implications

Our multi-regional analysis reveals that simple macroeconomic models are no longer sufficient.

*   **The Phillips Curve is unreliable.** The inflation-unemployment relationship is weak in the US and inverted in the CEE, making it a poor guide for policy.
*   **Economic growth is the key.** Fostering GDP growth is the most robust strategy for reducing unemployment across different economic systems.
*   **Context is critical.** Regional dynamics, from CEE's transition to Japan's deflationary history, fundamentally alter macroeconomic relationships.
*   **Inflation is not benign.** In the CEE context, inflation actively harms employment, underscoring the critical importance of price stability.

---

# Slide 15: Q&A

Thank you.