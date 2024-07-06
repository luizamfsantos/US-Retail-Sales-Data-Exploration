# %% [markdown]
# # Set Up
# 
# ### Import necessary packages

# %%
import pandas as pd
import matplotlib.pyplot as plt

# %% [markdown]
# ### Import data

# %%
relative_path = "Data/clean_us_monthly_retail_sales_1992_to_2022.csv"
df = pd.read_csv(relative_path)
df.head()

# %%
df["Kind of Business"].unique()

# %%
df.describe()

# %%
df.dtypes

# %%
df["Date"] = pd.to_datetime(df["Date"])
df.dtypes

# %%
df["Sales"] = pd.to_numeric(df["Sales"],errors="coerce")
df.dtypes

# %%
df.dropna(subset=['Sales'], inplace=True)
df.describe()

# %% [markdown]
# # Analysis
# 
# ## Trends
# 
# ### Simple Trend
# 
# #### Trends on total retail and food services sales in the US
# 
# On the x-axis, we have months. On the y-axis, we have total monthly retail and food services sales in the US in millions of US dolars.

# %%
retail_food_service = df.loc[df["Kind of Business"]=="Retail and food services sales, total"]
retail_food_service.set_index('Date', inplace=True)
retail_food_service.head()

# %%
# Ensure plots are displayed inline in the notebook
%matplotlib inline

# Sort values 
retail_food_service = retail_food_service.sort_values(by = "Date")

# Plot the time series
plt.figure(figsize=(10, 6)) 
plt.plot(retail_food_service.index, retail_food_service['Sales'], marker=',', linestyle='-')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('$MM Sales')
plt.title('US Monthly Retail and Food Services Sales')

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()


# %%
year_agg_retail = retail_food_service["Sales"].resample("A").sum()
year_agg_retail.head()

# %%
year_agg_retail.dropna(inplace=True)

# %%
year_agg_retail.index

# %%
# Plot the time series
plt.figure(figsize=(10, 6)) 
plt.plot(year_agg_retail.index, year_agg_retail, marker=',', linestyle='-')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('$MM Sales')
plt.title('US Yearly Retail and Food Services Sales')

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Trend Comparisons In Depth Look
# 
# Let's focus on leisure activities. Three types of retail sales that are commonly connected with leisure activities are: book stores, sporting goods stores, and hobby stores.

# %%
target_categories = ["Book stores","Sporting goods stores", "Hobby, toy, and game stores"]
leisure_activities = df[df["Kind of Business"].isin(target_categories)]
leisure_activities.describe()

# %%
# Set index to dates
leisure_activities.set_index('Date', inplace=True)

# Sort values 
leisure_activities = leisure_activities.sort_values(by = "Date")

# Group data by "Kind of Business"
grouped_leisure_activities = leisure_activities.groupby('Kind of Business')


# %%

# Plot the time series
plt.figure(figsize=(10, 6)) 

for name, group in grouped_leisure_activities:
    plt.plot(group.index, group['Sales'], marker=',', linestyle='-', label=name)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('$MM Sales')
plt.title('US Monthly Leisure Activities Sales')
plt.legend()

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()

# %%
# Group data by "Kind of Business" and Aggregate yearly
grouped_leisure_activities = leisure_activities.groupby(['Kind of Business', pd.Grouper(freq='A')]).sum()
# Reset index to convert "Kind of Business" back to a column
grouped_leisure_activities.reset_index(inplace=True)


# %%

# Plot the time series
plt.figure(figsize=(10, 6)) 

for name, group in grouped_leisure_activities.groupby('Kind of Business'):
    plt.plot(group['Date'], group['Sales'], marker=',', linestyle='-', label=name)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('$MM Sales')
plt.title('US Yearly Leisure Activities Sales by Type of Business')
plt.legend()

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()

# %% [markdown]
# The analysis of the annual time series graph depicting US leisure activities sales categorized by business type reveals several key trends. Notably, the data illustrates a rapid growth in sales for sporting goods, surpassing the growth rates of games and books. While the trajectory of sporting goods sales did experience a decline initially, a substantial surge was observed in 2020. This upswing can be attributed to the widespread adoption of outdoor pursuits during the COVID-19 pandemic.
# 
# Conversely, sales within the hobby, toy, and game store sector exhibited a comparatively sluggish growth pattern. In contrast to the robust expansion witnessed in sporting goods, the sales of these items advanced at a more moderate pace over the analyzed period.
# 
# Regrettably, the sales figures for bookstores portray a disheartening decline. This decline in book sales is particularly lamentable for individuals, like myself, who hold a passion for books.

# %% [markdown]
# ### Comparison between sales at women's clothing stores and men's clothing stores

# %%
men_women_clothes = df.loc[(df["Kind of Business"]=="Men's clothing stores") | (df["Kind of Business"] == "Women's clothing stores")]
men_women_clothes.set_index("Date", inplace=True)
men_women_clothes.head()

# %%
# Group data by "Kind of Business" and Aggregate yearly
men_women_clothes_yearly = men_women_clothes.groupby(['Kind of Business', pd.Grouper(freq='A')]).sum()
# Reset index to convert "Kind of Business" back to a column
men_women_clothes_yearly.reset_index(inplace=True)

# %%
# Plot the time series
plt.figure(figsize=(10, 6)) 

for name, group in men_women_clothes_yearly.groupby('Kind of Business'):
    plt.plot(group['Date'], group['Sales'], marker=',', linestyle='-', label=name)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('$MM Sales')
plt.title("US Yearly Women's and Men's Clothing Stores Sales")
plt.legend()

# Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=45)

# Display the plot
plt.tight_layout()
plt.show()

# %% [markdown]
# Women's clothes stores' sales has consistently outperformed the men's counterpart. Also, while men's clothes stores sales stayed consistent over the years before COVID, women's has fluctuated over the years.
# Interestingly women's clothes stores' sales seems to have returned to pre-COVID years while men's are still down. 

# %% [markdown]
# #### How much is the difference between the genders?

# %%
# Filter data for Women's and Men's clothing stores separately
women_mask = df["Kind of Business"] == "Women's clothing stores"
men_mask = df["Kind of Business"] == "Men's clothing stores"

# Sort
women_clothes_data = df.loc[women_mask].sort_values("Date")
men_clothes_data = df.loc[men_mask].sort_values("Date")

# Set index to date 
women_clothes_data.set_index("Date",inplace=True)
men_clothes_data.set_index("Date",inplace= True)

women_men_diff = women_clothes_data.Sales - men_clothes_data.Sales

women_men_diff.describe()

# %%
# Create the Series with specified attributes
women_men_diff_series = pd.Series(data=women_men_diff, index=women_men_diff.index, name='Sales')

# Plot the time series
plt.figure(figsize=(10, 6))
women_men_diff_series.plot(kind='line', title="Monthly Difference between Women's and Men's Retail Clothing Sales")
plt.xlabel('Date')
plt.ylabel('Sales')
plt.show()

# %%
women_men_diff_series["2021-01-01":"2022-12-31"]

# %%
men_clothes_data["2021-01-01":"2022-12-31"]

# %% [markdown]
# There's some missing data from men clothing retail sales. So I'll drop the difference before 2021-04-01.

# %% [markdown]
# The surprising fact for me is that I expected for women's and men's clothing retail sales to walk together eliminating the seasonality but the oposite is true.

# %%
women_men_diff_series_yearly = women_men_diff_series.resample('Y').sum()
women_men_diff_series_yearly.drop(pd.to_datetime("2022-12-31"), inplace=True)
women_men_diff_series_yearly.drop(pd.to_datetime("2021-12-31"), inplace=True)
women_men_diff_series_yearly.tail()

# %%
# Plot the time series
plt.figure(figsize=(10, 6))
women_men_diff_series_yearly.plot(kind='line', title="Yearly Difference between Women's and Men's Retail Clothing Sales")
plt.xlabel('Year')
plt.ylabel('$MM Sales')
plt.show()

# %% [markdown]
# The difference between women's and men's retail clothing sales had been increasing until COVID. 

# %%
################################# 1 ###################################
# # Create a Figure
# fig = plt.figure(figsize=(8,3))

# # Create a bar plot of name vs grade
# plt.bar(x=df_students.Name, height=df_students.Grade)

# # Display the plot
# plt.show()

# # Create a bar plot of name vs grade
# plt.bar(x=df_students.Name, height=df_students.Grade, color='orange')

################################# 2 ###################################


# # Customize the chart
# plt.title('Student Grades') # so we know what it represents
# plt.xlabel('Student') # so we know which axis shows which data
# plt.ylabel('Grade')
# plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7) # makes it easier to determine the values for the bars
# plt.xticks(rotation=90) # rotate the markers so we can read them

# # Display the plot
# plt.show()

# %%
# # Create a figure for 2 subplots (1 row, 2 columns)
# fig, ax = plt.subplots(1, 2, figsize = (10,4))

# # Create a bar plot of name vs grade on the first axis
# ax[0].bar(x=df_students.Name, height=df_students.Grade, color='orange')
# ax[0].set_title('Grades')
# ax[0].set_xticklabels(df_students.Name, rotation=90)

# # Create a pie chart of pass counts on the second axis
# pass_counts = df_students['Pass'].value_counts()
# ax[1].pie(pass_counts, labels=pass_counts)
# ax[1].set_title('Passing Grades')
# ax[1].legend(pass_counts.keys().tolist())

# # Add a title to the Figure
# fig.suptitle('Student Data')

# # Show the figure
# fig.show() 

# %% [markdown]
# # Statistical Analysis
# 
# ## Descriptive statistics and data distribution
# 
# ### Distribution

# %%
# # Get the variable to examine
# var_data = df_students['Grade']

# # Create a Figure
# fig = plt.figure(figsize=(10,4))

# # Plot a histogram
# plt.hist(var_data)

# # Add titles and labels
# plt.title('Data Distribution')
# plt.xlabel('Value')
# plt.ylabel('Frequency')

# # Show the figure
# fig.show()

# %% [markdown]
# Is it symmetrical? Does it look normal?

# %% [markdown]
# ### Measures of central tendency

# %%
# # Get the variable to examine
# var = df_students['Grade']

# # Get statistics
# min_val = var.min()
# max_val = var.max()
# mean_val = var.mean() 
# med_val = var.median()
# mod_val = var.mode()[0]

# print('Minimum:{:.2f}\nMean:{:.2f}\nMedian:{:.2f}\nMode:{:.2f}\nMaximum:{:.2f}\n'.format(min_val,
#                                                                                         mean_val,
#                                                                                         med_val,
#                                                                                         mod_val,
#                                                                                         max_val))

# # Create a Figure
# fig = plt.figure(figsize=(10,4))

# # Plot a histogram
# plt.hist(var)

# # Add lines for the statistics
# plt.axvline(x=min_val, color = 'gray', linestyle='dashed', linewidth = 2)
# plt.axvline(x=mean_val, color = 'cyan', linestyle='dashed', linewidth = 2)
# plt.axvline(x=med_val, color = 'red', linestyle='dashed', linewidth = 2)
# plt.axvline(x=mod_val, color = 'yellow', linestyle='dashed', linewidth = 2)
# plt.axvline(x=max_val, color = 'gray', linestyle='dashed', linewidth = 2)

# # Add titles and labels
# plt.title('Data Distribution')
# plt.xlabel('Value')
# plt.ylabel('Frequency')

# # Show the figure
# fig.show()

# %% [markdown]
# ### Box Plot

# %%
# # Get the variable to examine
# var = df_students['Grade']

# # Create a Figure
# fig = plt.figure(figsize=(10,4))

# # Plot a histogram
# plt.boxplot(var)

# # Add titles and labels
# plt.title('Data Distribution')

# # Show the figure
# fig.show()

# %%
# # Create a function that we can re-use
# def show_distribution(var_data):
#     from matplotlib import pyplot as plt

#     # Get statistics
#     min_val = var_data.min()
#     max_val = var_data.max()
#     mean_val = var_data.mean()
#     med_val = var_data.median()
#     mod_val = var_data.mode()[0]

#     print('Minimum:{:.2f}\nMean:{:.2f}\nMedian:{:.2f}\nMode:{:.2f}\nMaximum:{:.2f}\n'.format(min_val,
#                                                                                             mean_val,
#                                                                                             med_val,
#                                                                                             mod_val,
#                                                                                             max_val))

#     # Create a figure for 2 subplots (2 rows, 1 column)
#     fig, ax = plt.subplots(2, 1, figsize = (10,4))

#     # Plot the histogram   
#     ax[0].hist(var_data)
#     ax[0].set_ylabel('Frequency')

#     # Add lines for the mean, median, and mode
#     ax[0].axvline(x=min_val, color = 'gray', linestyle='dashed', linewidth = 2)
#     ax[0].axvline(x=mean_val, color = 'cyan', linestyle='dashed', linewidth = 2)
#     ax[0].axvline(x=med_val, color = 'red', linestyle='dashed', linewidth = 2)
#     ax[0].axvline(x=mod_val, color = 'yellow', linestyle='dashed', linewidth = 2)
#     ax[0].axvline(x=max_val, color = 'gray', linestyle='dashed', linewidth = 2)

#     # Plot the boxplot   
#     ax[1].boxplot(var_data, vert=False)
#     ax[1].set_xlabel('Value')

#     # Add a title to the Figure
#     fig.suptitle('Data Distribution')

#     # Show the figure
#     fig.show()

# # Get the variable to examine
# col = df_students['Grade']
# # Call the function
# show_distribution(col)

# %% [markdown]
# ### Probability Density Function

# %%
# def show_density(var_data):
#     from matplotlib import pyplot as plt

#     fig = plt.figure(figsize=(10,4))

#     # Plot density
#     var_data.plot.density()

#     # Add titles and labels
#     plt.title('Data Density')

#     # Show the mean, median, and mode
#     plt.axvline(x=var_data.mean(), color = 'cyan', linestyle='dashed', linewidth = 2)
#     plt.axvline(x=var_data.median(), color = 'red', linestyle='dashed', linewidth = 2)
#     plt.axvline(x=var_data.mode()[0], color = 'yellow', linestyle='dashed', linewidth = 2)

#     # Show the figure
#     plt.show()

# # Get the density of Grade
# col = df_students['Grade']
# show_density(col)


