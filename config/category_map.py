"""
This file contains a mapping of transaction categories to SUMMARY categories
"""

SUMMARY_CATEGORIES = [
    'Housing',
    'Food',
    'Child care',
    'Social & Enjoyment',
    'Upkeep',
    'Travel',
    'Insurance',
    'Taxes',
    'Other',
]

# This map is for semi-broad (mid-level detail) categories, grouped up to most broad summary categories
BROAD_TO_SUMMARY_CATEGORY_MAP = {
    # CHILD CARE
    'Child care': 'Child care',

    # FOOD
    'Food expense': 'Food',

    # HOUSING
    "Housing expense (Rent)": 'Housing',
    "Utility Bills": 'Housing',

    # INCOME
    # 'Passive Income': 'Income',
    # 'Salary': 'Income',

    # INSURANCE
    'Insurance': 'Insurance',

    # SOCIAL & ENJOYMENT
    'Social & Enjoyment': 'Social & Enjoyment',

    # TAXES
    'Taxes': 'Taxes',

    # TRAVEL
    'Travel': 'Travel',

    # UPKEEP
    'Fitness': 'Upkeep',
    'Maintenance Expense': 'Upkeep',

    # OTHER
    'Charity donations': 'Other',
    'Shopping': 'Other',
    'Other': 'Other',
}

# This map is for most detailed categories, grouped up to semi-broad (mid-level detail) categories
DETAIL_TO_SEMI_BROAD_CATEGORY_MAP = {
    "Auto & Transport": "Travel",
    "Baby Supplies": "Maintenance Expense",
    "Babysitter & Daycare": "Other",
    "Bank Fee": "Other",
    "Bills & Utilities": "Utility Bills",
    "Bonus": "Salary",
    "Books": "Shopping",
    "Bus": "Travel",
    "Business Services": "Other",
    "Buy": "",
    "Cable/Internet": "Utility Bills",
    "Cash & ATM": "Other",
    "Certification Fee": "Maintenance Expense",
    "Charity": "Charity donations",
    "Check": "Other",
    "Clothing": "Shopping",
    "Coffee Shops": "Social & Enjoyment",
    "Credit Card Fraud": "Other",
    "Credit Card Payment": "",
    "Dentist": "Maintenance Expense",
    "Deposit": "",
    "Dividend & Cap Gains": "Passive Income",
    "Doctor": "Maintenance Expense",
    "Donation": "Charity donations",
    "Education": "Maintenance Expense",
    "Electronics & Software": "Shopping",
    "Entertainment": "Social & Enjoyment",
    "Event Registration": "Fitness",
    "Extra Income": "Passive Income",
    "Eyecare": "Maintenance Expense",
    "Fast Food": "Food expense",
    "Federal Tax": "Taxes",
    "Finance Charge": "Other",
    "Financial": "Other",
    "Food & Dining": "Food expense",
    "From Savings": "",
    "Furnishings": "Housing expense (Rent)",
    "Gambling": "Other",
    "Gas & Fuel": "Travel",
    "Gift": "Shopping",
    "Gifts & Donations": "Shopping",
    "Groceries": "Food expense",
    "Gym": "Fitness",
    "Hair": "Maintenance Expense",
    "Health & Fitness": "Fitness",
    "Hide from Budgets & Trends": "",
    "Hobbies": "Social & Enjoyment",
    "Home": "Housing expense (Rent)",
    "Home Improvement": "Housing expense (Rent)",
    "Home Phone": "Utility Bills",
    "Home Services": "Housing expense (Rent)",
    "Home Supplies": "Housing expense (Rent)",
    "Hotel": "Travel",
    "Income": "Passive Income",
    "Interest Income": "Passive Income",
    "Interest Paid": "Other",
    "Internet": "Utility Bills",
    "Investments": "",
    "Late Fee": "Other",
    "Laundry": "Maintenance Expense",
    "Membership Dues": "Social & Enjoyment",
    "Misc Expenses": "Other",
    "Mobile Phone": "Utility Bills",
    "Mortgage & Rent": "Housing expense (Rent)",
    "Movie Theater": "Social & Enjoyment",
    "Movies & DVDs": "Social & Enjoyment",
    "Music": "Social & Enjoyment",
    "Music / Videos": "Social & Enjoyment",
    "Nails & Waxing": "Maintenance Expense",
    "New Clothes": "Shopping",
    "Office Supplies": "Shopping",
    "Other Insurance": "Insurance",
    "Parking": "Travel",
    "Paycheck": "Salary",
    "Personal Care": "Maintenance Expense",
    "Pet Food & Supplies": "Other",
    "Pharmacy": "Maintenance Expense",
    "Printing": "Other",
    "Public Transportation": "Travel",
    "Reimbursement": "Other",
    "Rental Car": "Travel",
    "Rental Car & Taxi": "Travel",
    "Restaurants": "Social & Enjoyment",
    "Rewards Program": "Passive Income",
    "Sell": "",
    "Seminars/Conferences": "Maintenance Expense",
    "Service & Parts": "Other",
    "Service Fee": "Other",
    "Shipping": "Other",
    "Shoes": "Shopping",
    "Shopping": "Shopping",
    "Spa & Massage": "Maintenance Expense",
    "Sporting Goods": "Shopping",
    "Sports Equipment": "Fitness",
    "State Tax": "Taxes",
    "Subscription/Member": "Social & Enjoyment",
    "Taxes": "Taxes",
    "Taxi": "Travel",
    "Television": "Social & Enjoyment",
    "To Investment": "",
    "To Savings": "",
    "Tools &amp; Supplies": "Housing expense (Rent)",
    "Toys": "Shopping",
    "Trade Commissions": "Other",
    "Train": "Travel",
    "Transfer": "",
    "Travel": "Travel",
    "Treats": "Social & Enjoyment",
    "Tuition": "Maintenance Expense",
    "Uncategorized": "Other",
    "Utilities": "Utility Bills",
    "Vacation": "Travel",
    "Wasted Cinema": "Other",
    "Withdrawal": "Other",
    "Gift (Received)": "Passive Income",
    "Fees & Charges": "Other",
    "Home Insurance": "Insurance",
    "Newspapers & Magazines": "Other",
    "Health Insurance": "Insurance",
    "Sports": "Social & Enjoyment",
}
