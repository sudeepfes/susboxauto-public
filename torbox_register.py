import time

TORBOX_URL = "https://torbox.app/login"
MANUAL_WAIT = 120


def register(page, alias_email: str, password: str) -> bool:
    print(f"Navigating to TorBox...")
    page.goto(TORBOX_URL, timeout=30000)
    page.wait_for_timeout(4000)

    signup_btn = page.get_by_role("button", name="Sign up")
    if signup_btn.is_visible():
        signup_btn.click()
        page.wait_for_timeout(1000)

    page.wait_for_selector("#email-input", timeout=10000)
    page.locator("#email-input").fill(alias_email)
    page.locator("#password-input").fill(password)
    page.locator("#consent-checkbox").check()
    page.wait_for_timeout(1500)

    submit_btn = page.locator("button[type='submit']")
    is_disabled = submit_btn.is_disabled()

    print(f"\n{'='*60}")
    print(f"Alias email: {alias_email}")
    print(f"{'='*60}")

    if not is_disabled:
        submit_btn.click()
        page.wait_for_timeout(5000)
        print("Registration submitted!")
        return True

    print("Solve the Turnstile captcha, then click 'Continue'.\n")
    for _ in range(MANUAL_WAIT // 10):
        time.sleep(5)
        if page.url != TORBOX_URL:
            print(f"\nRedirected to: {page.url}")
            print("Registration submitted!")
            return True

    print("Timed out waiting for captcha solve.")
    return False
