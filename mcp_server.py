from fastapi import FastAPI, Request, HTTPException 
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

app = FastAPI()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

flow = Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/calendar'],
    redirect_uri='http://localhost:8000/oauth2callback'
)


@app.post("/create-event")
async def create_event(request: Request):
    """Creates an event in the user's primary calendar."""
    data = await request.json()
    creds_data = data['credentials']
    
    from google.oauth2.credentials import Credentials
    credentials = Credentials.from_authorized_user_info(creds_data)
    
    service = build('calendar', 'v3', credentials=credentials)
    
    is_all_day = data.get('is_all_day', False)
    
    if is_all_day:
        event = {
            'summary': data['title'],
            'start': {'date': data['start_time_iso']},
            'end': {'date': data['start_time_iso']},
        }
    else:
        if 'end_time_iso' not in data:
            raise HTTPException(status_code=400, detail="Missing 'end_time_iso' for a timed event.")
            
        event = {
            'summary': data['title'],
            'start': {'dateTime': data['start_time_iso'], 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': data['end_time_iso'], 'timeZone': 'Asia/Kolkata'},
        }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return {"status": "event created", "link": created_event.get('htmlLink')}

@app.get("/login")
def login():
    """Redirects the user to Google to authorize the app."""
    authorization_url, state = flow.authorization_url(
        access_type='offline', 
        include_granted_scopes='true'
    )
    return {"authorization_url": authorization_url}

@app.get("/oauth2callback")
def oauth2callback(request: Request):
    """Handles the callback from Google after user authorization."""
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials
    
    creds_json = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    print("AUTHENTICATION SUCCESSFUL! COPY THE CREDENTIALS BELOW: \n")
    print(creds_json)
    return {"message": "Authentication successful! Check your terminal for credentials."}