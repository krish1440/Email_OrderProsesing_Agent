import os

class SheetsHandler:
    def __init__(self, service):
        self.service = service
        self.spreadsheet_id = os.getenv('SPREADSHEET_ID')

    def append_row(self, values, range_name="Sheet1!A1"):
        """
        Appends a list of values as a new row in the Google Sheet.
        """
        if not self.spreadsheet_id:
            raise Exception("SPREADSHEET_ID not set in environment!")

        body = {
            'values': [values]
        }
        
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        return result

    def initialize_headers(self, headers, range_name="Sheet1!A1"):
        """
        Sets the first row of the sheet as headers.
        """
        body = {
            'values': [headers]
        }
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
