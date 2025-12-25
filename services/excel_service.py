import os
import pandas as pd
from services.logger_service import log_step

def save_to_excel(recipients, output_path):
    log_step("Save recipients to Excel", "Pandas/OpenPyXL", "STARTED")

    # Ensure output directory exists
    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    df = pd.DataFrame(sorted(recipients), columns=["Recipient Email"])
    df.to_excel(output_path, index=False)

    log_step("Excel file saved successfully", output_path, "SUCCESS")
