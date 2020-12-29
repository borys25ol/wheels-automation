import pytest

from spreadseet import GoogleSpreadsheetService


@pytest.fixture(scope="module")
def service():
    """
    Test fixture.
    """
    service = GoogleSpreadsheetService("Casino")
    return service
