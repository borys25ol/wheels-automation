import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config


class GoogleSpreadsheetService:
    """
    Service for uploading and updating casino wheels numbers
    in specific Google Spreadsheet.
    """

    def __init__(self, sheet_name=None):
        self.sheet = self.init_sheet(sheet_name=sheet_name)

    def append_data_row(self, values, column):
        """
        Extract data from Custom Search API
        and push it to Google Spreadsheet.
        """
        sheet = self._get_worksheet(name=config.COLUMNS[column]["worksheet"])

        values_in_sheet = self.get_column_data(column=column)

        if values_in_sheet:
            values_for_append = self.calculate_missing(
                old_numbers=values_in_sheet, new_numbers=values
            )
            insert_range = self.calculate_insert_range(
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
                table_range=config.COLUMNS[column]["range"],
            )
            return values

    def get_column_data(self, column: str):
        """
        Extract all data in column and filter empty values.
        """
        sheet = self._get_worksheet(name=config.COLUMNS[column]["worksheet"])

        values_list = sheet.col_values(col=config.COLUMNS[column]["index"])
        values_list = list(filter(None, values_list))

        return values_list[::-1]

    def _get_worksheet(self, name):
        """
        Parse all sheets in current Spreadsheet and find index
        of sheet with given name.

        :param name: Name of sheet.

        :return Index of existing sheet in document.
        """
        sheet_data = self.sheet.fetch_sheet_metadata()
        sheets = sheet_data["sheets"]

        need_sheet = list(filter(lambda v: v["properties"]["title"] == name, sheets))

        try:
            worksheet = self.sheet.get_worksheet(need_sheet[0]["properties"]["index"])
        except IndexError:
            raise ValueError("Sheet not found!")

        return worksheet

    @classmethod
    def calculate_missing(cls, old_numbers: list, new_numbers: list):
        """
        Return list with all first numbers
        from `new_numbers` list that not exist in `old_numbers` list.

        :param old_numbers: List of numbers from Google Spreadsheet.
        :param new_numbers: Scraped list of numbers from source website.

        :return List of new numbers that not exist in `old_numbers`.
        """

        def is_sublist(lst1, lst2):
            """
            Check if `lst1` is exist in tail of `lst2`.
            """
            if len(lst2) == 1:
                return lst1[-1] == lst2[-1]

            new = "".join([str(char) for char in lst1[::-1]])
            old = "".join([str(char) for char in lst2[::-1]])

            return new.find(old) == 0

        old_numbers = [int(char) for char in old_numbers]

        if old_numbers == new_numbers:
            return []

        for i in range(1, len(old_numbers)):
            sublist = old_numbers[:-i]

            if is_sublist(lst1=new_numbers, lst2=sublist):
                return new_numbers[: -len(sublist)]

        return new_numbers

    @staticmethod
    def calculate_insert_range(in_column, append, column):
        """
        Return column range for inserting numbers.

        Example: "A2:A22"
        """
        start_table_range = int(config.COLUMNS[column]["range"][1:])

        column_symbol = config.COLUMNS[column]["range"][0]

        return (
            f"{column_symbol}{start_table_range + in_column}:"
            f"{column_symbol}{start_table_range + in_column + append - 1}"
        )

    @staticmethod
    def init_sheet(sheet_name):
        """
        Initialize Google Spreadsheet API.
        """
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        if config.IS_HEROKU:
            json_keyfile = json.loads(config.CREDENTIALS_JSON)
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                keyfile_dict=json_keyfile, scopes=scopes
            )
        else:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                filename=config.CREDENTIALS_FILE, scopes=scopes
            )

        client = gspread.authorize(credentials=credentials)

        sheet = client.open(sheet_name)

        return sheet
