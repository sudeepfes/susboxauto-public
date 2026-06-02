import requests
import config

API_BASE = "https://app.simplelogin.io/api"


def get_headers():
    return {
        "Authentication": config.SIMPLELOGIN_API_KEY,
        "Content-Type": "application/json",
    }


def get_mailboxes():
    resp = requests.get(f"{API_BASE}/mailboxes", headers=get_headers())
    resp.raise_for_status()
    return resp.json()["mailboxes"]


def create_alias(mailbox_id, note="Automated TorBox account"):
    payload = {
        "mailbox_id": mailbox_id,
        "note": note,
    }
    resp = requests.post(f"{API_BASE}/alias/random/new", json=payload, headers=get_headers())
    resp.raise_for_status()
    data = resp.json()
    return data["email"]


def main():
    mailboxes = get_mailboxes()
    if not mailboxes:
        raise SystemExit(
            "No mailboxes found. Add your Proton Mail email as a mailbox at:\n"
            "  https://app.simplelogin.io/dashboard/mailbox"
        )

    print("Available mailboxes:")
    for m in mailboxes:
        print(f"  ID: {m['id']}  Email: {m['email']}")

    mailbox_id = mailboxes[0]["id"]
    email = create_alias(mailbox_id)
    print(f"\nAlias created: {email}")
    return email


if __name__ == "__main__":
    main()
