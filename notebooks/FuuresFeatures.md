# Synthesizing Variables
After the previous analysis, we aim to focus on those that provide the most insight into market sentiment while minimizing redundancy in the information set:

- For ETH, the annualized basis and open interest exhibit a strong positive correlation with price, indicating that they are the primary drivers of market sentiment. 

- For BTC, only open interest shows a strong correlation with price, however, we will still include the annualized basis as a context variable since its defintion implies that it conveys some degree of market sentiment. If it turns out to be irrelevant, the weights optimization algorithm will, by definition, assign it to a weak weight (e.g. close to zero).

- Since the trends of volume and open interest are highly correlated after denoising the signals, and volume shows weaker correlation with price compared to other variables, we will exclude volume to avoid redundancy in the Fear and Greed Index.

- We will incorporate the trend of the annualized basis and the standard deviation of its residual component as indicators of fear and greed. Specifically, we will use the first derivatives of the trend $T_t^{Basis}$ and the standard deviation $\sigma_{\epsilon_t^{Basis}}$ of the residuals $\epsilon_t^{Basis}$.

- An upward trend ($\frac{\partial T_t^{Basis}}{\partial t} \geq 0$) signals greed in the market and vice versa.

- An increase in the residual standard deviation ($\frac{\partial \sigma_{\epsilon_t^{Basis}}}{\partial t} \geq 0$) reflects increasing market uncertainty, indicating fear.

- the residuals and seasonality of the open interest remain relatively flat and minor compared to the trend which indicates that the majority information about open interest is comprised in the trend component that's why we will only use that signal of the open interest

- we will use the first derivative of the trend of the open interest to check for increase or decrease coupled with the first derivative of the trend component in price to make the indicator $X_t = \frac{\partial T_t^{Price}}{\partial t} \times max(0,\frac{\partial T_t^{OI}}{\partial t})$:
  
  - Bullish Sentiment: If $X_t>0$, it indicates bullish sentiment. This scenario arises when both the price trend is increasing and the open interest trend is either increasing or stable (i.e., non-negative).
  
  - Bearish Sentiment: If $X_t<0$, it indicates bearish sentiment. This scenario arises when the price trends to decrease and the open interest trend is either increasing or stable