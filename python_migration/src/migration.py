import os
import csv
import json
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv

load_dotenv()

def get_bearer() -> str:
    descope_project_id = os.getenv("DESCOPE_PROJECT_ID")
    descope_management_key = os.getenv("DESCOPE_MANAGEMENT_KEY")
    
    if descope_project_id is None:
        raise ValueError("DESCOPE_PROJECT_ID is not defined")
    if descope_management_key is None:
        raise ValueError("DESCOPE_MANAGEMENT_KEY is not defined")
    
    bearer = f"Bearer {descope_project_id}:{descope_management_key}"
    return bearer

def create_user(user: Dict[str, Any]) -> Dict[str, Any]:
    body = {
        "loginId": user["email"],
        "email": user["email"],
        "displayName": user.get("displayName"),
        "verifiedEmail": user["verifiedEmail"],
    }
    
    if "password" in user and user["password"]:
        body["hashedPassword"] = {"django": {"hash": user["password"]}}
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_bearer()
    }
    
    try:
        response = requests.post("https://api.descope.com/v1/mgmt/user/create", json=body, headers=headers)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred
        
        data = response.json()
        if "errorCode" in data:
            print(data)
            return None
        return data["user"]
    except requests.RequestException as e:
        print(f"Error creating user: {e}")
        return None

def update_user_status(login_id: str, status: str) -> Dict[str, Any]:
    body = {"loginId": login_id, "status": status}
    headers = {
        "Content-Type": "application/json",
        "Authorization": get_bearer()
    }
    
    try:
        response = requests.post("https://api.descope.com/v1/mgmt/user/update/status", json=body, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if "errorCode" in data:
            print(data)
            return None
        return data["user"]
    except requests.RequestException as e:
        print(f"Error updating user status: {e}")
        return None

def write_csv(file_path: str, data: List[Dict[str, Any]]):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def process_csv(file_path: str):
    imported_mapped_users = []
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["verifiedEmail"] = True if row["verifiedEmail"] == "TRUE" else False
            row["password"] = None if row["password"] == "" else row["password"]
            try:
                row["roleNames"] = json.loads(row["roleNames"])
            except json.JSONDecodeError:
                row["roleNames"] = []
            
            user = row
            created_user = create_user(user)
            if created_user:
                print("Created User:", created_user)
                created_user_map = {"userId": created_user["userId"], "email": created_user["email"]}
                imported_mapped_users.append(created_user_map)
                
                updated_user = update_user_status(created_user["email"], "enabled")
                print("Updated User:", updated_user)
    
    print("Mapped users:")
    print(imported_mapped_users)
    write_csv("src/export/imported_users.csv", imported_mapped_users)

# Since the original Node.js uses async/await and Python's requests library is synchronous,
# we remove async/await for the synchronous calls in this Python version.
# If you need to handle asynchronous HTTP requests in Python, consider using aiohttp instead.

if __name__ == '__main__':
    process_csv('src/sample_exported_users.csv')

