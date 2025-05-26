import pandas as pd

# Load the dataset
df = pd.read_csv('netflix_titles.csv')

# 1. Inspect the dataset
print("Initial Info:")
print(df.info())
print("\nNull Values:")
print(df.isnull().sum())
print("\nDuplicates:", df.duplicated(subset=['show_id']).sum())

# 2. Handle missing values
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df['rating'].fillna('Unknown', inplace=True)
# Drop rows where critical fields are missing
df.dropna(subset=['title', 'date_added'], inplace=True)

# 3. Remove duplicates based on show_id
df.drop_duplicates(subset=['show_id'], keep='first', inplace=True)

# 4. Standardize text fields
df['country'] = df['country'].str.title().str.replace('United States', 'USA', case=False)
df['listed_in'] = df['listed_in'].str.title()

# 5. Convert date_added to dd-mm-yyyy
df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce').dt.strftime('%d-%m-%Y')

# 6. Rename columns to lowercase with underscores
df.columns = df.columns.str.lower().str.replace(' ', '_')

# 7. Fix data types
df['release_year'] = df['release_year'].astype(int)
# Parse duration (e.g., "90 min" to 90, "2 Seasons" to 2)
df['duration_value'] = df['duration'].str.extract(r'(\d+)').astype(float)
df['duration_unit'] = df['duration'].str.extract(r'(min|Season|Seasons)')
# Replace 'Seasons' with 'Season' for consistency
df['duration_unit'] = df['duration_unit'].replace('Seasons', 'Season')
# Ensure date_added is datetime
df['date_added'] = pd.to_datetime(df['date_added'], format='%d-%m-%Y', errors='coerce')

# 8. Final inspection
print("\nCleaned Info:")
print(df.info())
print("\nNull Values After Cleaning:")
print(df.isnull().sum())

# Save cleaned dataset
df.to_csv('cleaned_netflix.csv', index=False)
print("Cleaned dataset saved as 'cleaned_netflix.csv'")