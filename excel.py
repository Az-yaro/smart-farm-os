import pandas as pd
from typing import List, Dict, Any

def export_excel_report(file_name: str, event_logs_data: List[Dict[str, Any]], tanks_data: List[Dict[str, Any]]) -> None:
    """
    Exports the farm's event log and tank data to an Excel report.

    Args:
        file_name (str): The base name for the Excel files.
        event_logs_data (List[Dict[str, Any]]): List of dictionaries representing event logs.
        tanks_data (List[Dict[str, Any]]): List of dictionaries representing tank data.
    """

    df_events: pd.DataFrame = pd.DataFrame(event_logs_data)
    df_tanks: pd.DataFrame = pd.DataFrame(tanks_data)

    # Export event log to Excel
    if not df_events.empty:
        df_events = df_events.sort_values(by="message", ascending=True)
        print(f"Event log data prepared for {file_name}.xlsx")
    else:
        print("No events to export.")

    # Export tanks data to Excel
    if not df_tanks.empty:
        print(f"Tank data prepared for {file_name}.xlsx")
    else:
        print("No tanks to export.")

    # Write to a single Excel file with multiple sheets
    if not df_events.empty or not df_tanks.empty:
        with pd.ExcelWriter(f"{file_name}.xlsx") as writer:
            if not df_events.empty:
                df_events.to_excel(writer, sheet_name="Events", index=False)
            if not df_tanks.empty:
                df_tanks.to_excel(writer, sheet_name="Tanks", index=False)
        print(f"Report exported to {file_name}.xlsx")
    else:
        print("No data to write to Excel report.")
