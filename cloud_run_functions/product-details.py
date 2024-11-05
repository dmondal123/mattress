from google.cloud import storage
import csv
import json
import functions_framework
import logging
import re

logging.basicConfig(level=logging.INFO)

def clean_value(value):
    if value is None:
        return None
    return re.sub(r'[^a-zA-Z0-9]', '', str(value).lower())

def convert_to_number(value):
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return value

def convert_to_boolean(value):
    if value is None:
        return False
    return value.lower() == 'yes'

@functions_framework.http
def get_product_details(request):
    """
    OpenAPI endpoint for getting product details
    ---
    openapi: 3.0.0
    info:
        title: Product Details API
        description: API to retrieve details for specific mattress products
        version: 1.0.0
    servers:
        - url: https://us-central1-gd-gcp-rnd-genai-assessment.cloudfunctions.net
    paths:
        /get-product-details:
            post:
                summary: Get product details
                requestBody:
                    required: true
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    product_name:
                                        type: string
                                        description: Name of the product
                responses:
                    200:
                        description: Successful response
                    400:
                        description: Bad request
                    404:
                        description: Product not found
                    500:
                        description: Internal server error
    """
    request_json = request.get_json(silent=True)
    logging.info(f"Request JSON: {request_json}")
    product_name = request_json.get('product_name')

    if not product_name:
        return json.dumps({
            "error": "No product_name provided",
            "status": 400,
            "message": "Bad Request"
        }), 400, {'Content-Type': 'application/json'}

    try:
        # Initialize GCS client
        client = storage.Client()
        bucket = client.get_bucket("rnd-genai-assessment-demo2")
        blob = bucket.blob("expanded_mattresses_new.csv")

        # Download and process the CSV file
        csv_content = blob.download_as_text()
        csv_reader = csv.DictReader(csv_content.splitlines())

        cleaned_product_name = clean_value(product_name)
        for row in csv_reader:
            if clean_value(row.get('name')) == cleaned_product_name:
                response_data = {
                    "status": 200,
                    "message": "Success",
                    "data": {
                        "product": {
                            "name": row.get('name'),
                            "size": row.get('size'),
                            "pricing": {
                                "current_price": convert_to_number(row.get('current_price'))
                            },
                            "ratings": {
                                "rating": convert_to_number(row.get('rating')),
                                "num_reviews": convert_to_number(row.get('num_reviews'))
                            },
                            "specifications": {
                            "comfort": row.get('comfort'),
                            "best_for": row.get('best for')
                        }
                        }
                    }
                }
                
                logging.info(f"Returning product details: {response_data}")
                return json.dumps(response_data), 200, {'Content-Type': 'application/json'}

        logging.warning(f"Product '{product_name}' not found")
        return json.dumps({
            "status": 404,
            "message": "Not Found",
            "error": f"Product '{product_name}' not found"
        }), 404, {'Content-Type': 'application/json'}

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return json.dumps({
            "status": 500,
            "message": "Internal Server Error",
            "error": f"An error occurred: {str(e)}"
        }), 500, {'Content-Type': 'application/json'}