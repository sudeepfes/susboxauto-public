import config
import datetime

print("=== SusboxAuto Config Test ===\n")

print(f"✅ DuckDuckGo Email : {config.DUCKDUCKGO_EMAIL}")
print(f"✅ Stremio Email    : {config.STREMIO_EMAIL}")
print(f"✅ Total Proton Accounts : {len(config.PROTON_ACCOUNTS)}")

today = datetime.date.today().day % len(config.PROTON_ACCOUNTS)
acc = config.PROTON_ACCOUNTS[today]

print(f"\n📅 Today using Proton Account:")
print(f"   {acc['username']}@proton.me")

print("\n✅ Config looks good! You can now try the main script.")