Of course. Here is an enriched and expanded presentation that synthesizes the provided analyses into a comprehensive narrative, incorporating additional context, real-world applications, and future-looking perspectives.

# Rethinking the Trinity: A Global Analysis of Inflation, Unemployment, and Interest Rates

## Introduction: Beyond the Textbook

Classic economic theories provide foundational models for understanding the interplay between inflation, unemployment, and interest rates. The Phillips Curve suggests a trade-off between inflation and unemployment, while other principles propose a direct link between inflation and interest rates. However, as one analyst noted, these theories often represent just the "tip of the iceberg."

This presentation synthesizes multiple data-driven analyses to challenge these textbook models. We will explore whether these conventional relationships hold true against real-world data from the United States, Japan, and 11 Central and Eastern European (CEE) countries. By examining different economic contexts and employing various analytical techniques, we aim to uncover the complex, dynamic, and often surprising nature of these critical macroeconomic variables.

---

## Section 1: The US Case Study - A Faltering Phillips Curve?

The relationship between inflation and unemployment, known as the Phillips Curve, has been a cornerstone of macroeconomic policy for decades. The theory posits an inverse relationship: as unemployment falls, inflation should rise, and vice-versa. However, an examination of US data from recent decades tells a more complicated story.

### Visualizing the Long-Term Trends

Looking at the historical paths of inflation and unemployment in the United States, the relationship is not immediately obvious. Certain periods appear to show an inverse relationship, while others do not.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell12_out1.png)

**Figure 1 — Inflation trend over the years in the United States**
This line plot illustrates the annual consumer price inflation in the United States, showing significant fluctuations, including peaks in the 1970s and early 1980s, and a more stable period thereafter.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell14_out1.png)

**Figure 2 — Unemployment trend over the years in the United States**
This plot displays the total unemployment rate in the United States, revealing periods of high unemployment, such as in the early 1980s and during the Great Recession.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell16_out1.png)

**Figure 3 — Unemployment and Inflation trend over the years in the United States**
This combined line plot allows for a visual comparison of inflation and unemployment trends in the US. While some inverse movement is suggested, it is not consistently clear.

### A Scattered Relationship Across Decades

When plotting unemployment against inflation, the theoretical curve appears to break down. The relationship is highly context-dependent, with different decades showing entirely different patterns.
![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell5_out0.png)

**Figure 4 — Phillips Curve: Unemployment Rate vs. Inflation Rate by Decade**
This scatter plot illustrates the relationship between the Unemployment Rate and the Inflation Rate in the US, with points colored by decade. It shows that the classic inverse Phillips Curve relationship is not consistently strong across all decades, with points appearing scattered overall. While some decades like the 1990s and 2010s show periods of low inflation and low unemployment, a clear long-term inverse trend is not evident, suggesting the relationship has evolved over time.

### Quantifying a Weak Connection

Quantitative analysis confirms this visual intuition. Across multiple studies, the linear relationship between US inflation and unemployment is found to be exceptionally weak.

*   One analysis calculated a **Pearson's correlation coefficient of approximately 0.000**, indicating no significant linear relationship.
*   A separate analysis found a very weak positive correlation of **0.17**.

To account for potential time lags, Dynamic Time Warping (DTW) was also applied. The resulting warping path further confirms the lack of a strong mathematical connection.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell25_out1.png)

**Figure 5 — DTW Warping Path for US Inflation and Unemployment**
This visualization shows the warping path between US inflation and unemployment time series. The DTW distance of **100.27** indicates that despite theoretical inverse relationships, a strong mathematical connection with potential delays is not evident in the data.

### Industry Perspective: Why Has the Phillips Curve Flattened?

The weakening of the Phillips Curve is a widely discussed topic among economists and policymakers. Several factors are believed to contribute to this trend:
*   **Anchored Inflation Expectations:** Decades of credible central banking have led the public and businesses to expect low and stable inflation. This prevents a drop in unemployment from triggering a sharp rise in wage and price demands.
*   **Globalization:** The integration of global supply chains and labor markets has put downward pressure on domestic wages and prices, even in a tight labor market.
*   **Decline in Unionization:** A lower share of the workforce is represented by unions, reducing workers' collective bargaining power to demand higher wages when unemployment is low.
*   **E-commerce and Price Transparency:** The rise of online retail has made it easier for consumers to compare prices, increasing competition and making it harder for firms to pass on higher costs.

---

## Section 2: The Complex Dance of Inflation and Interest Rates

Economic theory also suggests a direct relationship between inflation and interest rates. To protect their returns from being eroded by inflation, lenders demand higher nominal interest rates. Let's examine this relationship in the US.

### A Relationship Shaped by Crisis

Visual analysis of US real interest rates and inflation reveals a connection that is heavily influenced by major economic events, particularly before the 21st century.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell41_out1.png)

**Figure 6 — Real Interest Rate trend over the years in the United States**
This plot shows the real interest rate in the US, highlighting a significant increase in the late 1970s and early 1980s, followed by a general decline and periods of volatility.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell42_out1.png)

**Figure 7 — Inflation trend over the years in the United States**
Re-presenting the US inflation trend, this figure is shown again to facilitate direct comparison with the interest rate trend, particularly noting the co-movement during the 1970s and 1980s.

The relationship becomes more complex after 2000, influenced by the dot-com bubble, the 2008 Great Financial Crisis, and subsequent periods of quantitative easing.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell45_out1.png)

**Figure 8 — DTW Warping Path for US Real Interest Rate and Inflation**
The DTW distance for US real interest rates and inflation is **100.27**. While a visual correlation is apparent before the 2000s, the relationship becomes more complex afterward, influenced by major economic events.

### The Correlation View

A correlation matrix provides a clearer quantitative picture. The analysis reveals a moderate negative correlation between inflation and *real* interest rates. This aligns with economic logic: when inflation rises unexpectedly, it erodes the real (inflation-adjusted) return on existing loans, leading to a lower real interest rate.
![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell8_out0.png)

**Figure 9 — Correlation Matrix of Key Economic Variables (US)**
This heatmap displays the Pearson correlation coefficients between the Unemployment Rate, Inflation Rate, and Real Interest Rate. It quantitatively confirms the weak positive correlation (0.17) between Unemployment and Inflation, and a negligible negative correlation (-0.08) between Unemployment and Real Interest Rate. A more substantial moderate negative correlation (-0.54) is observed between Inflation Rate and Real Interest Rate, an expected economic relationship where higher inflation tends to erode real returns.

### Real-World Application: The Role of Central Banks

The data reflects the powerful influence of central bank policy. The high interest rates of the early 1980s were not just a market reaction but a deliberate policy by the Federal Reserve under Paul Volcker to combat runaway inflation. Conversely, the near-zero interest rates following the 2008 crisis were a policy tool to stimulate the economy. This demonstrates that the relationship is not purely mechanical but is actively managed by monetary authorities.

---

## Section 3: A Different Story - Evidence from Central & Eastern Europe

Shifting our focus to the 11 Central and Eastern European (CEE) EU member countries from 2000 to 2020, we uncover a starkly different set of economic dynamics, particularly regarding the impact of inflation. These nations, having transitioned from centralized to market economies, faced unique challenges and opportunities.

### The Economic Landscape of the CEE Region

The evolution of key macroeconomic variables in the CEE countries shows significant volatility, shaped by their transition, EU integration, the 2008 global crisis, and the COVID-19 pandemic.
![](data/documents/ssrn-5233576/images/image_1_page_6.png)

**Figure 10 — The evolution of unemployment rate in the CEE countries**
![](data/documents/ssrn-5233576/images/image_2_page_7.png)

**Figure 11 — The evolution of GDP growth rate in the CEE countries**
![](data/documents/ssrn-5233576/images/image_3_page_8.png)

**Figure 12 — The evolution of consumer price index growth (inflation) in the CEE countries (reference year 2010=100)**
![](data/documents/ssrn-5233576/images/image_4_page_9.png)

**Figure 13 — The evolution FDI in the CEE countries**

### Panel VAR Model: Uncovering Causal Links

A Panel Vector Autoregression (PVAR) model was used to analyze the dynamic relationships between variables. After confirming data stationarity and selecting an optimal model, Granger causality tests revealed a crucial finding: both GDP growth and inflation have a unidirectional causal effect on unemployment.

**Table 1 — The results of panel unit root tests**
This table confirms that all variables are stationary, a prerequisite for the PVAR model.

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
This table guided the selection of a VAR(3) model for the analysis.

|   Lag | AIC       | SC        | HQ        |
|------:|:----------|:----------|:----------|
|     0 | 23.99048  | 24.21636  | 24.08217  |
|     1 | 21.27422  | 21.80129  | 21.48817  |
|     2 | 20.86073  | 21.68898* | 21.19694  |
|     3 | 20.69976  | 21.82919  | 21.15823* |
|     4 | 20.76087  | 22.19149  | 21.34161  |
|     5 | 20.69231  | 22.42411  | 21.39531  |
|     6 | 20.55633* | 22.58931  | 21.38158  |

**Table 3 — Granger causality test**
This table provides direct evidence that GDP growth and inflation Granger-cause unemployment, but not the other way around.

| Null Hypothesis:                                                     |    Chi-sq |   Prob. |
|:---------------------------------------------------------------------|----------:|--------:|
| GDP growth rate does not Granger Cause                               | 25.2334   |  0      |
| Unemployment rate Inflation rate does not Granger Cause Unemployment | 42.2884   |  0      |
| rate FDI does not Granger Cause Unemployment rate                    |  1.14351  |  0.7666 |
| Unemployment rate does not Granger Cause GDP                         |  3.65018  |  0.3018 |
| growth rate Unemployment rate does not Granger Cause Inflation       |  5.34779  |  0.148  |
| rate Unemployment rate does not Granger Cause FDI                    |  0.954303 |  0.8123 |

### A Reversed Phillips Curve: Inflation *Increases* Unemployment

The most striking finding from the CEE analysis is that an increase in inflation leads to a *positive* and persistent response in the unemployment rate. This directly contradicts the traditional Phillips Curve theory.
![](data/documents/ssrn-5233576/images/image_5_page_11.png)

**Figure 14 — Impulse response functions**
This figure shows that a shock to inflation generates a positive response in the unemployment rate, peaking at an increase of 0.8% after three years.

This suggests a stagflationary environment, where rising prices are associated with a weaker, not stronger, labor market. Variance decomposition analysis further shows that inflation shocks are a major driver of unemployment volatility, explaining over 23% of its variation over 10 periods.

**Table 4 — Variance decomposition analysis of unemployment**

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

---

## Section 4: The Unifying Factor - The Power of Economic Growth

While the inflation-unemployment relationship varies dramatically by region, the CEE analysis provides clear evidence for a more universal principle: economic growth is a powerful driver of employment. The very first US-based analysis highlighted the lack of GDP data as a key limitation, a gap which the CEE study fills.

The impulse response functions show that a positive shock to GDP growth leads to a statistically significant decrease in the unemployment rate for approximately two years. This aligns with Okun's Law, an empirically observed relationship which states that for every 1% increase in unemployment, a country's GDP will be roughly an additional 2% lower than its potential GDP. The CEE data provides strong support for this fundamental economic linkage.

---

## Section 5: Global Nuances and External Shocks

The analyses also shed light on other factors, revealing the unique economic signatures of different nations and the overriding influence of global events.

### The Case of Japan: A Different Economic Reality

A brief look at Japan, another country with complete data, showed an even weaker relationship between inflation and unemployment than in the US, with a DTW distance of **191.95**. This is attributed to Japan's unique modern economic history, characterized by decades of low inflation and deflation.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell30_out1.png)

**Figure 15 — DTW Warping Path for Japan Inflation and Unemployment**

### The Role of Foreign Direct Investment (FDI)

In the CEE countries, it was widely believed that FDI would be a major catalyst for job creation. However, the panel VAR analysis found that FDI does not have a statistically significant influence on the unemployment rate. While FDI may offer other benefits like technology transfer and increased productivity, it does not appear to be a direct lever for reducing unemployment in this context.

### The Overarching Impact of Global Crises

Across all datasets—US, CEE, and Japan—the impact of global shocks is undeniable. The 2008 financial crisis and the 2020 COVID-19 pandemic created simultaneous disruptions in GDP, unemployment, and inflation worldwide. These events demonstrate that national and regional economic relationships can be temporarily overridden by large-scale global forces.

---

## Conclusions & Future Outlook (December 2025)

This comprehensive analysis demonstrates that simple, one-size-fits-all economic theories are insufficient for navigating the complexities of the modern global economy.

**Main Takeaways:**
*   **The Phillips Curve is context-dependent and unreliable:** The classic inverse relationship between inflation and unemployment has significantly weakened in the US and is inverted in the CEE countries, where inflation is associated with *higher* unemployment.
*   **Economic growth is a robust driver of employment:** Across different economic systems, fostering GDP growth remains a key policy lever for reducing unemployment.
*   **Interest rate relationships are actively managed:** The link between inflation and interest rates is heavily mediated by the policy decisions of central banks in response to economic conditions.
*   **Local dynamics matter:** Economic relationships are shaped by unique national histories, from Japan's deflationary period to the post-transition challenges of CEE nations.

**Limitations:**
*   The analyses relied on annual data, which may smooth over shorter-term dynamics.
*   Linear relationships were the primary focus; more complex, non-linear dynamics exist but were not fully explored.
*   The absence of GDP data in the initial US study limited direct comparisons, highlighting the importance of comprehensive datasets.

**Future Outlook & Policy Implications for 2026:**
The world is currently navigating the aftermath of the post-pandemic inflationary surge of 2022-2024. Central banks, including the Federal Reserve and the ECB, responded with the most aggressive interest rate hikes in decades. As of late 2025, the primary debate revolves around achieving a "soft landing"—bringing inflation back to target without triggering a deep recession.

*   **For Policymakers:** The findings urge a move away from rigid reliance on the Phillips Curve. Instead, policy should be data-driven, recognizing that the drivers of inflation and unemployment can change. Maintaining price stability is critical, especially in economies like the CEE where inflation is shown to harm employment. Fostering sustainable economic growth remains the most reliable path to a healthy labor market.
*   **For Businesses and Investors:** Understanding these nuances is crucial for strategic planning. The breakdown of old relationships means that forecasting must account for a wider range of factors, including global supply chain dynamics, geopolitical events, and the specific credibility and stance of monetary authorities. The insignificant direct impact of FDI on employment in the CEE study also suggests that investment decisions should be based on a broader set of factors than just labor market effects.

Ultimately, a true understanding requires continuous engagement with current events, historical context, and a critical perspective on economic fundamentals.