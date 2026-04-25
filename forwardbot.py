"""
Simple Telegram Scheduled Post Bot
- Set a timer (in minutes/hours)
- Bot sends your message/post to your channel at that time
"""

import asyncio
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("7853887140", "0"))
API_HASH = os.getenv("8729399958:AAG9rR8uVjJkNJkRriatSZbPWFamdbSlz-o", "")
PHONE = os.getenv("PHONE", "")


async def main():
    client = TelegramClient("scheduler_session", API_ID, API_HASH)
    await client.start(phone=PHONE)

    print("\n✅ Logged in successfully!\n")

    # Step 1: Enter channel username or ID
    channel = input("Enter your channel username (e.g. @mychannel) or ID: ").strip()

    # Step 2: Enter the message
    print("\nEnter your message (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    message = "\n".join(lines).strip()

    if not message:
        print("❌ No message entered. Exiting.")
        return

    # Step 3: Set the timer
    print("\nSchedule the post:")
    print("  1. After X minutes")
    print("  2. After X hours")
    print("  3. At a specific time (HH:MM)")
    choice = input("Choose (1/2/3): ").strip()

    now = datetime.now()

    if choice == "1":
        mins = int(input("Send after how many minutes? ").strip())
        send_at = now + timedelta(minutes=mins)
    elif choice == "2":
        hrs = float(input("Send after how many hours? ").strip())
        send_at = now + timedelta(hours=hrs)
    elif choice == "3":
        t = input("Enter time (HH:MM, 24h format): ").strip()
        hour, minute = map(int, t.split(":"))
        send_at = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if send_at <= now:
            send_at += timedelta(days=1)  # next day if time already passed
    else:
        print("❌ Invalid choice. Exiting.")
        return

    wait_seconds = (send_at - now).total_seconds()

    print(f"\n⏰ Post scheduled for {send_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   ({int(wait_seconds // 60)} min {int(wait_seconds % 60)} sec from now)")
    print("\nWaiting... (keep this window open)\n")

    await asyncio.sleep(wait_seconds)

    await client.send_message(channel, message)
    print(f"✅ Post sent to {channel} at {datetime.now().strftime('%H:%M:%S')}!")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
    