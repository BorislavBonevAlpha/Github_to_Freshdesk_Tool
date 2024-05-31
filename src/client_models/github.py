import requests
from common.error_handling_utility import should_retry_exception
from typing import Optional, Dict, Any
import time


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str) -> None:
        self.token = token

    def get_github_user_information(self, username: str, timeout: int = 10, retries: int = 3) -> \
            Optional[Dict[str, Any]]:

        user_url = f"{self.BASE_URL}/users/{username}"
        emails_url = f"{self.BASE_URL}/user/emails"
        headers = {"Authorization": f"token {self.token}"}

        # If a potential error occurs the program will try to load it with the
        # specified number of retries
        for attempt in range(retries):
            try:
                response = requests.get(user_url, headers=headers, timeout=timeout)
                response.raise_for_status()
                user_info = response.json()

                # If the email is found in the first call, directly return the whole user_info
                if user_info.get("email"):
                    return user_info

                # If the first call does not give us the email, this here will find if the primary github email
                # is your main email since you can have multiple emails set
                response = requests.get(emails_url, headers=headers, timeout=timeout)
                response.raise_for_status()
                emails_info = response.json()

                for email in emails_info:
                    if email.get("primary"):
                        user_info["email"] = email["email"]
                        return user_info

                # If we get to here, it means that we were unable to fetch an email from github, which we need in order
                # to create a freshdesk contact (email is used as a unique identifier)
                return None

            except requests.RequestException as exc:
                if attempt < retries - 1 and should_retry_exception(exc):
                    time.sleep(2)  # Waiting for 2 seconds before retrying again
                else:
                    return None
            except Exception as exc:
                print(f"An error occurred - {str(exc)}")
                return None
