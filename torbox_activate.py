import time
import config


def activate(page):
    print("\n=== Step 4: Activating TorBox Free Trial ===")

    # Wait for verification redirect to complete
    print("Waiting for verification redirect...")
    for _ in range(30):
        time.sleep(2)
        if "torbox.app" in page.url and "login" not in page.url:
            print(f"On TorBox: {page.url}")
            break
        if "login" in page.url:
            try:
                page.locator("#email-input").fill("")
                page.locator("#password-input").fill(config.TORBOX_PASSWORD)
            except:
                pass
            print("Login needed — solve captcha if shown, then click submit.")
            input("Press Enter after logging in to TorBox...")
            break
    else:
        input("Press Enter after you're logged into TorBox...")

    # Go to dashboard — that's where the Pro trial button is
    print("Opening dashboard...")
    page.goto("https://torbox.app/dashboard", timeout=30000)
    page.wait_for_timeout(5000)

    print("Looking for TorBox Pro trial...")

    selectors = [
        "a:has-text('Try TorBox Pro')",
        "button:has-text('Try TorBox Pro')",
        "a:has-text('TorBox Pro')",
        "button:has-text('TorBox Pro')",
        "a:has-text('Start Free Trial')",
        "button:has-text('Start Free Trial')",
        "a:has-text('Free Trial')",
        "button:has-text('Free Trial')",
        "a:has-text('Upgrade')",
        "button:has-text('Upgrade')",
        "a[href*='subscription']",
        "a[href*='pricing']",
        "a[href*='upgrade']",
        "a[href*='pro']",
        "img[alt*='Pro']",
        "[class*='pro']",
        "[class*='Pro']",
    ]

    for selector in selectors:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=2000):
                text = btn.text_content() or selector
                print(f"Clicking '{text.strip()[:50]}'...")
                btn.click()
                page.wait_for_timeout(5000)
                print("Free trial activated!")
                return True
        except:
            pass

    print("Could not find free trial button automatically.")
    print("Please click 'Try TorBox Pro' on the dashboard manually.")
    input("Press Enter after activating the free trial...")
    return True
