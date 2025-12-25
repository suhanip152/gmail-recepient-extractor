import threading
import yaml

from services.gmail_service import GmailService
from services.excel_service import save_to_excel
from services.logger_service import log_step
from ui.dashboard import start_dashboard


def run_pipeline():
    try:
        log_step("Load configuration", "YAML", "STARTED")
        with open("config/settings.yaml") as f:
            config = yaml.safe_load(f)
        log_step("Load configuration", "YAML", "SUCCESS")

        gmail = GmailService()

        log_step("Authenticate Gmail", "Gmail API", "STARTED")
        gmail.authenticate()
        log_step("Authenticate Gmail", "Gmail API", "SUCCESS")

        log_step("Fetch recipients from sender", "Gmail API", "STARTED")
        recipients = gmail.fetch_recipients_from_sender(
            config["sender_email"]
        )
        log_step("Fetch recipients from sender", "Gmail API", "SUCCESS")

        log_step("Save recipients to Excel", "Pandas/OpenPyXL", "STARTED")
        save_to_excel(recipients, config["output_excel_path"])
        log_step("Save recipients to Excel", "Pandas/OpenPyXL", "SUCCESS")

    except Exception as e:
        log_step("Pipeline execution", "System", f"FAILED: {str(e)}")


if __name__ == "__main__":
    worker = threading.Thread(target=run_pipeline, daemon=True)
    worker.start()

    start_dashboard()
