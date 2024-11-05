import pandas as pd
import ast

# Load the CSV into a pandas DataFrame
df = pd.read_csv('mattress_firm_final2.csv')

# Function to extract the first part of the image path
def extract_image_name(image_list_str):
    try:
        # Convert the string representation of list into an actual list
        image_list = ast.literal_eval(image_list_str)
        if image_list:
            # Extract the folder name from the first image path
            image_path = image_list[0]
            # Get the folder part of the path (up to the last '/')
            folder_name = image_path.rsplit('/', 1)[0] + '/'
            return folder_name
        else:
            return None
    except Exception as e:
        return None

# Apply the function to the 'images' column
df['image_name'] = df['images'].apply(extract_image_name)

# Save the updated DataFrame back to CSV (optional)
df.to_csv('updated_file.csv', index=False)

# Show the resulting DataFrame
print(df[['images', 'image_name']])
