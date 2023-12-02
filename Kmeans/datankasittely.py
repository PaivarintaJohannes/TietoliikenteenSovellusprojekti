import pandas as pd

# Assuming your data is in a file named 'data.csv'
df = pd.read_csv('data.csv', header=None)

# Sort the data by Direction and ID
df.sort_values(by=[0, 1], inplace=True)

# Create a new DataFrame to store the reduced data
result_df = pd.DataFrame()

# Iterate through unique direction IDs
for direction_id in df[0].unique():
    # Select the first 50 rows for each direction ID
    subset_df = df[df[0] == direction_id].head(50)
    # Concatenate the subset to the result DataFrame
    result_df = pd.concat([result_df, subset_df])

# Save the result to a new CSV file
result_df.to_csv('result.csv', index=False, header=False)

