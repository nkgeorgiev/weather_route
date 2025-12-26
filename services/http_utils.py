import requests
import json

def safe_request(method, url, **kwargs):
    """
    Wrapper around requests to log errors with full response content.
    
    Usage:
        safe_request("GET", url, params=params)
        safe_request("POST", url, json=body, headers=headers)
    """
    try:
        res = requests.request(method, url, **kwargs)
        res.raise_for_status()  # raises HTTPError for 4xx/5xx
        return res
    except requests.exceptions.HTTPError as e:
        print(f"\n--- HTTP Error {e.response.status_code} ---")
        try:
            error_json = e.response.json()
            print(json.dumps(error_json, indent=2))
        except Exception:
            print(e.response.text)
        raise  # re-raise so caller knows there was an error
    except requests.exceptions.RequestException as e:
        # Catch other network errors (timeouts, connection errors)
        print("\n--- Request Exception ---")
        print(str(e))
        raise