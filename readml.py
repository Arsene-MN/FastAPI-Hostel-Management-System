import os
import pandas as pd

# Use the absolute path
file_path = os.path.join(os.getcwd(), "ml.csv")

# Read the CSV file into a dataframe
df = pd.read_csv(file_path)

# Generate summary statistics
summary = df.describe()
print(summary)
