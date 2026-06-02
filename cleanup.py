import requests
import config

API_BASE = "https://app.simplelogin.io/api"


def get_headers():
    return {
        "Authentication": config.SIMPLELOGIN_API_KEY,
        "Content-Type": "application/json",
    }


def delete_all_aliases():
    headers = get_headers()
    page = 0
    total = 0

    while True:
        resp = requests.get(f"{API_BASE}/aliases?page_id={page}", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        aliases = data.get("aliases", [])
        if not aliases:
            break

        for alias in aliases:
            aid = alias["id"]
            email = alias["email"]
            print(f"Deleting {email}...")
            requests.delete(f"{API_BASE}/aliases/{aid}", headers=headers)
            total += 1

        page += 1

    print(f"\nDeleted {total} alias(es).")
    return total


if __name__ == "__main__":
    delete_all_aliases()
