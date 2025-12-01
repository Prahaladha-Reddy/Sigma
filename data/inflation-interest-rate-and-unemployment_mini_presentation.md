# Analyzing Economic Relationships: Inflation, Interest Rates, and Unemployment

## Context & Objective

This notebook explores whether conventional economic theories regarding the relationships between inflation, interest rates, and unemployment hold true when tested against real-world data. The author, a student of business and economics, expresses skepticism about textbook theories and aims to validate them using empirical data.

The primary questions addressed are:
*   Is there an inverse relationship between inflation and unemployment?
*   Is there a direct relationship between inflation and interest rates?

## Data & Setup

The analysis uses a dataset containing annual economic indicators for various countries from 1970 onwards. Key variables include:
*   `Inflation, consumer prices (annual %)`
*   `Inflation, GDP deflator (annual %)`
*   `Real interest rate (%)`
*   `Deposit interest rate (%)`
*   `Lending interest rate (%)`
*   `Unemployment, total (% of total labor force) (national estimate)`
*   `Unemployment, total (% of total labor force) (modeled ILO estimate)`

The initial exploration focuses on the United States, followed by a brief look at other countries with complete data.

## Key Analytic Steps & Insights

*   **US Inflation and Unemployment Trends**: Individual and combined time series plots for the United States show the historical paths of inflation and unemployment.
*   **Pearson's Correlation (US Inflation vs. Unemployment)**: A Pearson's correlation coefficient of approximately **0.000** was calculated, indicating no significant linear relationship between inflation and unemployment in the US data.
*   **Dynamic Time Warping (DTW) for US Inflation vs. Unemployment**: To account for potential time lags, Dynamic Time Warping (DTW) was applied. The DTW distance for US inflation and unemployment was calculated as **100.27**.
*   **DTW for Japan Inflation vs. Unemployment**: Japan was identified as the only other country with complete data for both variables. The DTW distance for Japan's inflation and unemployment was significantly higher at **191.95**, suggesting an even weaker relationship than in the US.
*   **US Interest Rate and Inflation Trends**: Individual time series plots for the United States' real interest rate and inflation were examined. A noticeable spike in both variables was observed between 1970 and 1980.
*   **Dynamic Time Warping (DTW) for US Interest Rate vs. Inflation**: Applying DTW to US real interest rates and inflation yielded a distance of **100.27**. The notebook notes that the relationship appears complex, especially after the 2000s due to events like the dot-com bubble and the Great Financial Crisis.

## Figures & Visual Story

### United States Inflation Trend (1970-2021)
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell12_out1.png)
**Figure 1 — Inflation trend over the years in the United States**
This line plot illustrates the annual consumer price inflation in the United States, showing significant fluctuations, including peaks in the 1970s and early 1980s, and a more stable period thereafter.

### United States Unemployment Trend (1970-2021)
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell14_out1.png)
**Figure 2 — Unemployment trend over the years in the United States**
This plot displays the total unemployment rate in the United States, revealing periods of high unemployment, such as in the early 1980s and during the Great Recession.

### United States Unemployment and Inflation Combined Trend (1970-2021)
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell16_out1.png)
**Figure 3 — Unemployment and Inflation trend over the years in the United States**
This combined line plot allows for a visual comparison of inflation and unemployment trends in the US. While some inverse movement is suggested, it is not consistently clear.

### Dynamic Time Warping: US Inflation vs. Unemployment
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell25_out1.png)
**Figure 4 — DTW Warping Path for US Inflation and Unemployment**
This visualization shows the warping path between US inflation and unemployment time series. The DTW distance of **100.27** indicates that despite theoretical inverse relationships, a strong mathematical connection with potential delays is not evident in the data.

### Dynamic Time Warping: Japan Inflation vs. Unemployment
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell30_out1.png)
**Figure 5 — DTW Warping Path for Japan Inflation and Unemployment**
For Japan, the DTW distance between inflation and unemployment is **191.95**, which is considerably higher than for the United States, suggesting an even weaker relationship. This is attributed to Japan's unique economic history of consistently low inflation.

### United States Real Interest Rate Trend (1970-2021)
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell41_out1.png)
**Figure 6 — Real Interest Rate trend over the years in the United States**
This plot shows the real interest rate in the US, highlighting a significant increase in the late 1970s and early 1980s, followed by a general decline and periods of volatility.

### United States Inflation Trend (1970-2021)
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell42_out1.png)
**Figure 7 — Inflation trend over the years in the United States**
Re-presenting the US inflation trend, this figure is shown again to facilitate direct comparison with the interest rate trend, particularly noting the co-movement during the 1970s and 1980s.

### Dynamic Time Warping: US Interest Rate vs. Inflation
![](data/notebook/inflation-interest-rate-and-unemployment/images/inflation-interest-rate-and-unemployment_cell45_out1.png)
**Figure 8 — DTW Warping Path for US Real Interest Rate and Inflation**
The DTW distance for US real interest rates and inflation is **100.27**. While a visual correlation is apparent before the 2000s, the relationship becomes more complex afterward, influenced by major economic events.

## Conclusions & Next Steps

The analysis suggests that while economic theories provide a foundational understanding, real-world data often presents more complex relationships than textbook models imply.

*   **Inflation and Unemployment**: Despite theoretical inverse relationships (e.g., Phillips Curve), the Pearson's correlation for the US was near zero, and Dynamic Time Warping showed no strong, consistent mathematical connection, even when accounting for time lags, for both the US and Japan.
*   **Inflation and Interest Rates**: Theory suggests a direct relationship, which was visually supported during specific historical periods in the US (e.g., 1970s-1980s). However, DTW analysis revealed a complex relationship, particularly after the 2000s, influenced by significant economic events.

The author emphasizes that economic theories are merely the "tip of the iceberg." A true understanding requires continuous engagement with current events, historical context, and a critical perspective on economic fundamentals, rather than relying solely on rigid rules. The notebook encourages readers to delve deeper into the "why" behind economic changes and to recognize that past patterns do not guarantee future outcomes.