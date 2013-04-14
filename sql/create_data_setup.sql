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
('Train'), ('Bus'), ('Taxi'), ('Public Transportation'),
('Transfer'), ('Activity/Event');

INSERT INTO spending_transaction (post_date, amount, account_id, type_id, category_id, description, orig_description, notes)
VALUES
('2013-01-01', 43.00, 9, 1, 12, 'NYSC', 'NYSC-CORP SALES NY - 877-258-2311 NY 1276', ''),
('2013-01-01', 42.44, 11, 1, 3, 'Trudys Texas Star', 'TRUDY''S TEXAS STAR', ''),
('2013-01-01', 30, 1, 1, 25, 'Ny Tlr Cash', 'NY TLR cash withdrawal from CHK 0639 Banking Ctr CHELSEA BANKING CENTER...', 'Cash withdrawal of quarters'),
('2013-01-02', 9.81, 1, 1, 2, 'McDonalds', 'CHECKCARD 0101 MCDONALD''S F20728 GRAPEVINE TX 05140483001720036376044', ''),
('2013-01-02', 14.07, 1, 1, 7, 'Daily Juice', 'CHECKCARD 1231 DAILY JUICE AUSTIN TX 25536063002103001224797', ''),
('2013-01-02', 1.12, 1, 1, 30, 'Transfer to Regular Savings', 'KEEP THE CHANGE TRANSFER TO ACCT 5709 FOR 01/02/13', ''),
('2013-01-02', 0.89, 2, 2, 30, 'Keepthechange Acct Effective', 'KEEPTHECHANGE CREDIT FROM ACCT0639 EFFECTIVE 12/31', ''),
('2013-01-02', 600, 3, 1, 8, 'Winnie Lee', 'Chase QuickPay Electronic Transfer 3041410653 to WINNIE LEE', ''),
('2013-01-02', 23, 11, 1, 4, 'Elephant Room', 'ELEPHANT ROOM', ''),
('2013-01-02', 102.95, 11, 1, 3, 'Lamberts Downtown Barbequ', 'LAMBERTS DOWNTOWN BARBEQU', ''),
('2013-01-02', 46.21, 11, 1, 1, 'Morton', 'MORTON WILLIAMS BRO', ''),
('2013-01-03', 1180, 9, 1, 16, 'Picasso', 'PICASSO 3271641860014 - EL SEGUNDO CA 2477', 'Plane ticket to India'),
('2013-01-03', 24.5, 9, 1, 31, 'Tcktweb Thestuffyousho', 'TCKTWEB*THESTUFFYOUSHO - SAN FRANCISCO CA 5772', 'Stuff You Should Know TV event')
;











