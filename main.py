import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt
class CSV:
    # class variable
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"] 
    FORMAT = "%m-%d-%Y"

    # classmethod means it has access to class itself but not instance
    # 
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # data frame is from pandas
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)    

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        # "a" means append mode; adding to end of file
        # this with syntax is context manager that automatically closes file after block and deals with memory leaks
        with open(cls.CSV_FILE, mode='a', newline='') as csvfile:
            # csv writer takes dictionary and writes it into the csv file
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)   
        print("Entry added successfully.")

    @classmethod 
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        # use & instead of and for pandas dataframe
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        if filtered_df.empty:
            print("No transactions found in the specified date range.")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}: ")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")
        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (mm-dd-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)  

    
def plot_transactions(df):    
    df.set_index('date', inplace=True)
    # resample and make sure we have a row for each day ; "D" means daily frequency
    # sum different points; aggregate rows that have same date
    # reindex makes sure index is correct after operations; and that unfilled values are 0
    income_df=df[df['category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0)    
    expense_df=df[df['category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value=0)    
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label='Income', color='g') 
    plt.plot(expense_df.index, expense_df["amount"], label='Expesnse', color='r') 
    plt.xlabel('Date')
    plt.ylabel('Amount ($)')
    plt.title('Income and Expense Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add New Transaction")
        print("2. View Transactions and summary within date range")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")
        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date("Enter start date (mm-dd-yyyy): ")
            end_date = get_date("Enter end date (mm-dd-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").lower() == 'y':
                plot_transactions(df)
        elif choice == '3':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please select a valid option. Enter 1, 2, or 3")

# protecting function. Don't run main function unless directly running this file
if  __name__ == "__main__":
    main()
