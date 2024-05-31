import requests


def should_retry_exception(exc: requests.RequestException) -> bool:
    # Determine if we should retry specific exception
    if isinstance(exc, requests.HTTPError):
        if 400 <= exc.response.status_code <= 499:
            print(f"Client error occurred - {str(exc)}")
            return False
        elif 500 <= exc.response.status_code <= 599:
            # We want to retry on server error
            print(f"Server error occurred - {str(exc)}")
            return True
        else:
            print(f"Unexpected HTTPError occurred - {str(exc)}")
            return False
    elif isinstance(exc, requests.Timeout):
        # We want to retry on Timeout error
        print(f"Timeout error occurred - {str(exc)}")
        return True
    else:
        # We don't want to retry anything else
        print(f"Unexpected RequestException error occurred - {str(exc)}")
        return False
