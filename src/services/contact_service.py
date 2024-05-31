from database.data import insert_query, update_query
from datetime import datetime
from typing import Dict, Any


def create_contact(github_user_info: Dict[str, Any]) -> None:
    date_creation = datetime.now()
    insert_query('INSERT INTO UserData (date_creation, username) VALUES (?, ?)',
                 (date_creation, github_user_info['name']))


def update_contact(github_user_info: Dict[str, Any]) -> None:
    date_creation = datetime.now()
    update_query('UPDATE UserData SET date_creation = ? WHERE username = ?',
                 (date_creation, github_user_info['name']))
