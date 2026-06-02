import requests
import config


def get_recipients():
    url = "https://app.addy.io/api/v1/recipients"
    headers = {
        "Authorization": f"Bearer {config.ADDY_API_TOKEN}",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]


def create_alias(recipient_ids, description="Automated TorBox account"):
    url = "https://app.addy.io/api/v1/aliases"
    headers = {
        "Authorization": f"Bearer {config.ADDY_API_TOKEN}",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
    }
    payload = {
        "domain": config.ADDY_DOMAIN,
        "description": description,
        "recipient_ids": recipient_ids
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()["data"]
    return data["email"]


def main():
    recipients = get_recipients()
    matched = [r for r in recipients if r["id"] == config.PROTON_RECIPIENT_ID]
    if not matched:
        print("Available recipients:")
        for r in recipients:
            print(f"  ID: {r['id']}  Email: {r['email']}")
        raise SystemExit("PROTON_RECIPIENT_ID not found. Pick one from the list above.")

    email = create_alias([config.PROTON_RECIPIENT_ID])
    print(f"Alias created: {email}")
    return email


if __name__ == "__main__":
    main()
