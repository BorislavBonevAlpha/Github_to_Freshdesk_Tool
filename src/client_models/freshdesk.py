import requests
import base64
from common.error_handling_utility import should_retry_exception
from services import contact_service
from typing import Optional, Dict, Any
import time


class FreshdeskAPI:
    BASE_URL = "https://{subdomain}.freshdesk.com/api/v2"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_headers(self) -> Dict[str, str]:
        encoded_api_key = base64.b64encode(self.api_key.encode()).decode()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_api_key}"
        }

    def get_freshdesk_contact(self, subdomain: str, email: str, timeout: int = 10, retries: int = 3) -> \
            Optional[Dict[str, Any]]:

        url = f'{self.BASE_URL}/contacts'.format(subdomain=subdomain)
        params = {"email": email}  # Pass the email as a parameter by which we will search
        headers = self.get_headers()

        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
                response.raise_for_status()

                contacts = response.json()
                if contacts:
                    # This searches if the contact you entered is in the system of contacts
                    # in freshdesk. We capture the contact like this, since the response is a list and it is with ONLY one
                    # element - the contact which you delete or add.
                    return contacts[0]

                    # No contact with this email was found
                return None
            except requests.RequestException as exc:
                if attempt < retries - 1 and should_retry_exception(exc):
                    time.sleep(2)  # Waiting for 2 seconds before retrying again
                else:
                    return None
            except Exception as exc:
                print(f"An error occurred - {str(exc)}")
                return None

    def create_or_update_contact(self, subdomain: str, github_user_info: Dict[str, Any], timeout: int = 10,
                                 retries: int = 3) -> Optional[Dict[str, Any]]:

        existing_contact = self.get_freshdesk_contact(subdomain, github_user_info.get('email'))
        headers = self.get_headers()

        # Updating if there is already contact with this info in the system
        if existing_contact:
            contact_id = existing_contact['id']
            url = f'{self.BASE_URL}/contacts/{contact_id}'.format(subdomain=subdomain)
            method = requests.put
            contact_service.update_contact(github_user_info)

        # Creating if there is no contact found
        else:
            url = f'{self.BASE_URL}/contacts'.format(subdomain=subdomain)
            method = requests.post
            contact_service.create_contact(github_user_info)

        for attempt in range(retries):

            try:
                response = method(url, json=github_user_info, headers=headers, timeout=timeout)
                response.raise_for_status()
                return response.json()  # Returns the response information

            except requests.RequestException as exc:
                if attempt < retries - 1 and should_retry_exception(exc):
                    time.sleep(2)
                else:
                    return None
            except Exception as exc:
                print(f"An error occurred - {str(exc)}")
                return None

    # Deletes a contact and puts it in the bin section in freshdesk
    def soft_delete_contact(self, subdomain: str, contact_id: int, timeout: int = 10, retries: int = 3) -> bool:

        url = f'{self.BASE_URL}/contacts/{contact_id}'.format(subdomain=subdomain)
        headers = self.get_headers()

        for attempt in range(retries):

            try:
                response = requests.delete(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                return True

            except requests.RequestException as exc:
                if attempt < retries - 1 and should_retry_exception(exc):
                    time.sleep(2)
                else:
                    return False
            except Exception as exc:
                print(f"An error occurred - {str(exc)}")
                return False

    # After that the contact gets permanently deleted from the bin
    def permanently_delete_contact(self, subdomain: str, current_user: Dict[str, Any], timeout: int = 10,
                                   retries: int = 3) -> bool:

        current_contact = self.get_freshdesk_contact(subdomain, current_user.get('email'), timeout)
        if not current_contact:
            return False

        contact_id = current_contact['id']
        delete_status = self.soft_delete_contact(subdomain, contact_id, timeout)
        if not delete_status:
            return False

        url = f'{self.BASE_URL}/contacts/{contact_id}/hard_delete'.format(subdomain=subdomain)
        headers = self.get_headers()

        for attempt in range(retries):
            try:
                response = requests.delete(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                return True

            except requests.RequestException as exc:
                if attempt < retries - 1 and should_retry_exception(exc):
                    time.sleep(2)
                else:
                    return False
            except Exception as exc:
                print(f"An error occurred - {str(exc)}")
                return False
