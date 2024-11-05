import pandas as pd
import os
import ast

df = pd.read_csv("mattress_firm_final - Sheet1 (4).csv")

base_dir = "images"
for index, row in df.iterrows():
    # Extract old folder name from the first image path (e.g., 'Beautyrest_BR800_13.5_Plush_Pillow_Top_Mattress')
    first_image = ast.literal_eval(row['images'])[0]
    old_folder_name = first_image.split('/')[1]  # Assuming the second part is the folder name
    
    # Define new folder name based on product ID
    new_folder_name = f'{index + 1}'
    
    # Paths to old and new folder in the file system
    old_folder_path = os.path.join(base_dir, old_folder_name)
    new_folder_path = os.path.join(base_dir, new_folder_name)
    
    # Rename the folder in the file system
    if os.path.exists(old_folder_path):
        try:
            os.rename(old_folder_path, new_folder_path)
            print(f"Renamed folder '{old_folder_name}' to '{new_folder_name}'")
        except Exception as e:
            print(f"Error renaming folder: {e}")
    else:
        print(f"Folder '{old_folder_name}' not found")
    

# Add a product ID column (prod-1, prod-2, etc.)

# Save the updated DataFrame back to CSV (optional)
df.to_csv('updated_file_with_product_ids.csv', index=False)

# Show the resulting DataFrame
print(df)
