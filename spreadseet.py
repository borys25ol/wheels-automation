import config

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSpreadsheetService:
    COLUMNS = {"grosvenorcasinos": {"index": 1, "range": "A2", "worksheet": 2}}

    def __init__(self, sheet_name=None):
        self.sheet = self.init_sheet(sheet_name=sheet_name)

    def append_data_row(self, values, column):
        """
        Extract data from Custom Search API
        and push it to Google Spreadsheet.
        """
        sheet = self._get_worksheet(index=self.COLUMNS[column]["worksheet"])

        values_in_sheet = self.get_column_data(column=column)
        if values_in_sheet:
            values_for_append = self.calculate_missing(
                old_numbers=values_in_sheet, new_numbers=values
            )
            insert_range = self._calculate_insert_range(
                in_column=len(values_in_sheet),
                append=len(values_for_append),
                column=column,
            )
            sheet.append_rows(
                values=[[value] for value in values_for_append[::-1]],
                table_range=insert_range,
            )
            return values_for_append
        else:
            sheet.append_rows(
                values=[[value] for value in values[::-1]],
                table_range=self.COLUMNS[column]["range"],
            )
            return values

    def get_column_data(self, column: str):
        """
        Extract all data in column and filter empty values.
        """
        sheet = self._get_worksheet(index=self.COLUMNS[column]["worksheet"])

        values_list = sheet.col_values(col=self.COLUMNS[column]["index"])

        values_list = list(filter(None, values_list))

        return values_list[::-1]

    def _calculate_insert_range(self, in_column, append, column):
        start_table_range = int(self.COLUMNS[column]["range"][1:])
        column_symbol = self.COLUMNS[column]["range"][0]
        return (
            f"{column_symbol}{start_table_range + in_column}:"
            f"{column_symbol}{start_table_range + in_column + append - 1}"
        )

    def _get_worksheet(self, index=-1):
        """
        Return already exist worksheet.
        """
        worksheet = self.sheet.get_worksheet(index)

        return worksheet

    @classmethod
    def calculate_missing(cls, old_numbers: list, new_numbers: list) -> list:
        """
        Return list with all first numbers
        from `new_numbers` list that not exist in `old_numbers` list.

        :param old_numbers: List of numbers from Google Spreadsheet.
        :param new_numbers: Scraped list of numbers from source website.
        """
        # Convert list of string from Google Spreadsheet numeric.
        old_numbers = [int(number) for number in old_numbers]

        # Find all sub-lists in `old_numbers`.
        all_sublist = []
        for index in range(3, len(old_numbers) + 1):
            sublist = old_numbers[:index]
            if cls.is_sublist(sublist, new_numbers):
                all_sublist.append(sublist)

        if not all_sublist:
            return new_numbers

        max_sublist = max(map(lambda v: len(v), all_sublist))

        return new_numbers[:-max_sublist]

    @staticmethod
    def is_sublist(sublist: list, check_list: list) -> bool:
        """
        Check if `sublist` is sublist of `check_list`.
        """
        check_list = "".join([str(char) for char in check_list])
        sublist = "".join([str(char) for char in sublist])
        if check_list.find(sublist) != -1:
            return True
        return False

    @staticmethod
    def init_sheet(sheet_name):
        """
        Initialize Google Spreadsheet API.
        """
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            config.CREDENTIALS_FILE,
            [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name)
        return sheet
