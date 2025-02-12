import sys
sys.stdin = open('ip.txt','r')
sys.stdout = open('op.txt','w')


        
import aiohttp
import asyncio

async def send_post_request():
    # URL of the API endpoint
    url = "http://127.0.0.1:8000/test"

    # Data to send in the POST request
    payload = {
        "key1": "value1",
        "key2": "value2"
    }

    # Optional: Add headers (e.g., for authentication)
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json",
        "X-User-ID" :"User_123"
    }

    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        try:
            # Make the POST request
            for i in range(10):
                async with session.post(url, json=payload, headers=headers) as response:
                    # Check if the request was successful
                    if response.status == 200 or response.status == 201:
                        # Parse the JSON response
                        data = await response.json()
                        print("Response received:", data)
                    else:
                        print(f"Failed to submit data: {response.status}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the asynchronous function
asyncio.run(send_post_request())