import os

BRAIN_SERVICES_URL = os.environ.get('BRAIN_SERVICES_URL', 'http://0.0.0.0')
BRAIN_SERVICES_PORT = int(os.environ.get('BRAIN_SERVICES_PORT', 8000))
BRAIN_SERVICES_API_KEY = os.environ.get('BRAIN_SERVICES_API_KEY', 'test-key')
