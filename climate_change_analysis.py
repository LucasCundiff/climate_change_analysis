import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Function to create a plot in a new window
def create_plot_window(data, x, y, trend, title, xlabel, ylabel):
    plot_window = tk.Toplevel(app)
    plot_window.title(title)
    
    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    sns.lineplot(data=data, x=x, y=y, ax=ax, label=ylabel)
    sns.lineplot(data=data, x=x, y=trend, ax=ax, color='red', label='Trend')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Function to load data and setup analysis (to be called by GUI)
def analyze_and_compare():
    # Load the datasets
    temp_df = pd.read_csv('E:/Python Projects/climate_change_analysis/us_avg_temperature_data.csv')
    co2_df = pd.read_csv('E:/Python Projects/climate_change_analysis/co2_levels_data.csv')

    # Convert 'Year' to datetime format for both datasets
    temp_df['Year'] = pd.to_datetime(temp_df['Year'], format='%Y').dt.year
    co2_df['Year'] = pd.to_datetime(co2_df['Year'], format='%Y').dt.year

    # Trend Analysis with Linear Regression for Temperature
    temp_slope, temp_intercept, _, _, _ = linregress(x=temp_df['Year'], y=temp_df['Temperature'])
    temp_df['Trend'] = temp_intercept + temp_slope * temp_df['Year']

    # Trend Analysis for CO2 Levels (similar approach)
    co2_slope, co2_intercept, _, _, _ = linregress(x=co2_df['Year'], y=co2_df['CO2_Level'])
    co2_df['Trend'] = co2_intercept + co2_slope * co2_df['Year']

    # Creating plots in separate windows
    create_plot_window(temp_df, 'Year', 'Temperature', 'Trend', 'Global Average Temperature Over Time', 'Year', 'Temperature (°C)')
    create_plot_window(co2_df, 'Year', 'CO2_Level', 'Trend', 'CO2 Levels Over Time', 'Year', 'CO2 Level (ppm)')

# Main application window setup
app = tk.Tk()
app.title('Climate Change Data Analysis')
app.geometry('300x100')

analyze_button = ttk.Button(app, text="Analyze and Compare", command=analyze_and_compare)
analyze_button.pack(pady=20)

app.mainloop()