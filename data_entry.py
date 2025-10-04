from datetime import datetime

date_format = "%m-%d-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_Str = input(prompt)
    # if user pressed default and user didn't type any input
    if allow_default and not date_Str:
        return datetime.today().strftime("%m-%d-%Y")
    
    try:
        # in datetime object format
        valid_date = datetime.strptime(date_Str, "%m-%d-%Y")
        # convert from datetime object to string interpretation
        return valid_date.strftime("%m-%d-%Y")  
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY.")
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            raise ValueError("Amount must be positive and non-zero")
        return amount       
    except ValueError as e:
        print(f"Invalid amount: {e}")
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES: 
        return CATEGORIES[category]
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()

def get_description():
    return input("Enter description (optional): ")