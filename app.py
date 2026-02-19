import asyncio
import os
import smtplib
from email.mime.text import MIMEText
from playwright.async_api import async_playwright

EVENT_URL = "https://in.bookmyshow.com/sports/super-8-match-8-icc-men-s-t20-wc-2026/ET00474264"

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS")

alert_sent = False

def log(msg):
    print(msg, flush=True)

async def check_ticket():
    global alert_sent

    log("Checking ticket availability...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        log("Opening page...")
        await page.goto(EVENT_URL, timeout=60000)
        await page.wait_for_timeout(8000)

        content = await page.content()

        log("Page loaded successfully.")

        if not alert_sent:
            log("Triggering test email...")
            send_email()
            alert_sent = True

        await browser.close()

def send_email():
    log("Sending email...")

    subject = "🚨 Test Email - BMS Alert Working"
    body = f"Test successful!\n\nURL:\n{EVENT_URL}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAILS

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(
        SENDER_EMAIL,
        RECIPIENT_EMAILS.split(","),
        msg.as_string()
    )
    server.quit()

    log("Email sent successfully!")

async def main():
    log("Monitor started...")

    while True:
        try:
            await check_ticket()
        except Exception as e:
            log(f"Error occurred: {e}")

        log("Sleeping for 60 seconds...")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
