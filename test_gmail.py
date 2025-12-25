from services.gmail_service import GmailService

def logger(step, tool, status):
    print(step, tool, status)

gmail = GmailService(logger)
gmail.authenticate()
emails = gmail.fetch_recipients_from_sender("example@gmail.com")
print(emails)
