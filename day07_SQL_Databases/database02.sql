USE expense_tracker;

INSERT INTO expenses (title, amount, category)
VALUES
    ('Groceries', 370.00, 'Food'),
    ('Movie Tickets', 250.00, 'Entertainment'),
    ('Bus Ticket', 50.00, 'Travel');
SELECT * FROM expenses;

UPDATE expenses
SET amount = 400.00
WHERE title = 'Groceries';

DELETE FROM expenses
WHERE title = 'Bus Ticket';