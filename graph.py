import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data(austin_file, nyc_file):
    austin_df = pd.read_csv(austin_file)
    nyc_df = pd.read_csv(nyc_file)
    
    austin_df["Occurred Date"] = pd.to_datetime(austin_df["Occurred Date"], errors="coerce")
    nyc_df["DATE OCC"] = pd.to_datetime(nyc_df["DATE OCC"], errors="coerce")
    
    return austin_df, nyc_df

def plot_crime_trends(austin_df, nyc_df):
    austin_trend = austin_df.groupby(austin_df["Occurred Date"].dt.to_period("M")).size()
    nyc_trend = nyc_df.groupby(nyc_df["DATE OCC"].dt.to_period("M")).size()
    
    plt.figure(figsize=(12, 6))
    plt.plot(austin_trend.index.astype(str)[::3], austin_trend.values[::3], label="Austin", color="blue")
    plt.plot(nyc_trend.index.astype(str)[::3], nyc_trend.values[::3], label="NYC", color="red")
    plt.xticks(rotation=45)
    plt.xlabel("Year-Month")
    plt.ylabel("Number of Crimes")
    plt.title("Crime Trends Over Time: Austin vs NYC")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_top_crime_categories(austin_df, nyc_df, top_n=10):
    austin_crimes = austin_df["Highest Offense Description"].value_counts().nlargest(top_n)
    nyc_crimes = nyc_df["Crm Cd Desc"].value_counts().nlargest(top_n)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=austin_crimes.values, y=austin_crimes.index, palette="Blues")
    plt.title("Top Crime Categories in Austin")
    plt.xlabel("Count")
    plt.show()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=nyc_crimes.values, y=nyc_crimes.index, palette="Reds")
    plt.title("Top Crime Categories in NYC")
    plt.xlabel("Count")
    plt.show()

def plot_crime_by_hour(austin_df, nyc_df):
    austin_df["Occurred Hour"] = pd.to_datetime(austin_df["Occurred Time"], format="%H%M", errors="coerce").dt.hour
    nyc_df["Occurred Hour"] = nyc_df["TIME OCC"] // 100
    
    plt.figure(figsize=(12, 6))
    sns.histplot(austin_df["Occurred Hour"].dropna(), bins=24, kde=True, color="blue")
    plt.title("Crime Occurrence by Hour in Austin")
    plt.xlabel("Hour of Day")
    plt.show()
    
    plt.figure(figsize=(12, 6))
    sns.histplot(nyc_df["Occurred Hour"].dropna(), bins=24, kde=True, color="red")
    plt.title("Crime Occurrence by Hour in NYC")
    plt.xlabel("Hour of Day")
    plt.show()

def main():
    austin_file = "Austin_Crime_Reports.csv"
    nyc_file = "NYC_Crime_Data_from_2020_to_Present.csv"
    
    austin_df, nyc_df = load_and_prepare_data(austin_file, nyc_file)
    
    plot_crime_trends(austin_df, nyc_df)
    plot_top_crime_categories(austin_df, nyc_df)
    plot_crime_by_hour(austin_df, nyc_df)
    
if __name__ == "__main__":
    main()
