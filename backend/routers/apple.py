from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import os
import json
from fastapi import FastAPI

app = FastAPI()

router = APIRouter()

project_id = os.getenv('project_id')
location = os.getenv('location')
agent_id = os.getenv('agent_id')
token_id = os.getenv('token_id')

# Function to get access token
def get_access_token(service_account_file):
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    scoped_credentials.refresh(Request())
    return scoped_credentials.token

# Function to send request to Dialogflow CX
def send_request_to_dialogflow(project_id, location, agent_id, session_id, user_input):
    access_token = get_access_token('/Users/rakkumar/Downloads/gd-gcp-rnd-genai-assessment-dc91519ce774.json') 
    url = f"https://{location}-dialogflow.googleapis.com/v3/projects/{project_id}/locations/{location}/agents/{agent_id}/sessions/{session_id}:detectIntent"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    request_body = {
        "queryInput": {
            "text": {
                "text": user_input,
            },
            "languageCode": "en"
        }
    }
    
    response = requests.post(url, headers=headers, json=request_body)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text}

# Function to call a specific tool based on user input with ID token
def call_tool(url, id_token):
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text}

# Mapping tool URLs
tool_urls = {
    "MattressType": "https://mattress-type-ozbncmmqma-uc.a.run.app",
    "MattressFeatures": "https://mattress-features-ozbncmmqma-uc.a.run.app",
    "MattressBudget": "https://mattress-budget-ozbncmmqma-uc.a.run.app",
    "MattressSize": "https://mattress-size-ozbncmmqma-uc.a.run.app",
    "MattressBrand": "https://mattress-brand-ozbncmmqma-uc.a.run.app",
    "GetProductDetails": "https://function-details-ozbncmmqma-uc.a.run.app",
    "GetProductImages": "https://image2-ozbncmmqma-uc.a.run.app"
}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    session_id = 'test-session-1234'  
    id_token = ""  # Replace this with your actual ID token

    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message: {message}")
            
            # Send user input to Dialogflow CX
            dialogflow_response = send_request_to_dialogflow(project_id, location, agent_id, session_id, message)

            # Check for errors in the Dialogflow response
            if 'error' in dialogflow_response:
                await websocket.send_json({"error": dialogflow_response['error']})
                continue
            
            # Check if 'queryResult' exists and handle accordingly
            query_result = dialogflow_response.get('queryResult', {})
            fulfillment_text = query_result.get('fulfillmentText', None)

            if fulfillment_text:
                # Send fulfillment text back to the client
                await websocket.send_json({"message": fulfillment_text})
                
                # Process tools based on intent or fulfillment text
                for tool in ["MattressType", "MattressFeatures", "MattressBudget", "MattressSize", "MattressBrand"]:
                    if tool in fulfillment_text:
                        tool_response = call_tool(tool_urls[tool], id_token)
                        await websocket.send_json({
                            "tool": tool,
                            "response": tool_response
                        })

                # Optionally call product details and images functions here
                product_details_response = call_tool(tool_urls["GetProductDetails"], id_token)
                product_images_response = call_tool(tool_urls["GetProductImages"], id_token)

                await websocket.send_json({
                    "product_details": product_details_response,
                    "product_images": product_images_response
                })
            else:
                # Handle case where no fulfillment text is found
                await websocket.send_json({"error": "No fulfillment text found."})

    except WebSocketDisconnect:
        print("Client disconnected")