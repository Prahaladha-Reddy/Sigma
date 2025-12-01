# US Economic Analysis: Inflation, Unemployment, and Interest Rates

## Context & Objective

This notebook presents an exploratory analysis of key economic variables in the United States, focusing on the relationships between inflation, unemployment, and real interest rates. The primary objective is to investigate the context-dependent nature of economic relationships, drawing parallels to findings from other studies (e.g., CEE study findings).

The analysis specifically aims to:
*   Examine the relationship between the Unemployment Rate and the Inflation Rate (Phillips Curve).
*   Quantify the linear relationships between key economic variables.
*   Identify limitations in the dataset regarding economic growth analysis.

## Data & Setup

The analysis utilizes the `inflation interest unemployment.csv` dataset.
*   **Data Filtering:** The dataset was filtered to include only data for the 'United States'.
*   **Column Selection & Renaming:** Key columns were selected and renamed for clarity:
    *   `Inflation, consumer prices (annual %)` to `Inflation_Rate`
    *   `Unemployment, total (% of total labor force) (modeled ILO estimate)` to `Unemployment_Rate`
    *   `Real interest rate (%)` to `Real_Interest_Rate`
*   **Data Cleaning:** Missing values were identified in `Unemployment_Rate` (21 entries) and `Real_Interest_Rate` (1 entry) and subsequently dropped, resulting in 30 annual observations for the US.
*   **Limitation:** It was noted that the dataset **lacks raw GDP data**, preventing the calculation of annual GDP growth rate and thus limiting analysis related to economic growth as a driver of employment.

## Key Analytic Steps & Insights

1.  **Phillips Curve Analysis:** A scatter plot of Unemployment Rate vs. Inflation Rate, colored by decade, was used to visualize their relationship.
    *   **Insight:** The theoretical inverse relationship (Phillips Curve) was not consistently strong across all decades in the US data, indicating a context-dependent nature. Some decades (e.g., 1990s, 2010s) showed periods of relatively low inflation and low unemployment, but no clear, sustained inverse correlation was observed over the entire time span.

2.  **Economic Growth Limitation:** The absence of GDP data in the dataset prevented the analysis of the relationship between economic growth and unemployment.
    *   **Insight:** This highlights a data limitation that restricts direct comparison with findings regarding economic growth as a driver of employment.

3.  **Correlation Matrix:** A correlation matrix was generated for Unemployment Rate, Inflation Rate, and Real Interest Rate to quantify their linear relationships.
    *   **Insight 1 (Unemployment & Inflation):** A very weak positive correlation (approximately **0.17**) was observed, reinforcing the Phillips Curve observation.
    *   **Insight 2 (Unemployment & Real Interest Rate):** A negligible negative correlation (approximately **-0.08**) was found.
    *   **Insight 3 (Inflation & Real Interest Rate):** A moderate negative correlation (approximately **-0.54**) was identified, suggesting that as inflation rises, real interest rates tend to fall.

## Figures & Visual Story

![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell5_out0.png)
**Figure 1 — Phillips Curve: Unemployment Rate vs. Inflation Rate by Decade**
This scatter plot illustrates the relationship between the Unemployment Rate and the Inflation Rate in the US, with points colored by decade. It shows that the classic inverse Phillips Curve relationship is not consistently strong across all decades, with points appearing scattered overall. While some decades like the 1990s and 2010s show periods of low inflation and low unemployment, a clear long-term inverse trend is not evident, suggesting the relationship has evolved over time.

![](data/notebook/US_Economic_Analysis/images/US_Economic_Analysis_cell8_out0.png)
**Figure 2 — Correlation Matrix of Key Economic Variables (US)**
This heatmap displays the Pearson correlation coefficients between the Unemployment Rate, Inflation Rate, and Real Interest Rate. It quantitatively confirms the weak positive correlation (0.17) between Unemployment and Inflation, and a negligible negative correlation (-0.08) between Unemployment and Real Interest Rate. A more substantial moderate negative correlation (-0.54) is observed between Inflation Rate and Real Interest Rate, an expected economic relationship where higher inflation tends to erode real returns.

## Conclusions & Next Steps

**Main Takeaways:**
*   The analysis provides evidence for the **context-dependent nature of the Phillips Curve** in the US, as the theoretical inverse relationship between unemployment and inflation was not consistently strong across all decades.
*   Quantitative analysis via a correlation matrix confirmed **weak linear relationships** between the Unemployment Rate and both the Inflation Rate (0.17) and Real Interest Rate (-0.08).
*   A **moderate negative correlation** (-0.54) was observed between the Inflation Rate and Real Interest Rate, aligning with economic expectations.

**Limitations:**
*   The primary limitation was the **absence of raw GDP data**, which prevented the analysis of the relationship between economic growth and unemployment. This restricts direct comparison with other studies on this aspect.
*   The analysis focused on **linear relationships**; more complex, non-linear dynamics might exist but were not explored.
*   The use of **annual data** might limit the granularity of insights into short-term economic fluctuations.

**Future Work:**
*   To further investigate the role of economic growth, a dataset including GDP figures would be required.
*   Exploring non-linear relationships or time-series models could provide deeper insights into the evolving dynamics of these economic variables.