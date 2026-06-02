import sys
import torbox_register
import proton_verify
import torbox_activate
import stremio_setup
import config
from playwright.sync_api import sync_playwright


def get_email():
    email = config.DUCKDUCKGO_EMAIL
    if not email or email == "your_email@duck.com":
        email = input("Enter your email (DuckDuckGo or any): ").strip()
    return email


def main():
    print("=== TorBox Auto-Registration & Activation v2 ===\n")

    email = get_email()
    print(f"Using email: {email}\n")

    with sync_playwright() as p:
        print("Launching browser...\n")

        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )
        page = context.new_page()

        try:
            print("=== Step 1: Registering TorBox account ===")
            ok = torbox_register.register(page, email, config.TORBOX_PASSWORD)
            if not ok:
                print("Registration did not complete.")
                sys.exit(1)

            if not proton_verify.verify(page):
                print("Verification did not complete.")
                sys.exit(1)

            torbox_activate.activate(page)

            stremio_setup.setup(page)

        finally:
            print("\n=== Done! ===")
            input("Press Enter to close the browser...")
            browser.close()


if __name__ == "__main__":
    main()
