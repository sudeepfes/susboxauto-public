import config
import datetime
import time
import traceback
import sys

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    try:
        with open("automation.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

log("=== SusboxAuto - TorBox Stremio Automation Started ===")

# Daily Rotation
day = datetime.date.today().day % len(config.PROTON_ACCOUNTS)
selected = config.PROTON_ACCOUNTS[day]
log(f"Using Proton Account #{day+1}: {selected['username']}@proton.me")

config.PROTON_USERNAME = selected["username"]
config.PROTON_PASSWORD = selected["password"]

max_retries = 3

for attempt in range(max_retries):
    try:
        log(f"Attempt {attempt+1}/{max_retries} started")

        # Import modules safely
        import proton_verify
        import stremio_setup

        log("Starting Proton verification...")
        if hasattr(proton_verify, 'main'):
            proton_verify.main()
        elif hasattr(proton_verify, 'run'):
            proton_verify.run()
        else:
            log("Warning: proton_verify has no main/run function")

        log("Starting Stremio setup...")
        if hasattr(stremio_setup, 'main'):
            stremio_setup.main()
        elif hasattr(stremio_setup, 'run'):
            stremio_setup.run()
        else:
            log("Warning: stremio_setup has no main/run function")

        log("✅ Automation completed successfully for today!")
        break  # Success

    except Exception as e:
        log(f"❌ Attempt {attempt+1} failed: {e}")
        log(traceback.format_exc())
        
        if attempt < max_retries - 1:
            log("Waiting 60 seconds before retry...")
            time.sleep(60)
        else:
            log("❌ All attempts failed.")
            log("Check automation.log for details.")
            log("Common fixes: Check credentials, internet, or run manually.")

log("Script finished.")