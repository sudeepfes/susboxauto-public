import config
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled', '--no-sandbox'])
    context = browser.new_context(viewport={'width': 1280, 'height': 800}, locale='en-US')
    page = context.new_page()

    # ── Step 1: Login to TorBox ──
    print("=== Step 1: Login to TorBox ===")
    page.goto("https://torbox.app/login", timeout=30000)
    page.wait_for_timeout(4000)

    page.locator("#email-input").fill(config.DUCKDUCKGO_EMAIL)
    page.locator("#password-input").fill(config.TORBOX_PASSWORD)
    page.wait_for_timeout(1500)

    submit_btn = page.locator("button[type='submit']")
    if submit_btn.is_disabled():
        print("Turnstile captcha detected — solve it in the browser, then click Submit")
        for _ in range(600):
            try:
                if page.url != "https://torbox.app/login" and "login" not in page.url:
                    print(f"Login detected! URL: {page.url}")
                    break
            except:
                break
            page.wait_for_timeout(500)
    else:
        submit_btn.click()
        page.wait_for_timeout(8000)
        print("Login submitted!")

    # ── Step 2: Copy TorBox API Key ──
    print("\n=== Step 2: Copy TorBox API Key ===")
    page.goto("https://torbox.app/settings", timeout=30000)
    page.wait_for_timeout(8000)
    print(f"Settings page loaded: {page.url}")

    api_key = None

    try:
        inputs = page.locator("input")
        count = inputs.count()
        print(f"Found {count} input elements")
        for i in range(count):
            try:
                val = inputs.nth(i).input_value()
                if len(val.strip()) > 20 and " " not in val and "@" not in val:
                    api_key = val.strip()
                    print(f"API key found in input[{i}]")
                    break
            except:
                pass
    except:
        pass

    if not api_key:
        for t in ["code", "pre", "input"]:
            try:
                els = page.locator(t)
                for i in range(els.count()):
                    try:
                        val = els.nth(i).text_content() or ""
                        val = val.strip()
                        if len(val) > 20 and " " not in val and "@" not in val:
                            api_key = val
                            print(f"API key found in <{t}>[{i}]")
                            break
                    except:
                        pass
                if api_key:
                    break
            except:
                pass

    if not api_key:
        api_key = page.evaluate("prompt('TorBox API key not found. Copy it from settings and paste:')")
        if not api_key:
            browser.close()
            exit()

    page.evaluate(f"navigator.clipboard.writeText('{api_key}')")
    print(f"API key: {api_key[:20]}... (copied to clipboard!)")

    # ── Step 3: Login to Stremio ──
    print("\n=== Step 3: Login to Stremio ===")
    page.goto("https://web.stremio.com/#/intro?form=login", timeout=30000)
    page.wait_for_timeout(8000)

    try:
        lb = page.locator("button:has-text('Log in')").first
        if lb.is_visible(timeout=3000):
            lb.click()
            page.wait_for_timeout(2000)
    except:
        pass

    try:
        page.locator("input[type='email']").first.wait_for(state="visible", timeout=10000)
        page.locator("input[type='email']").first.fill(config.STREMIO_EMAIL)
        page.locator("input[type='password']").first.fill(config.STREMIO_PASSWORD)
        sb = page.locator("button[type='submit']").first
        if sb.is_visible():
            sb.click()
        else:
            page.locator("button:has-text('Log in')").first.click()
        page.wait_for_timeout(8000)
        print("Stremio login submitted")
    except:
        print("Log in manually...")
        for _ in range(180):
            try:
                if "login" not in page.url and "intro" not in page.url:
                    print("Logged in!")
                    break
            except:
                break
            page.wait_for_timeout(500)

    # ── Step 4: Uninstall Torrentio addon ──
    print("\n=== Step 4: Uninstall Torrentio addon ===")
    page.goto("https://web.stremio.com/#/addons", timeout=30000)
    page.wait_for_timeout(8000)

    page.locator("body").wait_for(state="visible", timeout=10000)
    html = page.locator("body").inner_text()
    if "torrentio" in html.lower():
        print("Torrentio found on page — opening...")
        for sel in [
            "div:has-text('Torrentio')",
            "span:has-text('Torrentio')",
            "a:has-text('Torrentio')",
        ]:
            try:
                el = page.locator(sel).first
                if el.is_visible(timeout=2000):
                    el.click()
                    page.wait_for_timeout(3000)
                    for bs in ["button:has-text('Uninstall')", "button:has-text('Remove')"]:
                        try:
                            b = page.locator(bs).first
                            if b.is_visible(timeout=2000):
                                b.click()
                                page.wait_for_timeout(2000)
                                print("Torrentio uninstalled!")
                                break
                        except:
                            pass
                    break
            except:
                pass
    else:
        print("Torrentio not found (may already be removed).")

    # ── Step 5: Build manifest URL from API key and add to Stremio ──
    print("\n=== Step 5: Building manifest URL ===")
    manifest = f"https://torrentio.strem.fun/torbox={api_key}/manifest.json"
    print(f"Manifest: {manifest}")

    print("\n=== Step 6: Add addon to Stremio ===")
            break

    if not manifest_url:
        manifest_url = page.evaluate("prompt('Manifest URL not found. Paste it here:')")

    if manifest_url:
        manifest_url = manifest_url.replace("stremio://", "https://")
    print(f"Manifest URL: {manifest_url[:80] if manifest_url else 'N/A'}")

    # ── Step 6: Add addon to Stremio ──
    print("\n=== Step 6: Adding addon to Stremio ===")
    page.goto("https://web.stremio.com/#/addons", timeout=30000)
    page.wait_for_timeout(8000)

    print("Clicking Add Addon button...")
    clicked = False
    for sel in ["[class*='add-button']", "button[class*='add']", "button"]:
        try:
            btns = page.locator(sel)
            for i in range(btns.count()):
                try:
                    b = btns.nth(i)
                    if b.is_visible(timeout=500):
                        t = (b.text_content() or "").lower()
                        if "add" in t:
                            b.click()
                            page.wait_for_timeout(3000)
                            print(f"Clicked Add button [{i}]")
                            clicked = True
                            break
                except:
                    pass
            if clicked:
                break
        except:
            pass
        if clicked:
            break

    if not clicked:
        print("Click Add Addon manually...")
        page.wait_for_timeout(30000)

    try:
        inp = page.locator("input[type='text']").first
        if inp.is_visible(timeout=5000):
            inp.fill(manifest)
            page.wait_for_timeout(1000)
            inp.press("Enter")
            page.wait_for_timeout(3000)
            print("URL pasted and Enter pressed!")
    except:
        print("Paste URL manually...")
        page.wait_for_timeout(30000)

    page.wait_for_timeout(5000)

    print("Looking for Install button...")
    install_clicked = False
    for sel in [
        "button:has-text('Install')",
        "button:has-text('install')",
        "button:has-text('Add')",
        "button:has-text('add')",
        "button[type='submit']",
        "[class*='install'] button",
        "[class*='Install']",
        "button",
    ]:
        try:
            btns = page.locator(sel)
            for i in range(btns.count()):
                try:
                    b = btns.nth(i)
                    if b.is_visible(timeout=500):
                        txt = (b.text_content() or "").lower()
                        if txt in ("install", "add") or "install" in txt:
                            b.click()
                            page.wait_for_timeout(3000)
                            print(f"Install clicked! [{sel}][{i}]")
                            install_clicked = True
                            break
                except:
                    pass
            if install_clicked:
                break
        except:
            pass
        if install_clicked:
            break
        try:
            b = page.locator(sel).first
            if b.is_visible(timeout=2000):
                b.click()
                page.wait_for_timeout(3000)
                print("Add clicked!")
                break
        except:
            pass

    print("\n=== All done! ===")
    page.wait_for_timeout(30000)
    browser.close()
