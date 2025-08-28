import openai
import json
import requests
from datetime import datetime, timedelta
import os

openai.api_key = "sk-proj"

try:
    with open("credentials.json", "r") as f:
        USER_CREDS = json.load(f)
except FileNotFoundError:
    print("🛑 ERROR: credentials.json not found. Please run the server and authenticate first.")
    exit()

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_calendar_event",
            "description": "Schedules an event on the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title or summary of the event."},
                    "start_time": {"type": "string", "description": "The start date and time for the event in ISO 8601 format."},
                    "duration_minutes": {"type": "integer", "description": "The event duration in minutes. The default is 60 minutes."}
                },
                "required": ["title", "start_time"]
            }
        }
    }
]

def run_agent(prompt: str):
    """Takes a user prompt and executes the appropriate tool."""
    if not openai.api_key:
        print("🛑 ERROR: OPENAI_API_KEY environment variable not set.")
        return
        
    print(f"User > {prompt}")
    

    current_time_prompt = f"The current date and time is {datetime.now().isoformat()}."
    
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": current_time_prompt},
            {"role": "user", "content": prompt}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message
    if not message.tool_calls:
        print("Agent > I'm not sure how to help with that. I can only schedule events.")
        return

    tool_call = message.tool_calls[0]
    
    if tool_call.function.name == "create_calendar_event":
        args = json.loads(tool_call.function.arguments)
        
        start_time_obj = datetime.fromisoformat(args['start_time'])
        duration = args.get('duration_minutes', 60)
        end_time_obj = start_time_obj + timedelta(minutes=duration)

        print(f"Agent > Understood. Scheduling '{args['title']}'...")
        print("Agent > Calling MCP Server to create the event...")


        api_response = requests.post(
            "http://localhost:8000/create-event",
            json={
                "credentials": USER_CREDS,
                "title": args['title'],
                "start_time_iso": start_time_obj.isoformat(),
                "end_time_iso": end_time_obj.isoformat()
            }
        )
        
        if api_response.status_code == 200:
            print(f"✅ Agent > Success! {api_response.json()}")
        else:
            print(f"🛑 Agent > Error: {api_response.text}")


if __name__ == "__main__":
    user_input = "Schedule a meeting for tomorrow at 4 PM to discuss the project launch for an hour"
    run_agent(user_input)