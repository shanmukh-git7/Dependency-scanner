import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    # 1. Register User
    print("Testing Registration...")
    user_cred = {"username": "testuser", "email": "test@example.com", "password": "password123"}
    try:
        res = requests.post(f"{BASE_URL}/register", json=user_cred)
        if res.status_code == 200:
            print("User Registered")
        elif res.status_code == 400 and "already registered" in res.text:
            print("User already exists (clean run expected but acceptable)")
        else:
            print(f"Registration Failed: {res.status_code} {res.text}")
    except Exception as e:
        print(f"Connection Failed: {e}")
        return

    # 2. Login
    print("Testing Login...")
    res = requests.post(f"{BASE_URL}/token", data={"username": "testuser", "password": "password123"})
    if res.status_code != 200:
        print(f"Login Failed: {res.text}")
        return
    token = res.json()["access_token"]
    print("Login Successful, Token Received")

    # 3. Upload Mock POM
    print("Testing Scan Upload...")
    mock_pom = """
    <project>
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.example</groupId>
        <artifactId>test-app</artifactId>
        <version>1.0</version>
        <dependencies>
            <dependency>
                <groupId>org.apache.logging.log4j</groupId>
                <artifactId>log4j-core</artifactId>
                <version>2.14.1</version>
            </dependency>
        </dependencies>
    </project>
    """
    files = {'file': ('pom.xml', mock_pom, 'text/xml')}
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.post(f"{BASE_URL}/scan", files=files, headers=headers)
    if res.status_code == 200:
        print(f"Scan Successful: {res.json()}")
        scan_id = res.json()['id']
    else:
        print(f"Scan Failed: {res.text}")
        return

    # 4. Get History
    print("Testing History...")
    res = requests.get(f"{BASE_URL}/history", headers=headers)
    if len(res.json()) > 0:
        print("History Retrieved")
    else:
        print("History Empty")

    # 5. PDF Generation
    print("Testing PDF Generation...")
    res = requests.get(f"{BASE_URL}/scan/{scan_id}/pdf", headers=headers)
    if res.status_code == 200:
        print("PDF Generated Successfully")
    else:
        print(f"PDF Failed: {res.status_code}")

if __name__ == "__main__":
    try:
        # Check if server is up
        requests.get(BASE_URL)
        test_flow()
    except:
        print("Server not running. Please start uvicorn backend.main:app --reload")
