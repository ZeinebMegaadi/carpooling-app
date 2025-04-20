import pandas as pd
import requests
from google.colab import files


# Step 1: Upload the file (students_with_coordinates.csv)
uploaded = files.upload()


# Step 2: Read the file
file_name = "students_with_coordinates.csv"
df = pd.read_csv(file_name)


# Step 3: Choose a subset of students (first 30)
n = 30  # You can change this number
subset_df = df.head(n)


# Step 4: Prepare coordinates and names
locations = subset_df[["Longitude", "Latitude"]].values.tolist()
names = subset_df["Name"].tolist()


# Step 5: Set your OpenRouteService API key
api_key = "5b3ce3597851110001cf62485aac7cfe76944e5ba0c8dca4add0ea7a"  # Replace with your actual API key


# Step 6: Create the payload for the matrix request
url = "https://api.openrouteservice.org/v2/matrix/driving-car"
headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}
payload = {
    "locations": locations,
    "metrics": ["distance"],  # You can also add "duration"
    "units": "km"
}


# Step 7: Send the request
response = requests.post(url, json=payload, headers=headers)


# Step 8: Handle the response
if response.status_code == 200:
    matrix_data = response.json()["distances"]
    matrix_df = pd.DataFrame(matrix_data, index=names, columns=names)


    # Save the matrix to CSV
    output_file = "distance_matrix_km.csv"
    matrix_df.to_csv(output_file)
    files.download(output_file)
    print("✅ Distance matrix saved and ready for download.")
else:
    print("❌ Error:", response.status_code, response.text)