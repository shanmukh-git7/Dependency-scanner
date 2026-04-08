import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def get_token():
    res = requests.post(f"{BASE_URL}/token", data={"username": "admin", "password": "admin"})
    if res.status_code == 200:
        return res.json()["access_token"]
    return None

def test_upload(filename, content, mime_type):
    token = get_token()
    if not token:
        print("Failed to get token")
        return
    
    files = {'file': (filename, content, mime_type)}
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.post(f"{BASE_URL}/scan", files=files, headers=headers)
    print(f"Testing {filename}: Status {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"  Deps found: {data['total_dependencies']}, Vulns: {data['vulnerabilities_count']}")
    else:
        print(f"  Error: {res.text}")

if __name__ == "__main__":
    # 1. Test package-lock.json
    pkg_lock = {
        "name": "test-app",
        "packages": {
            "node_modules/express": {"version": "4.17.1"},
            "node_modules/lodash": {"version": "4.17.21"}
        }
    }
    test_upload("package-lock.json", json.dumps(pkg_lock), "application/json")

    # 2. Test requirements.txt
    reqs = "flask==2.0.0\ndjango>=3.0\n# comment\nrequests"
    test_upload("requirements.txt", reqs, "text/plain")

    # 3. Test yarn.lock style
    yarn_lock = "\"lodash@^4.17.21\":\n  version \"4.17.21\""
    test_upload("yarn.lock", yarn_lock, "text/plain")

    # 4. Test yaml
    yaml_deps = "dependencies:\n  moment: 2.29.1\n  axios: 0.21.1"
    test_upload("deps.yaml", yaml_deps, "application/x-yaml")
