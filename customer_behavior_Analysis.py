
import pandas as pd

# Load the dataset
df = pd.read_csv('Dataset/customer_shopping_behavior.csv')

print(df.head())


print(df.info())
print(df.describe())

print(df.isnull().sum())

#impute the missing values with the median of the respective columns and categorical columns
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

#snake casing the column names
df.columns = df.columns.str.lower().str.replace(' ', '_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

print(df.columns)


#creating new columns

#age group
labels = ['Young Adult', 'Adult','Middle-aged', 'Senior']
df['age_group']=pd.qcut(df['age'], q=4, labels=labels)

print(df[['age', 'age_group']].head(10))

#purchase frequency days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['frequency_of_purchases', 'purchase_frequency_days']].head(10))

#check discount applied and and promocode used
print((df['discount_applied'] == df['promo_code_used']).all())

df=df.drop('promo_code_used', axis=1)
print(df.columns)



# Going to save the cleaned and transformed data to MySQL database using SQLAlchemy
import urllib.parse
from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = urllib.parse.quote_plus("Panthu@2004")
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

print("Successfully connected and uploaded data to MySQL!")

# Read back sample
pd.read_sql("SELECT * FROM customer LIMIT 5;", engine)