import csv
import json
import os


# Function to sum expenses for a given month from the CSV file
def sum_expenses_for_month(csv_file_path):
    total_expenses = 0.0
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip the first three lines
        next(reader)
        next(reader)
        next(reader)
        for row in reader:
            # Check if the row corresponds to the given month and year, and is a Debit transaction
            date, _, amount, _, transaction_type, status = row
            amount = amount.replace(',', '')
            if transaction_type.lower() == 'debit':
                total_expenses += float(amount)
    return total_expenses


# Function to update or create the JSON file with total expenses for the month
def update_expenses_json(json_file_path, month, total_expenses):
    expenses_data = {}

    # Check if the JSON file already exists
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            expenses_data = json.load(json_file)

    # Update the expenses data with the new total for the month
    expenses_data[month] = total_expenses

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(expenses_data, json_file, indent=4)


# Main program
if __name__ == "__main__":
    # Ask the user for the month
    month_input = input("Please enter the month (format YYYY-MM): ")

    # Specify your CSV file name
    csv_file_name = 'Transactions.csv'

    # Specify your JSON file name
    json_file_name = 'monthly_expenses.json'

    # Calculate the total expenses for the month
    total_month_expenses = sum_expenses_for_month(csv_file_name)
    print(f"Total expenses for {month_input}: {total_month_expenses}")

    # Update the JSON file with the total expenses
    update_expenses_json(json_file_name, month_input, total_month_expenses)
    print(f"Updated {json_file_name} with total expenses for {month_input}.")
