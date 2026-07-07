import requests

BASE = 'http://localhost:5000'

def test_features_endpoint():
    r = requests.get(f"{BASE}/features")
    assert r.status_code == 200

if __name__ == '__main__':
    print('Run this after starting the backend: pytest -q')
