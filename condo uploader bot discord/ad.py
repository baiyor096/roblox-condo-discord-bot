import requests
import time
import os

token = os.environ['acctoken']

def send_message(channel_id, message, headers):
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
    response = requests.post(url, headers=headers, json={'content': message, 'tts': 'false'})
    if response.status_code == 429:
        retry_after = response.json().get('retry_after', 0)
        print(f'Error Slowmode, retrying after {retry_after} seconds...')
        time.sleep(retry_after)
        return send_message(channel_id, message, headers)  # Retry after waiting
    elif response.status_code == 200:
        print(f"Success: Message sent to channel {channel_id}")
    else:
        print(f"Error {response.status_code}: Could not send message to channel {channel_id}")

def advertise(game_id):
    message = f'''
    *2 Player Games*
    https://www.roblox.com/games/{game_id}/
    '''
    headers = {'authorization': token}
    channel_ids = [
        '894272415234945045'
    ]

    for channel_id in channel_ids:
        send_message(channel_id, message, headers)
        time.sleep(5)  # Wait 5 seconds between each request to avoid rate limits

# Example usage
advertise(1234567890)  # Replace with your game ID
