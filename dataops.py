import requests
import pandas as pd

try:
    # Fetching data from the Hostels API
    hostels_api = requests.get('http://localhost:8000/hostels')
    hostels_api.raise_for_status()
    hostels_api_data = hostels_api.json()  # Expecting a list of hostels

    # Fetching data from the Rooms API
    rooms_api = requests.get("http://localhost:8000/rooms")
    rooms_api.raise_for_status()
    rooms_api_data = rooms_api.json()  # Expecting a list of rooms

    # Check if hostels_api_data is a list (not a dictionary with a 'hostels' key)
    if isinstance(hostels_api_data, list):
        hostels_df = pd.DataFrame(hostels_api_data)  # Directly convert list to DataFrame
    else:
        print("Error: Unexpected data format for hostels API.")
        exit()

    # Creating DataFrame for rooms, assuming rooms_api_data is structured as a list of rooms
    if isinstance(rooms_api_data, list):
        rooms_df = pd.DataFrame(rooms_api_data)
    else:
        print("Error: Unexpected data format for rooms API.")
        exit()


    # Fetching data from the Bookings API
    bookings_api = requests.get("http://localhost:8000/bookings")
    bookings_api.raise_for_status()
    bookings_api_data = bookings_api.json()  # Expecting a list of bookings

    # Check if bookings_api_data is a list
    if isinstance(bookings_api_data, list):
        bookings_df = pd.DataFrame(bookings_api_data)
    else:
        print("Error: Unexpected data format for bookings API.")
        exit()


    # Merging Hostels and Rooms data (inner join on hostel_id)
    merged_df = pd.merge(hostels_df, rooms_df, left_on="id", right_on="hostel_id", how="inner")

    # Counting rows in each DataFrame
    print(f"Hostels DataFrame row count: {hostels_df.shape[0]}")
    print(f"Rooms DataFrame row count: {rooms_df.shape[0]}")
    print(f"Merged DataFrame row count: {merged_df.shape[0]}")

    # Describing the data (statistical summary)
    print("\nHostels DataFrame Description:")
    print(hostels_df.describe())

    print("\nRooms DataFrame Description:")
    print(rooms_df.describe())

    print("\nMerged DataFrame Description:")
    print(merged_df.describe())

    # Encoding categorical features for hostels_df
    hostels_df = pd.get_dummies(hostels_df, drop_first=True)

    # Encoding categorical features for rooms_df
    rooms_df = pd.get_dummies(rooms_df, drop_first=True)

    # Right Join: All rows from rooms_df and matched rows from bookings_df based on room_id
    right_joined_df = pd.merge(rooms_df, bookings_df, left_on="id", right_on="room_id", how="right")

    # Calculate Length of Stay in bookings data
    right_joined_df['check_in_date'] = pd.to_datetime(right_joined_df['check_in_date'])  # Ensure check_in is in datetime format
    right_joined_df['check_out_date'] = pd.to_datetime(right_joined_df['check_out_date'])  # Ensure check_out is in datetime format
    right_joined_df['length_of_stay'] = (right_joined_df['check_out_date'] - right_joined_df['check_in_date']).dt.days

    print("\nRight Joined Bookings to Engineer Length of Stay:")
    print(right_joined_df)

    # Further analysis and additional join operations if necessary
    # Example of a full outer join with hostels and rooms data (all rows from both)
    outer_joined_df = pd.merge(hostels_df, rooms_df, left_on="id", right_on="hostel_id", how="outer")
    print("\nFull Outer Join between Hostels and Rooms:")
    print(outer_joined_df)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
