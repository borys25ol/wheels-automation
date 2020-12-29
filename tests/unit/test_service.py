import pytest


TEST_OLD_NUMBERS_1 = [14, 0, 5, 32, 25, 13, 6, 20, 15, 0, 16, 34, 22, 4, 13, 16, 13]
TEST_NEW_NUMBERS_1 = [14, 0, 5, 32, 25, 13, 6, 20, 15, 0, 16]
TEST_RESULT_1 = []

TEST_OLD_NUMBERS_2 = [14, 0, 5, 32, 25, 13, 6, 20, 15, 0, 16, 34, 22, 4, 13, 16, 13]
TEST_NEW_NUMBERS_2 = [14, 14, 0, 5, 32, 25, 13, 6, 20, 15, 0, 16]
TEST_RESULT_2 = [14]

TEST_OLD_NUMBERS_3 = [14, 0, 5, 32, 25, 13, 6, 20, 15, 0, 16, 34, 22, 4, 13, 16, 13]
TEST_NEW_NUMBERS_3 = [12, 12, 14, 14, 0, 5, 32, 25, 13, 6]
TEST_RESULT_3 = [12, 12, 14]

TEST_OLD_NUMBERS_4 = [1, 2, 3, 4, 5]
TEST_NEW_NUMBERS_4 = [12, 12, 14, 14, 0, 5, 32, 25, 13, 6]
TEST_RESULT_4 = [12, 12, 14, 14, 0, 5, 32, 25, 13, 6]

TEST_OLD_NUMBERS_5 = [12, 14, 0, 5, 32, 25, 13, 6, 20, 15, 0, 16, 34, 22, 4, 13, 16, 13]
TEST_NEW_NUMBERS_5 = [12]
TEST_RESULT_5 = [12]

TEST_OLD_NUMBERS_6 = [12, 14, 0, 5, 32, 25, 13, 6, 20, 15, 0, 16, 34, 22, 4, 13, 16, 13]
TEST_NEW_NUMBERS_6 = [12, 14, 0]
TEST_RESULT_6 = []

TEST_OLD_NUMBERS_7 = [1, 2, 3, 4, 5]
TEST_NEW_NUMBERS_7 = [6, 7, 8, 9, 10]
TEST_RESULT_7 = [6, 7, 8, 9, 10]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([TEST_OLD_NUMBERS_1, TEST_NEW_NUMBERS_1], TEST_RESULT_1),
        ([TEST_OLD_NUMBERS_2, TEST_NEW_NUMBERS_2], TEST_RESULT_2),
        ([TEST_OLD_NUMBERS_3, TEST_NEW_NUMBERS_3], TEST_RESULT_3),
        ([TEST_OLD_NUMBERS_4, TEST_NEW_NUMBERS_4], TEST_RESULT_4),
        ([TEST_OLD_NUMBERS_5, TEST_NEW_NUMBERS_5], TEST_RESULT_5),
        ([TEST_OLD_NUMBERS_6, TEST_NEW_NUMBERS_6], TEST_RESULT_6),
        ([TEST_OLD_NUMBERS_7, TEST_NEW_NUMBERS_7], TEST_RESULT_7),
    ],
)
def test_valid_calculating_missing(test_input, expected, service):
    """
    Test valid extracting missing numbers from list.
    """
    result = service.calculate_missing(*test_input)
    assert result == expected
