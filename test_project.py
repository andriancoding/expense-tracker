import project as p
import pytest
import os

CATEGORY_FILE_NAME = "test-categories.txt"
EXPENSE_FILE_NAME = "test-expense-tracker.csv"

def test_create_expense_tracker():
    p.create_expense_tracker(EXPENSE_FILE_NAME)
    res = os.path.exists(EXPENSE_FILE_NAME)
    os.remove(EXPENSE_FILE_NAME)
    assert  res == True

def test_generate_expense_id():
    p.create_expense_tracker(EXPENSE_FILE_NAME)
    id1 = p.generate_expense_id(EXPENSE_FILE_NAME)
    os.remove(EXPENSE_FILE_NAME)
    assert id1 == 1

def test_get_categories():
    with pytest.raises(FileNotFoundError):
        p.get_categories(CATEGORY_FILE_NAME)

    p.create_categories(CATEGORY_FILE_NAME, "Food,Housing,Travel")
    assert p.get_categories(CATEGORY_FILE_NAME) == ['Food','Housing','Travel']
    os.remove(CATEGORY_FILE_NAME)
