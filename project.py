import pandas as pd
import csv
from datetime import date as dt
import argparse
import os, sys

global EXPENSE_FILE_NAME, CATEGORY_FILE_NAME, CSV_FILED_NAMES
EXPENSE_FILE_NAME = "expense-tracker.csv"
CATEGORY_FILE_NAME = "categories.txt"
CSV_FILED_NAMES = ["ID","DATE","CATEGORY","AMOUNT","DESCRIPTION"]

class Expense:
    def __init__(self, date, category, amount, description):
        self._id = generate_expense_id(EXPENSE_FILE_NAME)
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    @property
    def id(self):
        return self._id

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if date:
            self._date = dt.fromisoformat(date)
        else:
            raise ValueError("Missing date")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if category:
            if category in get_categories(CATEGORY_FILE_NAME):
                self._category = category
            else:
                raise ValueError("Category should be one of ", str(get_categories()))
        else:
            raise ValueError("Missing category")

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        if amount:
            self._amount = abs(float(amount))
        else:
            raise ValueError("Missing amount")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if description:
            self._description = description
        else:
            raise ValueError("Missing description")

    def add(self, EXPENSE_FILE_NAME):
        with open(EXPENSE_FILE_NAME, "a") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FILED_NAMES)
            writer.writerow({"ID": self.id,"DATE": self.date,"CATEGORY": self.category,"AMOUNT": self.amount,"DESCRIPTION": self.description})


def main():
    parser = argparse.ArgumentParser(prog="Expense Tracker", description="Track your daily expenses")
    parser.add_argument("-c", help="When creating a new expense tracker, list the expense categories that you need to track as a comma separate list. ex: 'Travel,Food,Housing'")
    parser.add_argument("-a", help="When adding a new expense to an existing expense tracker, provide the expense as a comma separated list of values. The values should be in the order of date, category, amount, description. ex: '2022-12-18','Food','10.50','Harveys'")
    parser.add_argument("-r", type=int, help="When removing an expense from an existing expense tracker, provide the 'ID' of the expense. ex: 2")
    parser.add_argument("-s", action="store_true", required=False, help="Provides stats from the existing expense tracker including total amount and sum of each category")
    parser.add_argument("--all", "-all","-al","--al",action="store_true", help="Provides all expenses in an existing expense tracker")
    parser.add_argument("--delete", action="store_true", help="Delete expense tracker including all expense data and category data. This operation cannot be reverted")
    args = parser.parse_args()
    try:
        if args.c:
            create_categories(CATEGORY_FILE_NAME, args.c)
            create_expense_tracker(EXPENSE_FILE_NAME)
        elif args.a:
            expense_raw = args.a.split(",")
            add_expense(EXPENSE_FILE_NAME, Expense(expense_raw[0].strip(),expense_raw[1].strip(),expense_raw[2].strip(),expense_raw[3].strip()))
        elif args.r:
            remove_expense(args.r)
        elif args.delete:
            delete_expense_tracker(EXPENSE_FILE_NAME,CATEGORY_FILE_NAME)

        if args.s:
            get_expenses_stats(EXPENSE_FILE_NAME)
        if args.all:
            get_all_expenses(EXPENSE_FILE_NAME)
    except (ValueError, FileNotFoundError, FileExistsError) as e:
        if "Invalid isoformat string" in str(e):
            sys.exit("ERROR: Invalid date format")
        sys.exit("ERROR: "+str(e))


def create_expense_tracker(EXPENSE_FILE_NAME):
    if not os.path.exists(EXPENSE_FILE_NAME):
        with open(EXPENSE_FILE_NAME, "w+") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FILED_NAMES)
            writer.writeheader()
        print("File "+EXPENSE_FILE_NAME+" created")
    else:
        raise FileExistsError("Expense tracker already available")


def create_categories(CATEGORY_FILE_NAME, categories):
    if not os.path.exists(CATEGORY_FILE_NAME):
        if categories:
            with open(CATEGORY_FILE_NAME, "w+") as file:
                file.write(categories)
            print("File "+CATEGORY_FILE_NAME+" created with the given categories: "+categories)
        else:
            raise ValueError("Pass at least one category")
    else:
        raise FileExistsError("Expense tracker already available with categories "+str(get_categories()))


def get_categories(CATEGORY_FILE_NAME):
    with open(CATEGORY_FILE_NAME) as file:
        for i, line in enumerate(file):
            if i == 0:
                categories = line.strip().split(",")
                return categories


def generate_expense_id(EXPENSE_FILE_NAME):
    df = pd.read_csv(EXPENSE_FILE_NAME)
    if len(df.index) > 0:
        new_id = df.loc[df.index[-1], "ID"]
        return new_id+1
    else:
        return 1


def add_expense(EXPENSE_FILE_NAME,expense):
    expense.add(EXPENSE_FILE_NAME)


def remove_expense(id):
    if os.path.exists(EXPENSE_FILE_NAME):
        df = pd.read_csv(EXPENSE_FILE_NAME)
        removing_id = df.loc[df.ID == id]["ID"]
        if not removing_id.empty:
            print("Removing expense with ID ", id)
            df = df.loc[df.ID != id]
            df.to_csv(EXPENSE_FILE_NAME, index=False)
        else:
            raise ValueError("Expense with ID "+str(id)+" doesn't exist")
    else:
        raise FileNotFoundError("No expense tracker found")


def get_all_expenses(EXPENSE_FILE_NAME):
    if os.path.exists(EXPENSE_FILE_NAME):
        df = pd.read_csv(EXPENSE_FILE_NAME)
        if len(df.index) > 0 :
            print(df.to_string(), end="\n")
        else:
            print("No expenses recorded yet")
    else:
        raise FileNotFoundError("No expense tracker found")


def get_expenses_stats(EXPENSE_FILE_NAME):
    if os.path.exists(EXPENSE_FILE_NAME):
        df = pd.read_csv(EXPENSE_FILE_NAME)
        if len(df.index) > 0:
            total = df["AMOUNT"].sum()
            print("\nTotal expenses: ", total, "\n")
            df = df.groupby("CATEGORY")['AMOUNT'].sum()
            print(df.to_string())
        else:
            print("No expenses recorded yet")
    else:
        raise FileNotFoundError("No expense tracker found")

def delete_expense_tracker(EXPENSE_FILE_NAME,CATEGORY_FILE_NAME):
    answer = input("Are you sure you want to delete the expense tracker including all data ? yes/no : ").strip()
    if answer == "yes":
        if os.path.exists(EXPENSE_FILE_NAME):
            os.remove(EXPENSE_FILE_NAME)
            print("File "+EXPENSE_FILE_NAME+ " deleted")
        else:
            raise ValueError("No "+EXPENSE_FILE_NAME+" file to delete")

        if os.path.exists(CATEGORY_FILE_NAME):
            os.remove(CATEGORY_FILE_NAME)
            print("File "+CATEGORY_FILE_NAME+ " deleted")
        else:
            raise ValueError("No "+CATEGORY_FILE_NAME+" file to delete")


if __name__ == "__main__":
    main()
