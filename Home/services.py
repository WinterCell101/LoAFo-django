import os
import requests
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

def post_to_facebook(message, image_path, link=None):
    page_id = os.environ.get('FACEBOOK_PAGE_ID')
    access_token = os.environ.get('FB_PAGE_ACCESS_TOKEN')

    if not access_token:
        return {"error": {"message": "Access Token not found in environment variables"}}

    # If there is an image, we use the 'photos' endpoint
    if image_path:
        url = f"https://graph.facebook.com/{page_id}/photos"

        # We append the link to the end of the message/caption instead of a separate param
        full_caption = f"{message}\n\nView Details: {link}" if link else message

        payload = {'caption': full_caption, 'access_token': access_token}

        with open(image_path, 'rb') as image_file:
            files = {'source': image_file}
            response = requests.post(url, data=payload, files=files)
    else:
        # Fallback to text-only if no image exists
        url = f"https://graph.facebook.com/{page_id}/feed"
        payload = {'message': message, 'access_token': access_token, 'link': link}
        response = requests.post(url, data=payload)

    return response.json()