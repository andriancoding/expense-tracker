# Expense Tracker
#### Video Demo:  <https://www.youtube.com/watch?v=DTxkNg3q2LI>
#### Description:

This program allows users to track expenses. Below are all the features of this program

##### Create a new expense tracker with a list of expense categories

To create a new expense tracker user needs to run the python program and pass the argument "-c"
along with a comma separated list of category values.
```
python project.py -c "Travel,Housing,Medicine,Transportation"
```
This will result in creating two files by the program. The first file will be "expense-tracker.csv" and the second file will be "categories.txt".

All expenses that the user adds will be recorded in the "expense-tracker.csv" file. "categories.txt" is
used as a placeholder for different categoies that the user wants to track.


#### Add a new expense to the expense tracker created

A new expense can be added to the expense tracker by passing the "-a" argument along with the expense information. Each expense requires a date, category, amount and description inorder to sucessfully add the expense to the expsense tracker. The value for the category should be one of the category values user entered during the creation of the expense tracker.
```
python project.py -a "2022-11-23",Housing,1450,Rent
```

#### Remove an existing expense from the expense tracker

An existing expense can be removed from the expense tracker by passing the "-r" argument along with the expense id that needs to be removed.
```
python project.py -r 1
```

#### Display all expenses from the expense tracker

Existing expense information from the expense tracker can be retrieved by passing the "--all" flag.
This flag can be included during creating a new expense tracker, adding a new expense or removing an expense.

```
python project.py --all
```

```
python project.py -r 1 --all
```

#### Generate basic stats including total amount for all expenses and total for each category of expenses

Total amount of expenses along with the total for each category of expenses can be retrived by passing the "--s" flag.

```
python project.py -s
```

#### Delete the expsense tracker including all expenses and category information

The expense tracker including all expenses and category information can be deleted by passing the flag "--delete". User will be prompted to confirm this operation including a message that the operation cannot be reverted.

```
python project.py --delete
```

#### Files

<strong>expense-tracker.csv</strong> : This file only gets created after the successful first run of the program with required arguments. This file holds all expense information entered by the user.

<strong>categories.txt</strong> : This file only gets created after the successful first run of the program with required arguments. This file holds the expense categories which are specified by the user during creation of the expense tracker.

#### Design choices debated

I have created an Expense class to hold expense information before storing them to a csv file.
As part of the program I had to implement several functions to support the features of this program. I was debating wheather to have them as methods inside the class as as @staticmethods or to have them as individual functions outside of the class. I ended up moving them outside of the class because most of these functions were operations on the csv file rather than an operation on the Expense object.
