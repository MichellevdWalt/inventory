Treehouse Project 4 - Python

Create a in-command-line app for an inventory. 

Import data from csv file.

Menu loop asks user to choose an option.

Options are:

Add an item to the inventory:
    Uses user input to add a row to the inventory database
    Validation checks to ensure the correct data is supplied
    Validation checks to ensure a product is not added more than once.
        Double products are checked for latest date and updated accordingly

Display an item using product_id
    Uses user input of a product id to display all information on that product currently in the database
    Validation to ensure user supplies a numeric value
    Validation to ensure id exists in the db

Back up inventory
    Backs up the inventory to a new csv file.