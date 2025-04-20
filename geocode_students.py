import pandas as pd
import requests
from google.colab import files


# Step 1: Upload the cleaned CSV file
uploaded = files.upload()


# Step 2: Read the uploaded CSV file (it already has Name and Location columns)
file_name = "cleaned_students_locations.csv"
df = pd.read_csv(file_name)


# Step 3: API Key
api_key = "8a844bdeb2b84bd8b4d741879187070a"


# Step 4: Fetch coordinates
results = []


for index, row in df.iterrows():
    name = row['Name']
    location = row['Location']
   
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}"
    response = requests.get(url)
    data = response.json()


    if data['results']:
        coords = data['results'][0]['geometry']
        lat, lng = coords['lat'], coords['lng']
    else:
        lat, lng = None, None


    results.append({
        "Name": name,
        "Location": location,
        "Latitude": lat,
        "Longitude": lng
    })


# Step 5: Save results to CSV
output_df = pd.DataFrame(results)
output_file = "students_with_coordinates.csv"
output_df.to_csv(output_file, index=False)


# Step 6: Download the file
files.download(output_file)