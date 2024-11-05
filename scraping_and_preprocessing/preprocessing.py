import pandas as pd
import ast

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('updated_file_with_product_ids.csv')

# Function to clean up list columns: remove curly quotes, dollar signs, fix double commas, and incomplete lists
def clean_list_column(column):
    if isinstance(column, str):
        # Replace curly quotes with straight quotes, remove double commas, and remove dollar signs
        cleaned_column = column.replace('“', '"').replace('”', '"').replace(',,', ',').replace('$', '')
        
        # Ensure the list is properly closed by adding a closing bracket if needed
        if cleaned_column.count('[') > cleaned_column.count(']'):
            cleaned_column += ']'
        
        return cleaned_column
    return column

# Apply cleaning function to the 'size' and 'current_price' columns
df['size'] = df['size'].apply(clean_list_column)
df['current_price'] = df['current_price'].apply(clean_list_column)

# Convert strings to lists using ast.literal_eval for safety
df['size'] = df['size'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
df['current_price'] = df['current_price'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Use pandas explode to transform lists into separate rows
df_expanded = df.explode(['size', 'current_price'])

# Save the expanded DataFrame to a new CSV file with a different name
df_expanded.to_csv('expanded_mattresses_new.csv', index=False)

# Optionally, print a sample to check the result
print(df_expanded.head())