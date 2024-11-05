from fastapi import APIRouter, WebSocket, WebSocketDisconnect,Depends
import asyncio
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from typing import List, Dict, Any
import os
import json
import re
import anthropic
import ast
from fastapi import Query
from db.database import get_db  
from sqlalchemy.orm import Session
from services.product_services import MattressService


router = APIRouter()

project_id = os.getenv('project_id')
location = os.getenv('location')
agent_id = os.getenv('agent_id')
ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

conversation_states: Dict[str, List[Any]] = {}

def get_conversation_state() -> Dict[str, List[Any]]:
    return {"conversation": []} 



# Function to get access token
def get_access_token(service_account_file):
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    scoped_credentials.refresh(Request())
    return scoped_credentials.token

# Function to send request to Dialogflow CX
def send_request_to_dialogflow(project_id, location, agent_id, session_id, user_input):
    access_token = get_access_token('./gd-gcp-rnd-genai-assessment-dc91519ce774.json') 
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


def extract_links_and_text(message):
   
    url_pattern = r'(https?://[^\s]+)'
    
    urls = re.findall(url_pattern, message)
    
    text_without_urls = re.sub(url_pattern, '', message).strip()
    
    return text_without_urls, urls


# conversation_states: Dict[str, List[Any]] = {}
conversation_states = {} 

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,state: dict = Depends(get_conversation_state)):

    session_id = websocket.query_params.get('sessionId')
    
    if not session_id:
        await websocket.close(code=4000)  
        return

    print(f"Session ID from query parameters: {session_id}")
    
    if session_id not in conversation_states:
        conversation_states[session_id] = []
    
 
    await websocket.accept()
 
    try:
        while True:
            message = await websocket.receive_text()

            print(f"Received message: {message}")
            
            conversation_states[session_id].append({"text": message, "links": []})
            
            try:

                response = send_request_to_dialogflow(project_id, location, agent_id, session_id, message)
                print("webscoket",response)
            except ValueError:
                    
                    await websocket.send_json({"error": "websocket response failed"})

            if isinstance(response, dict):
                response_json = response  
            else:
                try:
                   
                    response_json = json.loads(response)
                except ValueError:
                   
                    await websocket.send_json({"error": "Received a non-JSON response."})
                    continue

            
            response_messages = response_json.get('queryResult', {}).get('responseMessages', [])
            
            formatted_response_messages = []
            for msg in response_messages:
                if 'text' in msg:
                    
                    for text in msg['text']['text']:
                        extracted_text, extracted_urls = extract_links_and_text(text)
                        formatted_response_messages.append({
                            "text": extracted_text,
                            "links": extracted_urls
                        })
                elif 'payload' in msg:
                    formatted_response_messages.append({
                        "text": "Received a payload message.",
                        "links": []
                    })
            
            # print(product_details_json)
            

            # formatted_response_messages.append({
            #             "data":product_details_json    
            #         })

            # Send the JSON response to the WebSocket client
            conversation_states[session_id].append(formatted_response_messages)
           
            await websocket.send_json({"messages": formatted_response_messages})

       
    except WebSocketDisconnect:
        print("Client disconnected")



@router.get("/final_output")
def json_output(session_id: str = Query(..., description="Session ID")):
    try:
        # Check if session exists and has messages
        
        if session_id not in conversation_states or not conversation_states[session_id]:
            return {"error": "No conversation history available"}

        
        last_message = conversation_states[session_id][-1] 
        
        
        print("Last Message:", last_message)

        
        product_details_json = anthropic_call(last_message)

        
        data = extract_data(product_details_json)
        print("Extracted Data:", data)
        
        # Return data or further processed result
        return {"data": data}
        
    except Exception as e:
        print("An error occurred:", str(e))
        return {"error": str(e)}


# @router.get("/final_output")
# def json_output(
#     session_id: str = Query(..., description="Session ID"),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Check if session exists and has messages
#         if session_id not in conversation_states or not conversation_states[session_id]:
#             return {"error": "No conversation history available"}

#         # Get the last message from the conversation
#         last_message = conversation_states[session_id][-1]
#         print("Last Message:", last_message)

#         # Generate product details JSON from the conversation
#         product_details_json = anthropic_call(last_message)
        
#         # Extract data fields from the JSON
#         data = extract_data(product_details_json)
#         print("Extracted Data:", data)
        
#         # Prepare filter parameters based on extracted data, setting None as default
#         filter_params = {
#             "name": data.get("name"),
#             "size": data.get("size"),
#             "comfort": data.get("comfort"),
#             "best_for": data.get("best_for"),
#             "mattress_type": data.get("mattress_type"),
#             "cooling_technology": data.get("cooling_technology"),
#             "motion_separation": data.get("motion_separation"),
#             "pressure_relief": data.get("pressure_relief"),
#             "support": data.get("support"),
#             "adjustable_base_friendly": data.get("adjustable_base_friendly"),
#             "breathable": data.get("breathable")
#         }
        
        
#         filter_params = {k: v for k, v in filter_params.items() if v is not None}
        
       
#         mattresses = MattressService.filter_mattresses(db=db, **filter_params)

        
#         if not mattresses:
#             raise HTTPException(status_code=404, detail="No mattresses found")

#         for mattress in mattresses:
#             product_id_str = str(mattress.product_id)
#             prefix = product_id_str[:-1] 
            
#             mattress.images = [
#                 f"https://storage.googleapis.com/rnd-genai-assessment-demo2/images1/{prefix}/image_1.jpg",
#                 f"https://storage.googleapis.com/rnd-genai-assessment-demo2/images1/{prefix}/image_2.jpg"
#             ]

#         # Return the filtered list of mattresses as the final output
#         return {"data": mattresses}
        
#     except Exception as e:
#         print("An error occurred:", str(e))
#         return {"error": str(e)}



def extract_data(json_response):
    try:
        # Step 1: Ensure 'data=' prefix is properly removed
        if json_response.startswith('data='):
            json_response = json_response[5:].strip()
        
        # Step 2: Replace empty string placeholders with null where appropriate
        json_response = json_response.replace('"current_price": ""', '"current_price": null')
        json_response = json_response.replace('"rating": ""', '"rating": null')
        json_response = json_response.replace('"num_reviews": ""', '"num_reviews": null')
        
        # Debug print to verify JSON format before parsing
        # print("Formatted JSON Response:", json_response)
        
        # Step 3: Parse JSON string to dictionary
        data_dict = json.loads(json_response)
        
        # Step 4: Convert any remaining empty strings to None if needed
        def replace_empty_strings(d):
            if isinstance(d, dict):
                return {k: replace_empty_strings(v) for k, v in d.items()}
            return None if d == "" else d
        
        # Apply conversion to handle empty string fields
        cleaned_data = replace_empty_strings(data_dict)
        
        return cleaned_data
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

# Example usage

def anthropic_call(response):
    completion = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system = """You are an expert assistant specialized in extracting and structuring information from text into a specific JSON schema.

        Instructions:
        1. Analyze the provided text and extract relevant information.
        2. If any field information is not present in the text:
           - Use an empty string ("") for missing text fields.
           - Use `null` for missing numeric fields or fields where the value is unknown or not applicable.
           - Use an empty array ([]) or empty object ({}) for list or object fields if they are missing.
        3. Maintain the exact structure of the JSON schema provided below.
        4. Do not add additional fields to the schema.
        5. Ensure all text values are strings, numerical values are numbers, and follow the guidelines for null and empty values.

        IMPORTANT: Return ONLY the JSON object without any additional comments or explanations.

        Required JSON Schema:
        {
            "name": string,
            "images": [string],
            "size": string,
            "comfort": string,
            "best_for": string,
            "mattress_type": string,
            "cooling_technology": string,
            "motion_separation": string,
            "pressure_relief": string,
            "support": string,
            "adjustable_base_friendly": string,
            "breathable": string,
        }

        Example Output:
        {
            "name": "Beautyrest BR800 13.5\" Plush Pillow Top Mattress",
            "images": [
                "images/Beautyrest_BR800_13.5_Plush_Pillow_Top_Mattress/image_1.jpg",
                "images/Beautyrest_BR800_13.5_Plush_Pillow_Top_Mattress/image_2.jpg",
                "images/Beautyrest_BR800_13.5_Plush_Pillow_Top_Mattress/image_3.jpg"
            ],
            "size": "King",
            "comfort": "Plush",
            "best_for": "Side Sleepers",
            "mattress_type": "Innerspring",
            "cooling_technology": "Yes",
            "motion_separation": "Yes",
            "pressure_relief": "Yes",
            "support": "Yes",
            "adjustable_base_friendly": "Yes",
            "breathable": "Yes",
        }

        If information is missing, example:
        {
            "name": "",
            "images": [],
            "size": "",
            "comfort": "",
            "best_for": "",
            "mattress_type": "",
            "cooling_technology": "",
            "motion_separation": "",
            "pressure_relief": "",
            "support": "",
            "adjustable_base_friendly": "",
            "breathable": "",
        }""",
        messages=[
            {
                "role": "user",
                "content": f"Please extract information from this text and format it according to the specified JSON schema: `{response}`"
            },
            {
                "role": "assistant", 
                "content": "I will analyze the text and provide a structured JSON output following the specified schema."
            }
        ],
        temperature=0,
    )
    
    response = completion.content[0].text
    return response