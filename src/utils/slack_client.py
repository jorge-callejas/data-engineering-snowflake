import requests

from config.settings import settings


class SlackClient:

    def send_message(self, message: str):

        response = requests.post(
            settings.slack_webhook_url,
            json={"text": message},
            timeout=30
        )

        response.raise_for_status()

        return response.status_code