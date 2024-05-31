from typing import Any, Dict

# We map the values to the needed ones for freshdesk using this specific function
def map_github_to_freshdesk(user_info: Dict[str, Any]) -> Dict[str, Any]:
    return {

        'name': user_info['name'],
        'email': user_info['email'],
        'description': user_info['bio']

    }
