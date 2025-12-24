import requests
import time

import os

PORT = os.environ.get('PORT', '8000')
BASE = f'http://localhost:{PORT}'

def one_request(path='/', ua='Mozilla/5.0'):
    headers = {'User-Agent': ua}
    r = requests.get(BASE + path, headers=headers)
    print(path, r.status_code, r.json())

if __name__ == '__main__':
    print('Normal request')
    one_request('/', 'Mozilla/5.0')

    print('\nScanner UA')
    one_request('/', 'sqlmap')

    print('\nMultiple unique paths (rate/path based detection)')
    for i in range(1,26):
        one_request(f'/p{i}', 'Mozilla/5.0')
        time.sleep(0.05)
