import requests
import datetime
import pytz
from bs4 import BeautifulSoup
from django.core.cache import cache

import gzip

# Decompress the payload (since it seems compressed in gzip)

TOKEN_CACHE_KEY = 'api_session_token'  # Key to store the token in cache
TOKEN_EXPIRATION_KEY = 'api_token_expiration'  # Key to store token expiration in cache
TOKEN_EXPIRATION_BUFFER = datetime.timedelta(minutes=5)  # Buffer time to refresh token before it expires

def fetch_live_streams():
    from .models import Stream  # Importing Stream model from the current app's models
    streams = []

    # Define the local time zone (adjust as needed)
    local_tz = pytz.timezone('America/New_York')

    # Get the current time in the local timezone
    now = datetime.datetime.now(local_tz)

    # Try to get the cached token and its expiration time
    token = cache.get(TOKEN_CACHE_KEY)
    token_expiration = cache.get(TOKEN_EXPIRATION_KEY)
    print("28----", token)
    if token and token_expiration and now < token_expiration - TOKEN_EXPIRATION_BUFFER:
        print("Using cached token.")
    else: 
        # Perform login if no token is found or token has expired
        login_url = "https://api.therealworld.ag/auth/session/login"
        payload = {
            "email": "miguelsguel1980@gmail.com",
            "password": "Newera2000x",
            "device_id": "01J31R1MHGM4W5CWC09FX7V40V",  # Example device_id
            "device_type": "Desktop",
            "friendly_name": "chrome on Windows 10"
        }

        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://app.jointherealworld.com",
            "referer": "https://app.jointherealworld.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "x-captcha-token": "test",  # Replace with actual CAPTCHA token if required
        }

        # Create a session to maintain cookies
        session = requests.Session()

        

        # Send the POST request to log in
        response = session.post(login_url, json=payload, headers=headers)

        # Check if login was successful
        if response.status_code == 200:
            response_data = response.json()

            if 'token' in response_data:
                token = response_data['token']
                print(f"Login successful! Token: {token}")

                # Cache the token with expiration (you might need to adjust based on actual token lifespan)
                expiration_time = now + datetime.timedelta(hours=1)  # Assuming token lasts for 1 hour
                cache.set(TOKEN_CACHE_KEY, token, timeout=3600)  # Cache token for 1 hour
                cache.set(TOKEN_EXPIRATION_KEY, expiration_time, timeout=3600)
            else:
                print("Login successful, but no token found in the response.")
                return  # Exit function if token is not found
        else:
            print(f"Login failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return  # Exit function if login failed

    # Now, use the token for the second API request
    event_url = "https://rpc.therealworld.ag/api/trpc/calendar.getMyUpcomingEvents?batch=1&input=%7B%7D"
    
    event_headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://app.jointherealworld.com",
        "referer": "https://app.jointherealworld.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "x-session-token": token  # Use the cached or new token
    }

    # Make the GET request to fetch events and servers
    event_response = requests.get(event_url, headers=event_headers)

    if event_response.status_code == 200:
        event_data = event_response.json()
        data = event_data[0]['result']['data']
        events = data['events']
        servers = data['servers']

        # Create a dictionary to map server IDs to server names
        server_map = {server['_id']: server['name'] for server in servers}

        for event in events:
            server_id = event.get('serverId', None)
            server_name = server_map.get(server_id, "Unknown")

            livestream_title = event['name']
            start_time_utc = event.get('start', 'No start time found')
            end_time_utc = event.get('end', 'No end time found')

            if start_time_utc != 'No start time found' and end_time_utc != 'No end time found':
                utc_start_time = datetime.datetime.strptime(start_time_utc, "%Y-%m-%dT%H:%M:%S.%fZ")
                utc_end_time = datetime.datetime.strptime(end_time_utc, "%Y-%m-%dT%H:%M:%S.%fZ")

                utc_start_time = pytz.utc.localize(utc_start_time)
                utc_end_time = pytz.utc.localize(utc_end_time)

                local_start_time = utc_start_time.astimezone(local_tz)
                local_end_time = utc_end_time.astimezone(local_tz)

                formatted_start_time = local_start_time.strftime("%Y-%m-%d %I:%M:%S %p")
                formatted_end_time = local_end_time.strftime("%Y-%m-%d %I:%M:%S %p")

                if local_end_time > now:
                    is_live = local_start_time <= now <= local_end_time

                    # Make sure these keys match your model field names
                    # print(server_name, livestream_title, local_start_time, local_end_time, is_live)
                    streams.append({
                        'server_name': server_name,  # Update this key to match your model's field name
                        'title': livestream_title,  # Update this key to match your model's field name
                        'start_time': formatted_start_time,  # Update this key to match your model's field name
                        'end_time': formatted_end_time,  # Update this key to match your model's field name
                        'is_live': is_live  # Update this key to match your model's field name
                    })

    else:
        print(f"Failed to retrieve events. Status code: {event_response.status_code}")

    # Update the database with the live streams
    Stream.objects.all().delete()  # Clear existing streams
    for stream in streams:
        Stream.objects.create(**stream)
    return streams

# Example usage within your Django application
if __name__ == '__main__':
    fetch_live_streams()
