import time
import config

LOGIN_URL = "https://account.proton.me/login"
INBOX_URL = "https://mail.proton.me/u/0/inbox"
POLL_SECONDS = 10
MAX_POLLS = 24


def do_login(page):
    print("Logging into Proton Mail...")
    page.goto(LOGIN_URL, timeout=30000)
    page.wait_for_timeout(5000)

    username_input = page.locator("#username")
    username_input.wait_for(state="visible", timeout=10000)
    username_input.fill(config.PROTON_USERNAME)
    page.wait_for_timeout(500)

    password_input = page.locator("#password")
    password_input.wait_for(state="visible", timeout=5000)
    password_input.fill(config.PROTON_PASSWORD)
    page.wait_for_timeout(500)

    submit = page.locator("button[type='submit']")
    submit.click()
    page.wait_for_timeout(8000)

    # Handle "which service?" page
    if "apps" in page.url:
        print("Selecting Mail service...")
        page.locator("a:has-text('Mail')").first.click()
        page.wait_for_timeout(5000)

    print(f"Current URL: {page.url}")
    return True


def poke_inbox(page):
    page.goto(INBOX_URL, timeout=30000)
    page.wait_for_timeout(5000)
    # Click "Unread" to show unread emails first
    try:
        unread = page.locator("button:has-text('Unread')").first
        if unread.is_visible(timeout=2000):
            unread.click()
            page.wait_for_timeout(3000)
    except:
        pass


def find_torbox_email(page):
    for selector in [
        "text=TorBox",
        "span:has-text('TorBox')",
        "div:has-text('TorBox')",
        "[data-testid='conversation-item']:has-text('TorBox')",
        "a:has-text('TorBox')",
    ]:
        try:
            el = page.locator(selector).first
            if el.is_visible(timeout=2000):
                print(f"Found TorBox email via: {selector}")
                el.click()
                page.wait_for_timeout(5000)
                return True
        except:
            continue
    return False


def wait_for_torbox_email(page):
    print("\n=== Step 3: Verifying via Proton Mail ===")
    page.goto(LOGIN_URL, timeout=30000)
    page.wait_for_timeout(5000)

    if "login" in page.url:
        do_login(page)

    poke_inbox(page)

    for attempt in range(MAX_POLLS):
        print(f"Looking for TorBox email... (attempt {attempt + 1}/{MAX_POLLS})")
        page.reload()
        page.wait_for_timeout(5000)

        if find_torbox_email(page):
            return True

        if attempt < MAX_POLLS - 1:
            time.sleep(POLL_SECONDS)

    print("Timed out waiting for TorBox verification email.")
    return False


def is_verify_link(href):
    if not href:
        return False
    if href.startswith("mailto:"):
        return False
    lower = href.lower()
    return "verify" in lower or "confirm" in lower or ("torbox" in lower and "token" in lower)


def click_verification_link(page):
    print("Looking for verification link in email...")
    page.wait_for_timeout(5000)

    href = None

    # Check all frames first — email content is usually in an iframe
    for frame in page.frames:
        try:
            links = frame.locator("a")
            for i in range(links.count()):
                h = links.nth(i).get_attribute("href") or ""
                if is_verify_link(h):
                    href = h
                    break
        except:
            pass
        if href:
            break

    # Fallback on main page
    if not href:
        try:
            links = page.locator("a")
            for i in range(links.count()):
                h = links.nth(i).get_attribute("href") or ""
                if is_verify_link(h):
                    href = h
                    break
        except:
            pass

    if href:
        print(f"Navigating to: {href[:100]}...")
        page.goto(href, timeout=60000)
        print("Verification link opened!")
        return True

    print("Could not find verification link automatically.")
    print("Please click it manually in the browser window.")
    input("Press Enter after clicking the verification link...")
    return True


def verify(page):
    if not wait_for_torbox_email(page):
        return False
    return click_verification_link(page)
