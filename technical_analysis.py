
#Conduct a technical analysis and calculate the following metrics for one day and one week from February 16, 2024: Moving Average, Bollinger Band, CCI (Commodity Channel Index)

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import talib

# Load data
eurinr_data = pd.read_csv('EURINR_data.csv')

# Convert date column to datetime
eurinr_data['Date'] = pd.to_datetime(eurinr_data['Date'])

# Filter data for February 2024
eurinr_feb_data = eurinr_data[(eurinr_data['Date'] >= '2024-02-01') & (eurinr_data['Date'] <= '2024-02-16')]

# Fit ARIMA model
model = ARIMA(eurinr_feb_data['Close'], order=(5,1,0))  # Example order, you may need to tune this
model_fit = model.fit()

# Forecast next week data
forecast = model_fit.forecast(steps=5)  # Forecast next 5 days

# Create DataFrame for predicted data
future_dates = pd.date_range(start='2024-02-17', periods=5)
predicted_data = pd.DataFrame({'Date': future_dates, 'Predicted_Close_Price': forecast})

# Calculate Bollinger Bands
rolling_std = eurinr_data['Close'].rolling(window=20).std()
eurinr_data['Middle_Band'] = eurinr_data['Close'].rolling(window=20).mean()
eurinr_data['Upper_Band'] = eurinr_data['Middle_Band'] + 2 * rolling_std
eurinr_data['Lower_Band'] = eurinr_data['Middle_Band'] - 2 * rolling_std

# Calculate Commodity Channel Index (CCI)
eurinr_data['CCI'] = talib.CCI(eurinr_data['High'], eurinr_data['Low'], eurinr_data['Close'], timeperiod=14)

# Predict moving averages for the next week
predicted_ma = []
for i in range(17, 22):
    past_week_data = eurinr_data[eurinr_data['Date'] < pd.Timestamp(f'2024-02-{i}')]
    predicted_ma.append(past_week_data['Close'].mean())

# Add predicted moving averages to the predicted data DataFrame
predicted_data['Predicted_MA'] = predicted_ma

# Calculate rolling standard deviation
rolling_std = eurinr_data['Close'].rolling(window=20).std()

# Calculate upper and lower Bollinger Bands
predicted_data['Upper_Band'] = predicted_data['Predicted_MA'] + (rolling_std.iloc[-1] * 2)
predicted_data['Lower_Band'] = predicted_data['Predicted_MA'] - (rolling_std.iloc[-1] * 2)

# Calculate CCI for the last day
cci_values = talib.CCI(eurinr_data['High'], eurinr_data['Low'], eurinr_data['Close'], timeperiod=14)
if not cci_values.empty:
    predicted_data['CCI'] = cci_values.iloc[-1]
else:
    predicted_data['CCI'] = None


# Print the predicted data for 17-21 Feb 2024 with Bollinger Bands and CCI
print("Predicted data for February 17-21, 2024:")
print(predicted_data[['Date', 'Predicted_Close_Price', 'Predicted_MA', 'Upper_Band', 'Lower_Band', 'CCI']])

# Save the predicted data with Bollinger Bands and CCI to a CSV file
predicted_data.to_csv("predicted_data_with_bands_and_CCI.csv", index=False)
print("Predicted data with Bollinger Bands and CCI saved to predicted_data_with_bands_and_CCI.csv")

# Visualize the results
plt.plot(eurinr_feb_data['Date'], eurinr_feb_data['Close'], label='Actual Close Prices', color='blue')
plt.plot(predicted_data['Date'], predicted_data['Predicted_Close_Price'], label='Predicted Close Prices', color='orange')
plt.plot(predicted_data['Date'], predicted_data['Upper_Band'], label='Upper Bollinger Band', color='green', linestyle='--')
plt.plot(predicted_data['Date'], predicted_data['Predicted_MA'], label='Predicted Moving Average', color='red', linestyle='--')
plt.plot(predicted_data['Date'], predicted_data['Lower_Band'], label='Lower Bollinger Band', color='purple', linestyle='--')
plt.title('Actual vs Predicted Close Prices for EUR/INR with Bollinger Bands and CCI')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

