from google.cloud import storage
import json
import functions_framework
import re
import csv

def clean_value(value):
    if value is None:
        return None
    return re.sub(r'[^a-zA-Z0-9]', '', str(value).lower())

@functions_framework.http
def get_product_images(request):
    # Check if the request has a JSON body
    if request.method != 'POST':
        return json.dumps({"error": "Only POST requests are accepted"}), 400, {'Content-Type': 'application/json'}
    
    try:
        request_json = request.get_json(silent=True)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON in request body"}), 400, {'Content-Type': 'application/json'}
    
    if request_json is None:
        return json.dumps({"error": "Request body must contain valid JSON"}), 400, {'Content-Type': 'application/json'}
    
    product_name = request_json.get('product_name')
    
    if not product_name:
        return json.dumps({"error": "No product_name provided in request"}), 400, {'Content-Type': 'application/json'}

    
    # Initialize GCS client and access the bucket
    client = storage.Client()
    bucket = client.get_bucket("rnd-genai-assessment-demo2")
    blob = bucket.blob("expanded_mattresses_new.csv")

    csv_content = blob.download_as_text()
    csv_reader = csv.DictReader(csv_content.splitlines())
    
    cleaned_product_name = re.sub(r'\"\"', '"', product_name)
    cleaned_product_name = clean_value(cleaned_product_name)
    
    productID = None
    for row in csv_reader:
        if clean_value(row.get('name')) == cleaned_product_name:
            print(row.get("ProductID"))
            productID = row.get("ProductID")
                
    
    # Use the cleaned product name to form the folder path
    product_folder = f"images1/{productID}/"
    print(product_folder)
    blobs = bucket.list_blobs(prefix=product_folder)
    
    image_urls = []
    for blob in blobs:
        if blob.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_urls.append(f"https://storage.googleapis.com/{bucket.name}/{blob.name}")
    
    if not image_urls:
        return json.dumps({"message": f"No images found for product: {product_name}"}), 404, {'Content-Type': 'application/json'}

    return json.dumps({"image_urls": image_urls}), 200, {'Content-Type': 'application/json'}
