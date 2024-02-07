import os
import csv
import json
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv
from descope import DescopeClient
from descope.management.user import UserObj
from descope.management.user_pwd import (
    UserPassword,
    UserPasswordDjango,
)

load_dotenv()

descope_client = DescopeClient(project_id=os.getenv("DESCOPE_PROJECT_ID"), management_key=os.getenv("DESCOPE_MANAGEMENT_KEY"))

def batch_create_users(users: List[UserObj]) -> Dict[str, Any]:
    try:
        data = descope_client.mgmt.user.invite_batch(users, send_mail=False)
        if "errorCode" in data:
            print(data)
            return None
        return data
        
    except requests.RequestException as e:
        print(f"Error creating user: {e}")
        return None


def write_csv(file_path: str, data: List[Dict[str, Any]]):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def process_csv(file_path: str):
    post_migration_user_export = []
    users = []
    failed_users = []
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        rowCount = 0
        batchCount = 0
        maxBatch = 100
        for row in reader:
            row["verifiedEmail"] = True if row["verifiedEmail"] == "TRUE" else False
            row["password"] = None if row["password"] == "" else row["password"]
            try:
                row["roleNames"] = json.loads(row["roleNames"])
            except json.JSONDecodeError:
                row["roleNames"] = []
            
            user = row

            user_obj_args = {
                "login_id": user["email"],
                "email": user["email"],
                "display_name": user.get("displayName"),
                "role_names": user.get("roleNames"),
                # "family_name": user.get("familyName"),
                # "given_name": user.get("givenName"),
            }

            if "password" in user and user["password"]:
                user_obj_args["password"] = UserPassword(
                    hashed=UserPasswordDjango(
                        hash=user["password"]
                    )
                )

            user_obj = UserObj(**user_obj_args)
            users.append(user_obj)

            if len(users) == maxBatch:
                batchCount += 1
                print("Creating users of batch ", batchCount)
                data = batch_create_users(users)
                created_users = data.get("createdUsers")
                res_failed_users = data.get("failedUsers")
                failed_users.extend(res_failed_users)

                for created_user in created_users:
                    created_user_map = {"userId": created_user["userId"], "email": created_user["email"]}
                    post_migration_user_export.append(created_user_map)

                print("Created users of batch ", batchCount)
                users = []
            if batchCount == 2:
                break
            rowCount += 1
        
    
    print("Create export")
    write_csv("src/export/post_migration_user_export.csv", post_migration_user_export)

if __name__ == '__main__':
    process_csv('src/generated_emails.csv')












# def create_user(userObj: UserObj) -> Dict[str, Any]:
#     try:
#         data = descope_client.mgmt.user.invite_batch([userObj], send_mail=False)
#         if "errorCode" in data:
#             print(data)
#             return None
#         user = userObj
    
#         if (user.get("roleNames")):
#             descope_client.mgmt.user.add_roles(login_id=user["email"], role_names=user["roleNames"])
#         final_user_obj = descope_client.mgmt.user.activate(user["email"])
#         return final_user_obj["user"]
#     except requests.RequestException as e:
#         print(f"Error creating user: {e}")
#         return None



def iteratively_update_users(users: List[UserObj], batchCount: int) -> Dict[str, Any]:
    try:
        print("Updating users...")
        count = 0
        for user in users:
            print("Updating user ", count, " of batch ", batchCount)
            data = descope_client.mgmt.user.activate(user.email)
            count += 1

        if "errorCode" in data:
            print(data)
            return None
        return data
    
        
    except requests.RequestException as e:
        print(f"Error creating user: {e}")
        return None
