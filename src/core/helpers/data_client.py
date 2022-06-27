import json

import requests

from core import settings as core_settings


class DataClient:
    """
    Client to call brain services
    """
    base_url = f'{core_settings.BRAIN_SERVICES_URL}:{core_settings.BRAIN_SERVICES_PORT}'

    def predict_attending(self, input_data: dict) -> bool:
        """
        Call the attending prediction from the brain services
        :param input_data:
        :return:
        """
        url = f'{self.base_url}/predict_attending'
        headers = {'Authorization': f'Bearer {core_settings.BRAIN_SERVICES_API_KEY}'}

        response = requests.post(
            url=url,
            headers=headers,
            data=json.dumps(input_data),
        )
        response_json = response.json()
        return response_json['attending']
