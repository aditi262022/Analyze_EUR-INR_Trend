#Scrape the EUR/INR currency data from Yahoo Finance, covering the period from January 1, 2023, to February 16, 2024.

import requests
import pandas as pd
from datetime import datetime
import io

def scrape_currency_data(start_date, end_date):
    
    # Convert start and end dates to UNIX timestamps
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    # Construct the URL
    url = f"https://query1.finance.yahoo.com/v7/finance/download/EURINR%3DX?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        
        # Send HTTP GET request to fetch the data
        response = requests.get(url, headers=headers)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            
            # Read the response content as CSV and create DataFrame
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
            
            # Return the DataFrame
            return df
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Define start and end dates
start_date = "2023-01-01"
end_date = "2024-02-16"

# Scrape currency data
currency_data = scrape_currency_data(start_date, end_date)

# Save DataFrame to CSV file
if currency_data is not None:
    currency_data.to_csv("EURINR_data.csv", index=False)
    print("Data has been successfully saved to EURINR_data.csv")
else:
    print("Failed to save data to CSV file.")
