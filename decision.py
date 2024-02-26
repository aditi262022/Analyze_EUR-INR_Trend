#Based on the results of the technical indicators, make a decision to BUY, SELL or remain NEUTRAL, for the specified time frames.

import pandas as pd
import matplotlib.pyplot as plt

# Load data
eurinr_data = pd.read_csv('EURINR_data.csv')
one_week_data = pd.read_csv('one_week_data.csv')

# Convert date columns to datetime
eurinr_data['Date'] = pd.to_datetime(eurinr_data['Date'])
one_week_data['Date'] = pd.to_datetime(one_week_data['Date'])

# Filter data for February 2024
eurinr_feb_data = eurinr_data[(eurinr_data['Date'] >= '2024-02-01') & (eurinr_data['Date'] <= '2024-02-21')]
one_week_feb_data = one_week_data[(one_week_data['Date'] >= '2024-02-15') & (one_week_data['Date'] <= '2024-02-21')]

# Set up the plot
plt.figure(figsize=(12, 6))

# Plot EUR/INR data
plt.plot(eurinr_feb_data['Date'], eurinr_feb_data['Close'], label='EUR/INR', color='blue')

# Plot predicted data for the week
plt.plot(one_week_feb_data['Date'], one_week_feb_data['Predicted_MA'], label='Predicted', color='orange')

# Add arrows for increasing and decreasing points based on the difference between close prices of consecutive days
for index, row in eurinr_feb_data.iterrows():
    arrow_color = 'green' if row['Close'] - row['Open'] > 0 else ('red' if row['Close'] - row['Open'] < 0 else 'black')
    arrow_direction = '↑' if arrow_color == 'green' else ('↓' if arrow_color == 'red' else '-')
    plt.annotate(arrow_direction, (row['Date'], row['Close']), textcoords="offset points", xytext=(0,10),
                 ha='center', fontsize=12, color=arrow_color)

# Add arrows for increasing and decreasing points based on the difference between open and close values
for index, row in one_week_feb_data.iterrows():
    arrow_color = 'green' if row['Predicted_Close_Price'] - row['Predicted_MA'] > 0 else ('red' if row['Predicted_Close_Price'] - row['Predicted_MA'] < 0 else 'black')
    arrow_direction = '↑' if arrow_color == 'green' else ('↓' if arrow_color == 'red' else '-')
    plt.annotate(arrow_direction, (row['Date'], row['Predicted_Close_Price']), textcoords="offset points", xytext=(0,10),
                 ha='center', fontsize=12, color=arrow_color)


# Format the axes
plt.title('EUR/INR Price Fluctuation and Prediction for February 2024')
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.yticks(ticks=range(0, 121, 40))  # Set y-axis ticks from 0 to 160 with an increment of 40
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Format x-axis dates
plt.xticks(pd.date_range(start='2024-02-01', end='2024-02-21', freq='D'))  # Ensure 21 values on x-axis

# Add legend
plt.legend()

# Show the plot
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Add legend for buy, sell, and neutral
legend_handles = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Buy'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Sell'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='Neutral')
]
plt.legend(handles=legend_handles, loc='upper left')

# Show the plot
plt.show()


