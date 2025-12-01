# The Interplay of Inflation, Interest Rates, and Unemployment
### A Global, Regional, and Empirical Analysis
**Date: 2025-11-28**

---

# Slide 1: The Core Analytical Problem

Traditional macroeconomic theories propose stable, predictable relationships between inflation, interest rates, and unemployment. However, recent global data challenges the universality of these textbook models.

This analysis investigates whether these foundational economic relationships hold true across different scopes—global, regional, and national—to build a more nuanced and actionable policy perspective.

---

# Slide 2: Our Analytical Framework

We dissect these dynamics through a multi-pronged investigation, moving from a broad overview to specific, high-conviction findings.

1.  **Global Exploratory Analysis:** Establish a baseline understanding of variable distributions and correlations.
2.  **Regional PVAR Model:** Use a Panel Vector Autoregression model on Central & Eastern European (CEE) countries to identify causal links.
3.  **Empirical Theory Test:** Examine US and Japan data to test the real-world validity of established economic theories.

---

# Slide 3: Global View: Variable Distributions![](notebook/inflation_interest_unemployment_analysis_v2/images/inflation_interest_unemployment_analysis_v2_cell4_out0.png)

*Caption: The global distributions for inflation, interest rates, and unemployment are all right-skewed. The pronounced "fat tail" in the inflation data indicates that extreme hyperinflationary events are more frequent than a normal distribution would predict, posing a significant tail risk.*

---

# Slide 4: Global View: Correlation Structure![](notebook/inflation_interest_unemployment_analysis_v2/images/inflation_interest_unemployment_analysis_v2_cell16_out1.png)

*Caption: The correlation matrix reveals a moderate negative relationship (-0.38) between inflation and real interest rates. Critically, the inflation-unemployment correlation is statistically negligible (-0.01) at this aggregate level, providing no initial support for a simple Phillips Curve trade-off.*

---

# Slide 5: Global View: The Inflation-Interest Rate Signal![](notebook/inflation_interest_unemployment_analysis_v2/images/inflation_interest_unemployment_analysis_v2_cell18_out0.png)

*Caption: This scatter plot visually confirms the negative trend between inflation and real interest rates. The relationships involving unemployment, however, show no discernible linear pattern. The global view is too noisy for simple conclusions, necessitating a more focused regional analysis.*

---

# Slide 6: Transition: From Global Noise to Regional Signal

The aggregated global data masks underlying dynamics. To isolate a clearer signal, our analysis narrows to a structurally similar region: the 11 Central and Eastern European (CEE) EU member states from 2000-2020.

**Hypothesis:** A regional analysis of a cohesive economic bloc will reveal stronger, more directional relationships than the global overview.

---

# Slide 7: CEE Deep Dive: Uncovering Causality

| Null Hypothesis: | Chi-sq | Prob. |
| :--- | ---: | ---: |
| Inflation rate does not Granger Cause Unemployment rate | 42.2884 | 0.000 |
| Unemployment rate does not Granger Cause Inflation rate | 5.34779 | 0.148 |

*Caption: Granger causality tests for the CEE region reveal a statistically significant, unidirectional causal link from inflation to unemployment (Prob. < 0.001). The reverse is not true. This is a critical directional insight that was invisible in the global data.*

---

# Slide 8: CEE Deep Dive: The Impact of an Inflation Shock![](documents/ssrn-5233576/images/image_5_page_11.png)

*Caption: The Impulse Response Function shows that a positive shock to inflation (second row, third column) produces a persistent, statistically significant increase in the unemployment rate. This evidence points towards stagflationary dynamics in the CEE region, directly challenging the traditional inflation-unemployment trade-off.*

---

# Slide 9: CEE Deep Dive: Inflation as the Dominant Driver

| Period | S.E. | UNEMPLOYMENT | GDP_GROWTH | INFLATION | FDI |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1.16 | 100.00 | 0.00 | 0.00 | 0.00 |
| 5 | 2.95 | 76.90 | 2.47 | **20.45** | 0.18 |
| 10 | 3.31 | 69.58 | 5.40 | **23.39** | 1.63 |

*Caption: Variance decomposition analysis quantifies the drivers of unemployment volatility. After 10 years, inflation shocks account for **23.39%** of the forecast error variance in unemployment, making it the most significant long-term driver—far outweighing GDP growth (5.4%).*

---

# Slide 10: Transition: Do These Findings Generalize?

The CEE analysis presents a compelling, localized story of a positive inflation-unemployment link. But does this dynamic apply to major, developed economies?

We now test the universality of these relationships by applying advanced time-series analysis to US and Japanese data, putting established theory on trial.

---

# Slide 11: Reality Check: The Phillips Curve Falters in US & Japan

| Figure 9: DTW for US Inflation vs. Unemployment | Figure 10: DTW for Japan Inflation vs. Unemployment |
| :---: | :---: |
| ![](notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell25_out1.png) | ![](notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell30_out1.png) |

*Caption: Dynamic Time Warping (DTW) reveals a high degree of dissimilarity between inflation and unemployment in both the US (Distance: 105.78) and Japan (Distance: 343.89). This provides strong empirical evidence against a stable, predictable Phillips Curve relationship in these economies.*

---

# Slide 12: Reality Check: The Policy-Driven Interest Rate Link![](notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell45_out1.png)

*Caption: In the US, there is a clear visual alignment between interest rate policy and inflation, particularly during the high-inflation era of the 1970s-80s. The relationship is not static; it is mediated by deliberate policy decisions, economic shocks, and structural breaks in the economy.*

---

# Slide 13: Synthesis: A Three-Tiered Conclusion

Our multi-pronged analysis reveals a nuanced reality that defies simple, universal rules.

1.  **Global:** High-level correlations are weak and potentially misleading. A moderate inflation-interest rate link exists, but the unemployment signal is lost in the noise.
2.  **Regional (CEE):** A clear, positive, and causal link from inflation to unemployment emerges, indicating a structural risk of stagflation.
3.  **National (US/Japan):** Foundational theories like the Phillips Curve do not hold up to empirical scrutiny, revealing complex, country-specific dynamics.

---

# Slide 14: Strategic Implications: The Future of Monetary Policy

The era of relying on universal macroeconomic rules is over. Effective economic policy requires a paradigm shift.

*   **Context is King:** Move beyond one-size-fits-all theories and adopt region- and country-specific models.
*   **Embrace Adaptability:** Frameworks must account for new structural realities like supply chain fragility and the rise of digital currencies.
*   **Data Over Dogma:** Recognize that the relationships between core indicators are dynamic, not fixed. Policy must be as fluid as the data that informs it.

---

# Slide 15: End of Presentation

**Q&A**