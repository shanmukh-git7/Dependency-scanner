import requests

BASE_URL = "http://localhost:8000"

def test_recovery():
    email = "test@example.com"
    print(f"Testing recovery for {email}...")
    res = requests.post(f"{BASE_URL}/forgot-password", json={"email": email})
    print(f"Status: {res.status_code}")
    print(f"Body: {res.json()}")
    
    if res.status_code == 200 and "debug_token" in res.json():
        token = res.json()["debug_token"]
        print(f"Attempting reset with token: {token}")
        res2 = requests.post(f"{BASE_URL}/reset-password", json={"token": token, "new_password": "newpassword123"})
        print(f"Reset Status: {res2.status_code}")
        print(f"Reset Body: {res2.json()}")
        
        print("Testing login with new password...")
        res3 = requests.post(f"{BASE_URL}/token", data={"username": "testuser", "password": "newpassword123"})
        print(f"Login Status: {res3.status_code}")
        if res3.status_code == 200:
            print("Login success with recovered password!")

if __name__ == "__main__":
    test_recovery()
