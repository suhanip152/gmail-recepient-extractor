from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os
import base64
import email
import time
from services.logger_service import log_step

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class GmailService:
    def __init__(self):
        self.service = None

    def authenticate(self):
        log_step("Authenticate Gmail", "Gmail API", "STARTED")

        attempts = 0
        last_error = None
        while attempts < 3:
            try:
                creds = None
                if os.path.exists("auth/token.json"):
                    creds = Credentials.from_authorized_user_file("auth/token.json", SCOPES)

                if not creds or not creds.valid:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "auth/credentials.json", SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    with open("auth/token.json", "w") as token:
                        token.write(creds.to_json())

                self.service = build("gmail", "v1", credentials=creds)
                log_step("Authenticate Gmail", "Gmail API", "SUCCESS")
                return
            except Exception as exc:
                attempts += 1
                last_error = exc
                if attempts < 3:
                    log_step("Authenticate Gmail", "Gmail API", "RETRIED")
                    time.sleep(1)
                else:
                    log_step(f"Authenticate Gmail failed: {exc}", "Gmail API", "FAILED")
                    raise

    def fetch_recipients_from_sender(self, sender_email):
        log_step(f"Fetch emails from {sender_email}", "Gmail API", "STARTED")

        attempts = 0
        last_error = None
        while attempts < 3:
            try:
                recipients = set()
                results = self.service.users().messages().list(
                    userId="me",
                    q=f"from:{sender_email}"
                ).execute()

                messages = results.get("messages", [])

                for msg in messages:
                    msg_data = self.service.users().messages().get(
                        userId="me",
                        id=msg["id"],
                        format="raw"
                    ).execute()

                    raw = base64.urlsafe_b64decode(msg_data["raw"].encode("ASCII"))
                    email_msg = email.message_from_bytes(raw)

                    for header in ["To", "Cc", "Bcc"]:
                        if email_msg.get(header):
                            addresses = email_msg.get(header).split(",")
                            for addr in addresses:
                                recipients.add(addr.strip())

                log_step("Emails fetched & recipients extracted", "Gmail API", "SUCCESS")
                return recipients
            except Exception as exc:
                attempts += 1
                last_error = exc
                if attempts < 3:
                    log_step("Fetch emails from sender", "Gmail API", "RETRIED")
                    time.sleep(1)
                else:
                    log_step(f"Fetch emails from sender failed: {exc}", "Gmail API", "FAILED")
                    raise
