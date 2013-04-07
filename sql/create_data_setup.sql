USE heydollar;

INSERT INTO people_people (first_name, last_name, birthdate, gender)
VALUES ('Eric', 'Connelly', '1986-05-27', 'MAL');

INSERT INTO spending_transactionType (name) VALUES ('debit'), ('credit'), ('transfer'), ('investment purchase'), ('investment sale');

INSERT INTO account_financialInstitution (name) VALUES ('Bank of America'), ('Chase'), ('American Express'), ('Fidelity'), ('Vanguard'), ('HSBC');

INSERT INTO account_accountType (name, base_sign) 
VALUES ('checking', 1), ('saving', 1), ('credit card', -1), ('personal investment', 1), ('retirement investment', 1);

INSERT INTO account_account (description, institution_id, type_id, owner_id, login_user, login_password) 
VALUES 
('BoA Checking', '1', '1', 1, '', ''), ('BoA Savings', '1', '2', 1, '', ''), 
('Chase Shared Checking', '2', '1', 1, '', ''), 
('Fidelity 401k', '4', '5', 1, '', ''), ('Fidelity Individual', '4', '4', 1, '', ''),
('Vanguard IRA', '5', '5', 1, '', ''), ('Vanguard Cash Holdings', '5', '5', 1, '', ''), ('Vanguard Personal', '5', '4', 1, '', ''),
('FIA Credit Card', '3', '3', 1, '', ''),
('HSBC Savings', '6', '2', 1, '', '');

INSERT INTO spending_category (name)
VALUES ('Groceries'), ('Fast Food'), ('Restaurants'), ('Bars'), ('Alcohol'), ('Coffee'), ('Treats'),
('Mortgage & Rent'), ('Phone'), ('Cable & Internet'), ('Electricity'), ('Gym'),
('Gifts'), ('Charity'),
('Home Furnishings'),
('Air Travel'), ('Hotel'),
('Doctor'), ('Dentist'), ('Sports Registration'), ('Sports Equipment'), ('Medication'),
('Personal Care'), ('Haircut'), ('Laundry'),
('Train'), ('Bus'), ('Taxi'), ('Public Transportation');