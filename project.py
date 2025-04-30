import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_excel("WorldBank.xlsx")
# print(data.info())
print(data.isnull().sum())

# Columns to drop (not needed for your 5 objectives)
columns_to_drop = [
    "Electric power consumption (kWh per capita)",
    "Infant mortality rate (per 1,000 live births)",
    "Population density (people per sq. km of land area)",
    "Unemployment (% of total labor force) (modeled ILO estimate)"
]

data.drop(columns=columns_to_drop, inplace=True)

# Columns you want to fill
columns_to_fill = [
    "GDP (USD)",
    "GDP per capita (USD)",
    "Life expectancy at birth (years)",
    "Birth rate, crude (per 1,000 people)",
    "Death rate, crude (per 1,000 people)",
    "Individuals using the Internet (% of population)"
]

for col in columns_to_fill:
    data[col] = (
        data.sort_values(by=["Country Name", "Year"])
            .groupby("Country Name")[col]
            .ffill()
            .bfill()
    )
data.to_csv("WorldBank_Cleaned.csv", index=False)

data2 = pd.read_csv("WorldBank_Cleaned.csv")
print(data2.info())
print(data.isnull().sum())

# Checking Relation Betweeen Columns  

# Load dataset
df = pd.read_csv("WorldBank_Cleaned.csv")

# Select relevant columns
cols = ['GDP per capita (USD)', 
        'Individuals using the Internet (% of population)', 
        'Life expectancy at birth (years)', 
        'Birth rate, crude (per 1,000 people)', 
        'Death rate, crude (per 1,000 people)']

df_selected = df[cols].dropna()

# Calculate correlation matrix
correlation = df_selected.corr()

# Plot heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Between Socio-Economic Indicators")
plt.show()

## OBJECTIVE 1:  

# Remove rows with missing values in important columns
df = df.dropna(subset=['GDP (USD)', 'GDP per capita (USD)', 'IncomeGroup'])

# Plot GDP over time by Income Group
plt.figure(figsize=(10, 6))
for group in df['IncomeGroup'].unique():
    group_data = df[df['IncomeGroup'] == group]
    yearly_avg = group_data.groupby('Year')['GDP (USD)'].mean()
    plt.plot(yearly_avg.index, yearly_avg.values, marker='o', label=group)

plt.title('Average GDP Over Time by Income Group')
plt.xlabel('Year')
plt.ylabel('GDP (USD)')
plt.legend(title='Income Group')
plt.grid(True)
plt.show()

# Plot GDP per capita over time by Income Group
plt.figure(figsize=(10, 6))
for group in df['IncomeGroup'].unique():
    group_data = df[df['IncomeGroup'] == group]
    yearly_avg = group_data.groupby('Year')['GDP per capita (USD)'].mean()
    plt.plot(yearly_avg.index, yearly_avg.values, marker='o', label=group)

plt.title('Average GDP per Capita Over Time by Income Group')
plt.xlabel('Year')
plt.ylabel('GDP per Capita (USD)')
plt.legend(title='Income Group')
plt.grid(True)
plt.show()

## OBJECTIVE 2:

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df_selected, 
                x='Individuals using the Internet (% of population)', 
                y='GDP per capita (USD)', 
                color='green')
plt.title("Internet Usage vs GDP per Capita")
plt.xlabel("Internet Usage (%)")
plt.ylabel("GDP per Capita (USD)")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df_selected, 
                x='Life expectancy at birth (years)', 
                y='GDP per capita (USD)', 
                color='purple')
plt.title("Life Expectancy vs GDP per Capita")
plt.xlabel("Life Expectancy (years)")
plt.ylabel("GDP per Capita (USD)")
plt.grid(True)
plt.show()

## OBJECTIVE 3: Regional & Income Group Disparities in Socio-Economic Indicators

sns.set(style="whitegrid")

# Group by Region and calculate average life expectancy
regional_life_exp = df.groupby("Region")["Life expectancy at birth (years)"].mean().sort_values()

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(x=regional_life_exp.values, y=regional_life_exp.index, palette="viridis")
plt.title("Average Life Expectancy by Region")
plt.xlabel("Life Expectancy (years)")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

## OBJECTIVE 4: 

cols = ['IncomeGroup', 'GDP per capita (USD)',
        'Individuals using the Internet (% of population)',
        'Life expectancy at birth (years)']

df_selected = df[cols].dropna()

# Group by Income Group and take mean
grouped = df_selected.groupby('IncomeGroup').mean()

# Plotting all three indicators together
# 1. GDP per capita
plt.figure(figsize=(6,4))
grouped['GDP per capita (USD)'].plot(kind='bar', color='skyblue')
plt.title('Average GDP per capita by Income Group')
plt.ylabel('GDP per capita (USD)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 2. Internet Usage
plt.figure(figsize=(6,4))
grouped['Individuals using the Internet (% of population)'].plot(kind='bar', color='orange')
plt.title('Internet Usage by Income Group')
plt.ylabel('% of Population')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
plt.show()

# 3. Life Expectancy
plt.figure(figsize=(6,4))
grouped['Life expectancy at birth (years)'].plot(kind='bar', color='seagreen')
plt.title('Life Expectancy by Income Group')
plt.ylabel('Years')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

## OBJECTIVE 5: 

cols = ['Region', 'GDP per capita (USD)', 
        'Individuals using the Internet (% of population)', 
        'Life expectancy at birth (years)']
df_region = df[cols].dropna()

region_mean = df_region.groupby('Region').mean().reset_index()
# print(region_mean)

# GDP per capita by Region
plt.figure(figsize=(6,4))
sns.barplot(x='Region', y='GDP per capita (USD)', data=region_mean)
plt.xticks(rotation=45)
plt.title("GDP per Capita by Region")
plt.show()

# Internet Usage by Region
plt.figure(figsize=(6,4))
sns.barplot(x='Region', y='Individuals using the Internet (% of population)', data=region_mean)
plt.xticks(rotation=45)
plt.title("Internet Usage by Region")
plt.show()

# Life Expectancy by Region
plt.figure(figsize=(6,4))
sns.barplot(x='Region', y='Life expectancy at birth (years)', data=region_mean)
plt.xticks(rotation=45)
plt.title("Life Expectancy by Region")
plt.show()