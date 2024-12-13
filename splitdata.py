import httpx
import pandas as pd

# Constants
API_URL = "http://localhost:8000/rooms/"  # Change to your FastAPI server URL

# Step 1: Fetch data from the /rooms API and save the first 50 rows to a CSV
def rooms_to_csv():
    response = httpx.get(API_URL)
    rooms = response.json()
    df = pd.DataFrame(rooms)
    df_first_50 = df.head(50)  # Take the first 50 rows
    df_first_50.to_csv('rooms_first_50.csv', index=False)
    print("First 50 rows saved to rooms_first_50.csv")

def extract_csv():
    df = pd.read_csv('rooms_first_50.csv')

    df_extracted = df[['number', 'capacity']]
    df_extracted.to_csv('rooms_extracted_columns.csv', index=False)
    print("Extracted columns saved to rooms_extracted_columns.csv")

    df_remaining = df.drop(columns=['number', 'capacity'])
    df_remaining.to_csv('rooms_remaining_columns.csv', index=False)
    print("Remaining columns saved to rooms_remaining_columns.csv")

# Step 3: Concatenate the original CSV and extracted columns CSV
def concatenate_csv():
    df_remaining = pd.read_csv('rooms_remaining_columns.csv')
    df_extracted = pd.read_csv('rooms_extracted_columns.csv')

    # Merge both DataFrames on the 'id' column to restore the original data
    df_merged = pd.concat([df_remaining, df_extracted], axis=1)

    # Save the merged DataFrame back to a CSV
    df_merged.to_csv('merged.csv', index=False)
    print("CSV files concatenated and saved to rooms_merged.csv")

# Run all steps
#rooms_to_csv()
#extract_csv()
# concatenate_csv()
