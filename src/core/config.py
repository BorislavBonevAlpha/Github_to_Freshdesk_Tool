import os


class Config:
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
    FRESHDESK_TOKEN = os.environ.get("FRESHDESK_TOKEN")
