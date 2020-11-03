"""Pizza orders"""

import re
import sys

""" CONFIG """
# maximum number of pizzas in one order
max_pizzas = 5
# delivery charge (in $)
delivery_charge = 3.00
# list of dictionaries (pizzas) with name and price
pizzas_available = (
    {"name": "Hawaiian",             "price": 8.5},
    {"name": "Meat Lovers",          "price": 8.5},
    {"name": "Pepperoni",            "price": 8.5},
    {"name": "Ham & Cheese",         "price": 8.5},
    {"name": "Classic Cheese",       "price": 8.5},
    {"name": "Veg Hot 'n' Spicy",    "price": 8.5},
    {"name": "Beef & Onion",         "price": 8.5},
    {"name": "Seafood Deluxe",       "price": 13.5},
    {"name": "Summer Shrimp",        "price": 13.5},
    {"name": "BBQ Bacon & Mushroom", "price": 13.5},
    {"name": "BBQ Hawaiian",         "price": 13.5},
    {"name": "Italiano",             "price": 13.5},
)
""" END CONFIG """


# defines exception; this is to be raised when an order is cancelled
class CancelOrder(Exception):
    pass


# class with default order details
class Order():
    def __init__(self):
        self.pickup = True

        self.name = ""
        self.address = None
        self.phone = None

        self.number_pizzas = 0
        self.pizzas = []

        self.total_cost = 0


def get_input(regex, input_message=None, error_message=None, ignore_case=True):
    """Gets valid input, validated using regular expressions."""
    # loops until input is valid ("break" is called)
    while True:
        # input to validate, input prompt is as specified
        u_input = input(str(input_message))

        # check if the user wants to quit or cancel the order
        lower = u_input.lower()
        if lower == "qq" or lower == "quit":
            sys.exit()
        elif u_input == "cc" or u_input == "cancel":
            raise CancelOrder()

        # check if the input matches the regex provided
        if ignore_case:
            if re.match(regex, u_input, re.IGNORECASE):
                break
        else:
            if re.match(regex, u_input):
                break

        # if it doesn't match, and an error message has been specified
        if error_message:
            print(str(error_message))

    return u_input


def print_order(order):
    print("| Name: {}".format(order.name))
    print("| Order type: {}".format("Pickup" if order.pickup else "Delivery"))
    if not order.pickup:
        print("| Delivery address: {}".format(order.address))
        print("| Customer phone number: {}".format(order.phone))
    print("|\n| Order summary:\t\t\t\tPrice each:\tSubtotal:")
    for pizza in order.pizzas:
        print("| \t{}x {:<22}\t${:<6.2f}\t\t${:>5.2f}".format(
            pizza['amount'], pizza['name'],
            pizza['price'], pizza['price']*pizza['amount']))

    if not order.pickup:
            print("| \tDelivery charge\t\t\t\t\t$ {:>5.2f}".format(
                delivery_charge))
    print("| {:61}--------".format(""))
    print("| {:54} Total: ${:.2f}".format("", order.total_cost))


print("== Pizza Orders ==")
print("==  Order Manager  ==")
print("Enter 'CC' to cancel order, or 'QQ' to exit program at any time")
print("The first letter of a word is usually only required as input")
print("A word [enclosed] in brackets is the default option")

# list to hold all completed orders
orders = []

# sorts pizza list by price, then alphabetically
pizzas_available = sorted(
    pizzas_available,
    key=lambda k: (k["price"], k["name"]))

# keep getting orders, only exits through sys.exit()
while True:
    # try ... except to catch CancelOrder exception
    try:
        print("\nNew Order")
        order = Order()

        # get delivery/pickup type
        user_input = get_input(
            r"$|(?:P|D)",
            "Pickup or delivery? [Pickup]:",
            "Please enter a 'p' (pickup) or a 'd' (delivery)")
        if user_input.lower().startswith("d"):
            order.pickup = False

        # get name info
        order.name = get_input(
            r"[A-Z]+$",
            "Enter customer name:",
            "Name must only contain letters")

        # get address, phone number info (if the customer wants delivery)
        if not order.pickup:
            order.address = get_input(
                r"[ -/\w]+$",
                "Delivery address:",
                "Address must only contain alphanumeric characters")
            order.phone = get_input(
                r"\d+$",
                "Phone number:",
                "Phone number must only contain numbers")

        # get number of pizzas to order,
        # make sure it is more than 0,less than max_pizzas
        while True:
            user_input = get_input(
                r"\d$",
                "Number of pizzas to order:",
                "Must be a digit, 5 or less")
            user_input = int(user_input)
            if 0 < user_input <= max_pizzas:
                order.number_pizzas = user_input
                break
            else:
                print("Must be a digit, 5 or less (but more than 0)")

        # print menu (each pizza is assigned a number)
        print("\nWhat pizzas would you like to order?")
        for i, pizza in enumerate(pizzas_available):
            # each pizza's number is its index (i) + 1,
            # so the first pizza is 1
            print("{}: {}".format(str(i+1).zfill(2), pizza['name']))

        print("\nEnter your selection number for each pizza you want to buy")
        for i in range(order.number_pizzas):
            while True:
                string = "Pizza #{} of {}:".format(i+1, order.number_pizzas)
                user_input = get_input(
                    r"\d\d?$",
                    string,
                    "Pizza selection number must"
                    "correspond to those listed above")
                user_input = int(user_input)
                try:
                    if user_input == 0:
                        raise IndexError
                    # selects the pizza based on user_input
                    to_add = pizzas_available[user_input-1]

                    # if the pizza has already been ordered,
                    # increment the amount ordered
                    for ordered in order.pizzas:
                        if to_add["name"] == ordered["name"]:
                            ordered["amount"] += 1
                            break
                    # else add the pizza to the order list
                    else:
                        order.pizzas.append(to_add)
                        order.pizzas[-1]["amount"] = 1

                    # if there has been no error,
                    # input is valid, break from the while loop
                    break

                except IndexError:
                    print("Pizza selection number must"
                        "correspond to those listed above")

        order.total_cost = sum(
            pizza["price"]*pizza["amount"]
            for pizza in order.pizzas)
        if not order.pickup:
                order.total_cost += delivery_charge

        # add order to list of orders
        orders.append(order)
        print("\nOrder saved. Order was:")
        print_order(order)

        user_input = get_input(
            r"$|(?:Y|N|O).*",
            "Would you like to enter another order or view all"
                "previous orders? [Yes]/No/Orders:",
            "Only yes/no or \"orders\" responses allowed")
        if user_input.lower().startswith("o"):
            for i, order in enumerate(orders):
                print("-" * 73)
                print_order(order)
                if i == len(orders) + 1:
                    print("-" * 73)
        elif user_input.lower().startswith("n"):
            sys.exit()

    except CancelOrder:
        try:
            print("\nOrder cancelled")
            user_input = get_input(
                r"$|(?:Y|N).*",
                "Would you like to enter another order? [Yes]/No",
                "Only yes or no responses allowed")
            if user_input.lower().startswith("n"):
                sys.exit()

        except CancelOrder:
            print("Type 'QQ' to exit the program")
