import httpx
import pandas as pd

# Constants
API_URL_ROOMS = "http://localhost:8000/rooms/"  # Change to your FastAPI server URL for rooms
API_URL_HOSTELS = "http://localhost:8000/hostels/"  # Change to your FastAPI server URL for hostels

# Step 1: Fetch data from the /rooms API and save the first 50 rows to a CSV
def rooms_to_csv():
    response = httpx.get(API_URL_ROOMS)
    rooms = response.json()
    df_rooms = pd.DataFrame(rooms)
    df_rooms_first_50 = df_rooms.head(50)  # Take the first 50 rows
    df_rooms_first_50.to_csv('rooms_first_50.csv', index=False)
    print("First 50 rooms saved to rooms_first_50.csv")

# Step 2: Fetch data from the /hostels API and save the first 50 rows to a CSV
def hostels_to_csv():
    response = httpx.get(API_URL_HOSTELS)
    hostels = response.json()
    df_hostels = pd.DataFrame(hostels)
    df_hostels_first_50 = df_hostels.head(50)  # Take the first 50 rows
    df_hostels_first_50.to_csv('hostels_first_50.csv', index=False)
    print("First 50 hostels saved to hostels_first_50.csv")

# Step 3: Concatenate the rooms and hostels CSV files to create one big CSV
def concatenate_csv():
    # Read the CSVs into DataFrames
    df_rooms = pd.read_csv('rooms_first_50.csv')
    df_hostels = pd.read_csv('hostels_first_50.csv')

    # Merge the DataFrames on a common column, e.g., 'hostel_id'
    # Ensure that 'hostel_id' is present in both DataFrames
    df_merged = pd.merge(df_rooms, df_hostels, left_on='hostel_id', right_on='id', how='inner')

    # Save the merged DataFrame back to a CSV
    df_merged.to_csv('rooms_and_hostels_merged.csv', index=False)
    print("CSV files concatenated and saved to rooms_and_hostels_merged.csv")

# Run all steps

# hostels_to_csv()
# concatenate_csv()
