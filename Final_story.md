# Slide 1: Rethinking the Trinity: Inflation, Unemployment & Interest Rates

Classic economic models, like the Phillips Curve, provide a foundational framework for the interplay between inflation, unemployment, and interest rates. They suggest predictable trade-offs that guide monetary policy.

This analysis challenges that textbook view. Using data from the US, Japan, and Central & Eastern Europe (CEE), we investigate whether these relationships hold in the face of real-world economic shocks and diverse regional dynamics.

---

# Slide 2: The US Case: A Faltering Phillips Curve?

The cornerstone of macroeconomic policy is the Phillips Curve, which posits an inverse relationship between inflation and unemployment. Lower unemployment should drive higher inflation.

We begin by examining US data to test this core assumption. A simple visual inspection of the long-term trends suggests the relationship is, at best, inconsistent.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell16_out1.png)


*Caption: A visual comparison of US inflation and unemployment trends. While some periods show inverse movement, many others do not, indicating the relationship is not stable over time.*

---

# Slide 3: Decadal Analysis Reveals Structural Breaks

When plotting unemployment against inflation by decade, the theoretical curve dissolves. The relationship is highly context-dependent, with different economic eras showing entirely different patterns. The tight cluster of the 2010s (low inflation, low unemployment) contrasts sharply with the stagflationary pattern of the 1970s.
![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell5_out0.png)


*Caption: This scatter plot shows no consistent, long-term inverse relationship. The data suggests the Phillips Curve is not a fixed law but a state-dependent phenomenon.*

---

# Slide 4: Quantifying a Weak Connection

Statistical analysis confirms the visual intuition. The connection between US inflation and unemployment is quantitatively weak, both in direct correlation and when accounting for time lags.

*   **Pearson Correlation:** A coefficient of ~0.00 indicates no significant linear relationship.
*   **Dynamic Time Warping (DTW):** A distance of 100.27 confirms the lack of a strong mathematical link, even with potential delays.

The evidence points to a "flattening" of the Phillips Curve in the US.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell25_out1.png)


*Caption: The DTW warping path visualizes the misalignment between the two time series, reinforcing the statistical finding of a weak relationship.*

---

# Slide 5: The Inflation-Interest Rate Dance

Economic theory suggests a direct link between inflation and interest rates, as central banks raise rates to cool an overheating economy. US data shows this relationship is heavily influenced by policy responses to major economic crises, particularly before the 21st century.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell45_out1.png)


*Caption: The relationship is visually apparent in the high-inflation era of the 1970s-80s but becomes more complex after 2000, shaped by quantitative easing and zero-interest-rate policies.*

---

# Slide 6: A Clearer Signal in the Correlation Matrix

While noisy, the relationship between inflation and *real* interest rates is clearer. The data reveals a moderate negative correlation (-0.54), which aligns with economic logic. Unexpected inflation erodes the real (inflation-adjusted) return on assets, resulting in a lower real interest rate. This highlights the active role of central banks in managing inflation expectations.
![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell8_out0.png)


*Caption: The heatmap quantifies the key relationships, confirming the weak inflation-unemployment link (0.17) and the much stronger negative link between inflation and real interest rates (-0.54).*

---

# Slide 7: A Different Story: Evidence from Central & Eastern Europe

The US analysis reveals weak or evolving relationships. To find a clearer signal, we turn to a panel data analysis of 11 Central & Eastern European (CEE) economies from 2000-2020. These transitioning economies exhibit significant volatility, providing a different analytical lens.
![](data/documents/ssrn-5233576/images/image_1_page_6.png)
![](data/documents/ssrn-5233576/images/image_3_page_8.png)


*Caption: The evolution of unemployment and inflation in the CEE region shows significant fluctuation, shaped by post-transition dynamics, EU integration, and global shocks.*

---

# Slide 8: The "Aha!" Moment: Uncovering a Causal Link

Using a Panel Vector Autoregression (PVAR) model, we move from correlation to causation. Granger Causality tests on the CEE data reveal a critical finding:

**Inflation has a unidirectional causal effect on unemployment.**

This means that in the CEE context, changes in inflation help predict future changes in unemployment, but the reverse is not true. This is a profound departure from the Phillips Curve framework.

| Null Hypothesis: | Chi-sq | Prob. |
| :--- | ---: | ---: |
| Inflation rate does not Granger Cause Unemployment | 42.2884 | 0.00 |
| Unemployment rate does not Granger Cause Inflation | 5.34779 | 0.148 |

*Caption: The statistical results are unambiguous (Prob. < 0.05). Inflation is a causal driver of unemployment in this dataset.*

---

# Slide 9: The CEE Anomaly: Inflation Shocks *Increase* Unemployment

The most striking finding is the *direction* of this causal link. An impulse response analysis shows that a shock to inflation generates a positive and persistent rise in unemployment, peaking after three years.

This is a complete inversion of the Phillips Curve, suggesting a stagflationary dynamic where rising prices are associated with a weaker, not stronger, labor market.
![](data/documents/ssrn-5233576/images/image_5_page_11.png)


*Caption: The impulse response function provides clear visual evidence. A positive shock to inflation (Response of UNEMPLOYMENT to INFLATION) leads to a statistically significant increase in the unemployment rate.*

---

# Slide 10: Decomposing the Drivers of Unemployment

Variance decomposition analysis reinforces this finding. It quantifies how much of the future volatility in unemployment can be explained by shocks to other variables.

Over a 10-period horizon, **inflation shocks account for over 23% of the variation in the CEE unemployment rate**, second only to unemployment's own inertia. This confirms inflation as a primary driver of labor market instability in this region.

| Period | UNEMPLOYMENT | GDP_GROWTH | INFLATION | FDI |
|---:|---:|---:|---:|---:|
| 10 | 69.58 | 5.40 | **23.39** | 1.63 |

*Caption: This table isolates the key drivers of unemployment volatility. The significant contribution from inflation (23.39%) underscores its detrimental impact on the CEE labor market.*

---

# Slide 11: The Unifying Factor: Economic Growth

While the inflation-unemployment relationship is region-specific, the role of economic growth appears more universal.

The CEE analysis provides strong evidence for Okun's Law: a positive shock to GDP growth leads to a statistically significant decrease in the unemployment rate. Fostering sustainable growth remains a robust and reliable policy lever for improving labor market outcomes across different economic systems.

---

# Slide 12: Adding Global Nuance

The analysis of other economies reinforces the core theme: context is critical.

*   **Japan:** Exhibits an even weaker inflation-unemployment link than the US (DTW distance of 191.95), a result of its unique multi-decade history of low inflation and deflation.
*   **Foreign Direct Investment (FDI):** Contrary to common assumptions, FDI was found to have no statistically significant causal impact on reducing unemployment in the CEE countries.
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell30_out1.png)


*Caption: Japan's distinct economic path further illustrates that macroeconomic relationships are not universal constants.*

---

# Slide 13: The Overriding Influence of Global Shocks

These regional dynamics do not operate in a vacuum. Major global events, such as the 2008 Financial Crisis and the 2020 COVID-19 pandemic, create synchronized disruptions across all variables and regions. These systemic shocks can temporarily override local economic relationships, demonstrating the interconnectedness of the modern global economy.

---

# Slide 14: Synthesis: Key Takeaways

Our analytical journey reveals that simple, one-size-fits-all economic theories are insufficient.

1.  **The Phillips Curve is Unreliable:** The relationship has flattened in the US and is inverted in the CEE region. Relying on it for policy is fraught with risk.
2.  **Inflation's Dual Nature:** While manageable in a mature economy like the US, inflation is a direct cause of higher unemployment in transitioning CEE economies.
3.  **Growth is Paramount:** Fostering GDP growth is the most consistent and powerful lever for reducing unemployment across diverse economic contexts.

---

# Slide 15: Strategic Implications for 2026 and Beyond

As we navigate the aftermath of the 2022-2024 global inflation surge, these insights are critical.

*   **For Policymakers:** Move beyond rigid adherence to the Phillips Curve. Policy must be data-driven and context-aware. In economies susceptible to stagflation, maintaining price stability is not just an inflation goal—it is a core component of employment strategy.
*   **For Investors:** Forecasting models must account for regional heterogeneity. The drivers of unemployment in Warsaw are fundamentally different from those in Washington. The data demands a more nuanced approach to assessing country risk and opportunity.