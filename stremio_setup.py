import config


def copy_torbox_api_key(page):
    print("[TorBox] Navigating to settings...")
    page.goto("https://torbox.app/settings", timeout=30000)
    page.wait_for_timeout(8000)

    print("[TorBox] Looking for API key...")

    try:
        inputs = page.locator("input")
        count = inputs.count()
        print(f"[TorBox] Found {count} input elements")
        for i in range(count):
            try:
                val = inputs.nth(i).input_value()
                if len(val.strip()) > 20 and " " not in val and "@" not in val:
                    api_key = val.strip()
                    print(f"[TorBox] API key: {api_key[:20]}...")
                    return api_key
            except:
                pass
    except:
        pass

    for t in ["code", "pre", "input"]:
        try:
            els = page.locator(t)
            for i in range(els.count()):
                try:
                    val = els.nth(i).text_content() or ""
                    val = val.strip()
                    if len(val) > 20 and " " not in val and "@" not in val:
                        print(f"[TorBox] API key: {val[:20]}...")
                        return val
                except:
                    pass
        except:
            pass

    print("[TorBox] Could not find API key automatically.")
    return page.evaluate("prompt('Paste your TorBox API key:')")


def login_stremio(page):
    print("\n[Stremio] Logging in...")
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
        page.wait_for_timeout(500)
        sb = page.locator("button[type='submit']").first
        if sb.is_visible():
            sb.click()
        else:
            page.locator("button:has-text('Log in')").first.click()
        page.wait_for_timeout(8000)
        print("[Stremio] Login submitted!")
    except:
        print("[Stremio] Log in manually...")
        for _ in range(180):
            try:
                if "login" not in page.url and "intro" not in page.url:
                    print("[Stremio] Logged in!")
                    break
            except:
                break
            page.wait_for_timeout(500)
    return True


def uninstall_torrentio(page):
    print("\n[Stremio] Opening addons...")
    page.goto("https://web.stremio.com/#/addons", timeout=30000)
    page.wait_for_timeout(8000)

    page.locator("body").wait_for(state="visible", timeout=10000)
    if "torrentio" not in (page.locator("body").inner_text() or "").lower():
        print("[Stremio] Torrentio not found (may already be removed).")
        return True

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
                print("[Stremio] Torrentio opened")
                for bs in ["button:has-text('Uninstall')", "button:has-text('Remove')"]:
                    try:
                        b = page.locator(bs).first
                        if b.is_visible(timeout=2000):
                            b.click()
                            page.wait_for_timeout(2000)
                            print("[Stremio] Torrentio uninstalled!")
                            break
                    except:
                        pass
                break
        except:
            pass
    return True


def install_torrentio(page, api_key):
    manifest = f"https://torrentio.strem.fun/torbox={api_key}/manifest.json"
    print(f"[Torrentio] Manifest URL: {manifest}")

    print("\n[Stremio] Adding addon...")
    page.goto("https://web.stremio.com/#/addons", timeout=30000)
    page.wait_for_timeout(8000)

    print("[Stremio] Clicking Add Addon button...")
    clicked = False
    for sel in ["[class*='add-button']", "button[class*='add']", "button"]:
        try:
            btns = page.locator(sel)
            for i in range(btns.count()):
                try:
                    b = btns.nth(i)
                    if b.is_visible(timeout=500):
                        if "add" in (b.text_content() or "").lower():
                            b.click()
                            page.wait_for_timeout(3000)
                            print(f"[Stremio] Add button [{i}] clicked!")
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
        print("[Stremio] Click Add Addon manually.")
        page.wait_for_timeout(30000)

    try:
        inp = page.locator("input[type='text']").first
        if inp.is_visible(timeout=5000):
            inp.fill(manifest)
            page.wait_for_timeout(1000)
            inp.press("Enter")
            page.wait_for_timeout(3000)
            print("[Stremio] URL pasted and Enter pressed!")
    except:
        print("[Stremio] Paste URL manually.")
        page.wait_for_timeout(30000)

    page.wait_for_timeout(5000)

    print("[Stremio] Looking for Install button...")
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
                            print(f"[Stremio] Install clicked! [{sel}][{i}]")
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

    print("[Torrentio] Done!")
    return True


def setup(page):
    print("\n=== Step 5: Setting up Torrentio on Stremio ===")

    api_key = copy_torbox_api_key(page)
    if not api_key:
        print("[TorBox] No API key. Skipping.")
        return False

    page.goto("https://torbox.app", timeout=30000)
    page.wait_for_timeout(2000)

    login_stremio(page)
    uninstall_torrentio(page)
    install_torrentio(page, api_key)

    print("\n=== Stremio + Torrentio setup complete! ===")
    return True
