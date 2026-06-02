import config
import datetime
import time
import traceback
from playwright.sync_api import sync_playwright

# ================== LOGGING ==================
def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    try:
        with open("automation.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

log("=== Susbox Auto - TorBox Stremio Automation Started ===")

# Daily Proton Rotation (with 5 accounts)
day = datetime.date.today().day % len(config.PROTON_ACCOUNTS)
selected = config.PROTON_ACCOUNTS[day]
log(f"Using Proton Account #{day+1}: {selected['username']}@proton.me")

config.PROTON_USERNAME = selected["username"]
config.PROTON_PASSWORD = selected["password"]

max_retries = 3

for attempt in range(max_retries):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--disable-gpu'
                ]
            )
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()

            log("Browser launched successfully")

            # Import and run modules
            import proton_verify
            import stremio_setup

            log("Starting Proton verification...")
            proton_verify.main() if hasattr(proton_verify, 'main') else proton_verify.run()

            log("Starting Stremio setup...")
            stremio_setup.main() if hasattr(stremio_setup, 'main') else stremio_setup.run()

            log("✅ Automation completed successfully for today!")
            browser.close()
            break  # Success, exit retry loop

    except Exception as e:
        log(f"Attempt {attempt+1} failed: {e}")
        log(traceback.format_exc())
        if attempt < max_retries - 1:
            log("Retrying in 30 seconds...")
            time.sleep(30)
        else:
            log("❌ All retries failed. Check automation.log for details.")
            log("Common fixes:")
            log("1. Check if credentials are correct in config.py")
            log("2. Make sure Proton accounts are verified")
            log("3. Try running locally with headless=False to see the browser")

    finally:
        try:
            browser.close()
        except:
            pass

log("Script finished.")
