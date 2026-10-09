import requests

from config.settings import settings


payload = {
    "text": "Meetup pipeline initialized successfully"
}

response = requests.post(
    settings.slack_webhook_url,
    json=payload,
    timeout=30
)

print(response.status_code)
print(response.text)