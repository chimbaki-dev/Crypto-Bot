import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
from datetime import datetime
from utils.coingecko import get_coin_history

def generate_price_chart(coin_id):
    # Fetch historical data for the past 7 days
    days = 7
    prices = get_coin_history(coin_id, days)

    # Convert the timestamps to datetime objects and split into separate lists
    dates = [datetime.fromtimestamp(price[0] / 1000) for price in prices]
    values = [price[1] for price in prices]

    # Find the peak and lowest values and their dates
    peak_value = max(values)
    peak_date = dates[values.index(peak_value)]
    low_value = min(values)
    low_date = dates[values.index(low_value)]

    # Create the plot with a larger size
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, values)

    # Annotate the peak and low values on the plot
    ax.text(peak_date, peak_value, f'${peak_value:.2f}', fontsize=10, verticalalignment='bottom', horizontalalignment='right')
    ax.text(low_date, low_value, f'${low_value:.2f}', fontsize=10, verticalalignment='top', horizontalalignment='right')

    # Add small green and red dots for peak and low values
    ax.plot(peak_date, peak_value, 'go', markersize=8)  # Larger green dot for peak
    ax.plot(low_date, low_value, 'ro', markersize=8)    # Same size red dot for low

    # Format the date on the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
    fig.autofmt_xdate() # Rotate and align the date labels

    # Add gridlines and set background color
    ax.grid(True, linestyle='-', linewidth=0.5, color='gray')
    ax.set_facecolor('#f0f0f0')  # Light gray background

    # Customize the spines (borders) of the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)

    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(f'7-day price chart for {coin_id.capitalize()}')

    # Annotate peak and low values in the top right corner
    ax.text(0.97, 0.95, f'Peak Price: ${peak_value:.2f}\nLow Price: ${low_value:.2f}', transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))

    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Close the plot
    plt.close(fig)

    return buf