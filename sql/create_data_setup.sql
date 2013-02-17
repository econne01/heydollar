USE heydollar;

INSERT INTO heydollar_transactionType (name) VALUES ('debit'), ('credit'), ('transfer'), ('investment purchase'), ('investment sale');

INSERT INTO heydollar_financialInstitution (name) VALUES ('Bank of America'), ('Chase'), ('American Express'), ('Fidelity'), ('Vanguard'), ('HSBC');

INSERT INTO heydollar_accountType (name) VALUES ('checking'), ('saving'), ('credit card'), ('personal investment'), ('retirement investment');

INSERT INTO heydollar_account (description, institution_id, type_id) 
VALUES 
('BoA Checking', '1', '1'), ('BoA Savings', '1', '2'), 
('Chase Shared Checking', '2', '1'), 
('Fidelity 401k', '4', '5'), ('Fidelity Individual', '4', '4'),
('Vanguard IRA', '5', '5'), ('Vanguard Cash Holdings', '5', '5'), ('Vanguard Personal', '5', '4'),
('FIA Credit Card', '3', '3'),
('HSBC Savings', '6', '2');

INSERT INTO heydollar_category (name)
VALUES ('Groceries'), ('Fast Food'), ('Restaurants'), ('Bars'), ('Alcohol'), ('Coffee'), ('Treats'),
('Mortgage & Rent'), ('Phone'), ('Cable & Internet'), ('Electricity'), ('Gym'),
('Gifts'), ('Charity'),
('Home Furnishings'),
('Air Travel'), ('Hotel'),
('Doctor'), ('Dentist'), ('Sports Registration'), ('Sports Equipment'), ('Medication'),
('Personal Care'), ('Haircut'), ('Laundry'),
('Train'), ('Bus'), ('Taxi'), ('Public Transportation');