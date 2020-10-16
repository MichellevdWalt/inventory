from peewee import *
import datetime
import sqlite3
from sqlite3 import Error
import csv
from collections import OrderedDict
import re

db = SqliteDatabase("inventory.db")

class Product(Model):
    product_id = AutoField(primary_key = True)
    product_name = CharField(max_length=255, unique = True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def process_csv(file):
    """Processed csv data into dictionary"""
    with open(file, newline='') as csvfile:
        inventorylist = csv.DictReader(csvfile)
        rows = list(inventorylist)
    return rows

def csv_to_db(csv_list):
    """Cleans and pushes data from csv to the db. """
    print("Welcome to our inventory app.")
    while True:
        view = input("\nWould you like to see details of the csv import? [y/n]   ")
        if view.lower() == "y":
            for item in csv_list:
                try:
                    Product.create( product_name = item['product_name'], 
                                    product_quantity = int(item['product_quantity']), 
                                    product_price = int(float(item['product_price'][1:]) * 100),
                                    date_updated = datetime.datetime.strptime(item['date_updated'], '%m/%d/%Y')
                    )
                except IntegrityError:
                            print("\n{}.  --  Product name already exists.  ".format(item["product_name"]))
                            name_length = len(item["product_name"])
                            doubled_item = Product.get(product_name = item["product_name"])
                            if doubled_item.date_updated < datetime.datetime.strptime(item['date_updated'], '%m/%d/%Y'):
                                doubled_item.product_quantity = item["product_quantity"]
                                doubled_item.product_price = int(float(item['product_price'][1:]) * 100)
                                doubled_item.date_updated = datetime.datetime.strptime(item['date_updated'], '%m/%d/%Y')
                                doubled_item.save()
                                print(" "*(name_length+3) + "--  Product record was updated to latest information.")
                            elif doubled_item.date_updated > datetime.datetime.strptime(item['date_updated'], '%m/%d/%Y'):
                                print(" "*(name_length+3) + "--  Product record outdated. Record disguarded.")
                            else:
                                print(" "*(name_length+3) + "--  Product record duplicate. Record disguarded.")
            break
        elif view.lower() == "n":
            doubled = None
            for item in csv_list:
                try:
                    Product.create( product_name = item['product_name'], 
                                    product_quantity = int(item['product_quantity']), 
                                    product_price = int(float(item['product_price'][1:]) * 100),
                                    date_updated = datetime.datetime.strptime(item['date_updated'], '%m/%d/%Y')
                    )
                except IntegrityError:
                    doubled = True
            if doubled:
                print("\nImport information: Some items in the imported csv file already existed in the database.")
            break
        else:
            print("\nPlease enter either 'y' or 'n'.")

#Researched, https://www.sqlitetutorial.net/sqlite-python/creating-database/ 
def create_connection(db_file):
    """ Create a database connection to a SQLite database. Creates new one if it doesn't exist """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def restart():
    while True:
        add_more = input("\nDo you want to add another product? [yn]")
        if add_more.lower() == "y":
            add_more = True
            break
        elif add_more.lower() == "n":
            add_more = False
            break
        else:
            print("Please enter either a 'y' or 'n' ")
    if add_more:
        return True
    else:
        return False

def add_item():
    """Add an item to the inventory"""
    print("\nYou are adding a product to the inventory.")
    
    while True:
        name = None
        quantity = None
        price = None
        checked = None
        date = None
        add_more = None
        name = input("\nEnter product name:  ")

        while True:
            quantity = input("Enter quantity:  ")
            is_num = quantity.isnumeric()
            if is_num:
                break
            else:
                print("\nERROR: Please enter a valid number")
                continue

        while True:
            price = input("Enter Price of product in the format $00.00:  ")
            matched = bool(re.match("^\$([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$", price)) #RegEx adapted from https://regexlib.com/Search.aspx?k=currency&AspxAutoDetectCookieSupport=1
            if matched:
                break
            else:
                print("\n ERROR: Please use the correct format for your price\n")
                continue
        while True:
            date_correct = True
            date = input("Enter the date this was recorded in the format mm/dd/yyyy:  ")
            try:
                datetime.datetime.strptime(date, '%m/%d/%Y')
            except ValueError:
                print("\nERROR: Your date format seems to be in the incorrect format, please try again\n")
                date_correct = False
            if date_correct:
                break
            else:
                continue

        print("Please check the data provided: \nProduct Name: {} \nProduct Quantity: {} \nProduct Price: {} \nDate Updated: {}"
               .format(name, quantity, price, date))
        
        while True:
            checked = input("Are you happy to proceed? [yn]  ")
            if checked.lower() == "y" :
                try:
                    Product.create(product_name = name, 
                                product_quantity = int(quantity), 
                                product_price = int(float(price[1:]) * 100), 
                                date_updated = datetime.datetime.strptime(date, '%m/%d/%Y'))
                    print("Product was created")
                except IntegrityError:
                    print("\n{}.  --  Product name already exists.  ".format(name))
                    name_length = len(name)
                    doubled_item = Product.get(product_name = name)
                    if doubled_item.date_updated < datetime.datetime.strptime(date, '%m/%d/%Y'):
                        doubled_item.product_quantity = int(quantity)
                        doubled_item.product_price = int(float(price[1:]) * 100)
                        doubled_item.date_updated = datetime.datetime.strptime(date, '%m/%d/%Y')
                        doubled_item.save()
                        print(" "*(name_length+3) + "--  Product record was updated to latest information.")
            
                    elif doubled_item.date_updated > datetime.datetime.strptime(date, '%m/%d/%Y'):
                        print(" "*(name_length+3) + "--  Product record outdated. Record disguarded.")
                    else:
                        print(" "*(name_length+3) + "--  Product record duplicate. Record disguarded.")
                break
            elif checked.lower() == "n":
                continue
            else: 
                print("\nPlease enter either a 'y' or 'n'")
        
        add_more = restart()
        if add_more:
            continue
        else:
            break

def display_product():
    """Display a product by id"""
    do_continue = None
    product = None
    while True:
        input_id = input("\nPlease enter the id of the product you want to be displayed:   ")
        try:  
            product = Product.get(product_id = input_id )
        except Product.DoesNotExist:
            print("\nProduct not found, please try entering the id again.")
            continue
        if product:
            print("\nProduct ID: {} \nProduct Name: {} \nProduct Quantity: {} \nProduct Price: ${} \nLast Updated: {}"
                .format(product.product_id, product.product_name, product.product_quantity, product.product_price / 100, datetime.datetime.strftime(product.date_updated, '%m/%d/%Y')))
            while True:
                again = input("\nDo you want to display another product? [y/n]  ")
                if again.lower() == "y":
                    do_continue = True
                    break
                elif again.lower() == "n":
                    do_continue = False
                    break
                else:
                    print("\nPlease type either a 'y' or a 'n'")
            if do_continue:
                continue
            else:
                break
            



def create_backup():
    """Create a csv backup of the inventory"""
    with open('inventory_backup.csv', 'a') as csvfile:
        fieldnames = ['product_id', 'product_name', 'product_price',
                      'product_quantity', 'date_updated']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        products = Product.select()

        for product in products:
            writer.writerow({
                'product_id': product.product_id,
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_quantity': product.product_quantity,
                'date_updated': product.date_updated
            })
    print("\nBackup created as 'inventory_backup.csv' at {}".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")))

        
def menu_loop():
    """Handles interaction with user"""
    choice = None
    menu = OrderedDict([
        ('a', add_item),
        ('v', display_product),
        ('b', create_backup)
    ])
    while True:
        print("\n=======MAIN MENU=======")
        print("\nEnter 'q' at any point to quit.\n")
        print("Options:")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input("\nPlease choose an option [avb]:   ").lower().strip()
        if choice in menu:
            menu[choice]()
        elif choice.lower() == "q":
            break
        else:
            print("Please choose a valid option from the list")

    pass



if __name__ == '__main__':
    create_connection(r"./inventory.db")
    db.create_tables([Product], safe = True)

    inventory_list = process_csv('inventory.csv')
    csv_to_db(inventory_list)
    menu_loop()
