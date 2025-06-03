import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv(r"C:\Users\user\Downloads\NetflixViewingHistory.csv")

# Convert the date column to datetime format
df["Date"] = pd.to_datetime(df["Date"])
df["Weekday"] = df["Date"].dt.day_name()
df["Month"]  = df["Date"].dt.month
df["Day"] = df["Date"].dt.day

# Filter out entries that contain a season (indicating a series episode)
df_seasonal = df[df["Title"].str.contains("Season", na=False)].copy()
df_seasonal["Season"] = df_seasonal["Title"].str.extract(r"(\d+)\. Season").astype("Int64")
df_seasonal["Series"] = df_seasonal["Title"].str.extract(r"^(.*?): \d+\. Season", expand=False).str.strip()

# Show which series exist in each season
# Example: Season 1 might have Alpha Male series, but Season 2 might not include it
season_content = df_seasonal.groupby("Season")["Series"].apply(lambda x: list(set(x)))
# print(season_content)

# Show how many different days each series was watched
series_watch_days = df_seasonal.groupby("Series")["Day"].nunique()
# print(series_watch_days)

# Show the most watched weekday for each series
daily_watch_counts = df_seasonal.groupby(["Series", "Weekday"]).size()
most_watched_day = daily_watch_counts.groupby(level=0).idxmax()
# print(most_watched_day)

# Visualization: How many different days each series was watched
plt.figure(figsize=(10,6))
series_watch_days.sort_values().plot(kind='barh', color="lightseagreen")
plt.xlabel("Number of Days")
plt.ylabel("Series")
plt.title("Number of Different Days Each Series Was Watched")
plt.grid(axis='x', linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
