# %% [markdown]
# # Set Up
# 
# ### Import necessary packages

# %%
import pandas as pd
from datetime import datetime, timedelta

# %% [markdown]
# ### Import data

# %% [markdown]
# 

# %%
relative_path = "Data/monthly_retail_trade_report_1992to05.2023.xlsx"

# Subset rows only to get not adjusted sales values
start_row = 4
end_row = 70

# Subset columns to get business type and sales per month
columns_range = "B:N"

# Loop through every sheet
current_year = 2022
end_year = 1991  # Stop at 1991 since you mentioned until 1992

# Loop through the years in reverse order
for year in range(current_year, end_year, -1):
    sheet_name = str(year)
    df_name = "df_" + str(year)
    
    # Read the Excel sheet for the current year
    df = pd.read_excel(relative_path, sheet_name=sheet_name, header=None,
                       skiprows=start_row, nrows=end_row - start_row + 1,
                       usecols=columns_range)
    
    # Assign the DataFrame to a variable with dynamic name
    globals()[df_name] = df

# %% [markdown]
# # Data Cleaning

# %% [markdown]
# ### Change Column Names

# %%
# Modify the first column

dataframes = [globals()[f"df_{year}"] for year in range(2022, 1991, -1)]

new_column_name = "Kind of Business"

for df in dataframes:
    df.rename(columns={df.columns[0]: new_column_name}, inplace=True)

# Example of accessing one of the modified dataframes
print(df_2022.head())


# %%
def first_days_of_months(year):
    first_days = []
    for month in range(1, 13):
        first_day = datetime(year, month, 1)
        first_days.append(first_day)
    return first_days

year = 2022

column_mapping = {i: date.strftime("%Y-%m-%d") for i, date in enumerate(first_days_of_months(year), start=2)}

df_2022.rename(columns=column_mapping, inplace=True)

print(df_2022.head())


# %%
def first_days_of_months(year):
    first_days = []
    for month in range(1, 13):
        first_day = datetime(year, month, 1)
        first_days.append(first_day)
    return first_days

dataframes = [globals()[f"df_{year}"] for year in range(2022, 1991, -1)]

for year, df in zip(range(2022, 1991, -1), dataframes):
    column_mapping = {i: date.strftime("%Y-%m-%d") for i, date in enumerate(first_days_of_months(year), start=2)}
    df.rename(columns=column_mapping, inplace=True)

# Example of accessing one of the modified dataframes
print(df_2022.head())

# %% [markdown]
# ### Drop first two rows

# %%
dataframes = [globals()[f"df_{year}"] for year in range(2022, 1991, -1)]

for df in dataframes:
    df.drop([0, 1], inplace=True)

# Example of accessing one of the modified dataframes
print(df_2022.head())


# %% [markdown]
# ### Combine all years in one DataFrame

# %%
# Create an empty list to store the melted dataframes
all_melted_dataframes = []

dataframes = [globals()[f"df_{year}"] for year in range(2022, 1991, -1)]

for year, df in zip(range(2022, 1991, -1), dataframes):
    df_melted = pd.melt(df, id_vars="Kind of Business", var_name="Date", value_name="Sales")
    
    # Append the melted dataframe to the list
    all_melted_dataframes.append(df_melted)

# Concatenate all the melted dataframes into one big dataframe
big_dataframe = pd.concat(all_melted_dataframes, ignore_index=True)

# Print a portion of the big dataframe
print(big_dataframe.head())


# %% [markdown]
# ### Remove NaN

# %%
big_dataframe.dropna(subset=['Sales'], inplace=True)

# %% [markdown]
# # Export Clean Data

# %%
big_dataframe.to_csv('Data/clean_us_monthly_retail_sales_1992_to_2022.csv', index=False)


