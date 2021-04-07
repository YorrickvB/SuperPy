# Imports
import sys
import datetime
import csv
import argparse
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from os import path
from tkcalendar import Calendar, DateEntry
from matplotlib import pyplot as plt


# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.

""""
This section describes all functions called when the program is started.
"""
def startup():
    create_date_file()
    create_bought_file()
    create_sold_file()

#Check if there is already a file present containing the date set as current date. If not: create one.
def create_date_file(): 
    if path.exists('date.txt') == False:
        date = str(datetime.date.today())
        file = open('date.txt', 'w')
        file.write(date)
        file.close()
        
#Check if there is already a bought.csv file present. If not: create one
def create_bought_file(): 
    if path.exists('bought.csv') == False:
        with open('bought.csv', 'w', newline='') as csvfile: #let op de w voor write!
            bought_creation = csv.writer(csvfile)
            bought_creation.writerow(['id', 'product_name', 'buy_date', 'buy_price', 'expiration_date'])

#Check if there is already a sold.csv file present. If not: create one
def create_sold_file(): 
    if path.exists('sold.csv') == False:
        with open('sold.csv', 'w', newline='') as csvfile: #let op de w voor write!
            sold_creation = csv.writer(csvfile)
            sold_creation.writerow(['id', 'bought_id', 'sell_date', 'sell_price'])

"""
The section below describes all parsers, the elements used to communicate with the command line.
"""
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', help='Welcome to SuperPy. Please choose your command from the following items, or use one of the optional arguments below.')

parser.add_argument('-t', '--advance_time', type=int, metavar='', help='Advance time n days. Please specify the number of days with this argument')
parser.add_argument('-o', '--open_interface', action='store_true', help='Open the user interface')

sell_parser = subparsers.add_parser("sell", help='Sell an item')
buy_parser = subparsers.add_parser("buy", help='Buy an item')
report_parser = subparsers.add_parser("report", help='Create a report')

buy_parser.add_argument('--product_name', type=str, metavar='', required = True, help='Enter name of the bought product')
buy_parser.add_argument('--price', type=float, metavar='', required = True, help='Enter price of the bought product')
buy_parser.add_argument('--expiration_date', type=str, metavar='', required = True, help='Enter expiration date of the bought product in YYYY-mm-dd format')
buy_parser.add_argument('--buy_date', type=str, default='today', metavar='', required = False, help='Enter buy date of the bought product in YYYY-mm-dd format')

sell_parser.add_argument('--product_name', type=str, metavar='', required = True, help='Enter name of the sold product')
sell_parser.add_argument('--price', type=float, metavar='', required = True, help='Enter price of the sold product')

report_subparsers = report_parser.add_subparsers(dest='command', help='What kind of report would you like?')
report_inventory = report_subparsers.add_parser('inventory', help='Show inventory')
report_revenue = report_subparsers.add_parser('revenue', help='Calculate revenue')
report_profit = report_subparsers.add_parser('profit', help='Calculate profit')

report_inventory.add_argument('--now', action='store_true', help='Show current inventory')
report_inventory.add_argument('--yesterday', action='store_true', help='Show yesterday\s inventory')
report_inventory.add_argument('--date', type=str, help='Show inventory on date using YYYY-mm-dd format')
report_revenue.add_argument('--today', action='store_true', help='Show today\'s revenue')
report_revenue.add_argument('--yesterday', action='store_true', help='Show yesterday\'s revenue')
report_revenue.add_argument('--date', type=str, help='Show revenue on a specific date using YYYY-mm-dd format')
report_revenue.add_argument('--period', type=str, help='Show revenue for a specific period (YYYY-mm-dd/YYYY-mm-dd)') #Deze nog maken
report_profit.add_argument('--today', action='store_true', help='Show today\'s profit')
report_profit.add_argument('--yesterday', action='store_true', help='Show yesterday\'s profit')
report_profit.add_argument('--date', type=str, help='Show profit for a specific year (YYYY), month, (YYYY-mm) of day (YYYY-mm-dd)')
report_profit.add_argument('--period', type=str, help='Show profit for a specific period (YYYY-mm-dd/YYYY-mm-dd)') #deze nog maken
args = parser.parse_args()

"""
The functions below are used by the program to perform the various actions, either called for via the
command line, or using the user interface.
"""

#General overall helpful function to determine the date stored as 'today'.
#Takes no argument, returns the current date
def get_date():
    with open('Date.txt') as f:
        lines = f.readlines()
        current_date = datetime.datetime.strptime(lines[0], "%Y-%m-%d").date()
        return current_date

#The function used to advance the date stored as 'today'.
#Takes the current date and adds the specified number of days.
def advance_time(interval):
    #huidige datum pakken. Datum toevoegen, datum opslaan.
    current_date = get_date()
    new_date = str(current_date + datetime.timedelta(days = interval))
    file = open('date.txt', 'w')
    file.write(new_date)
    file.close()

#The main action for buying a product. Requires a name, price, expiration date and date of purchase
#Generates a new ID based on the last know ID and stores all values in a csv file.
def buy_item(product_name, buy_price, expiration_date, buy_date):
    product_name = product_name.lower()
    with open('bought.csv', 'r+', newline='') as file:
        reader = csv.reader(file)
        next(reader) 
        find_buy_id = [0]
        for row in reader:
            bought_id = int(row[0])
            find_buy_id.append(bought_id)
        bought_id = max(find_buy_id)+1
        if buy_date == 'today':
            date_bought = get_date()
        else:
            date_bought = buy_date
        bought_item = csv.writer(file)
        bought_item.writerow([bought_id, product_name, date_bought, buy_price, expiration_date])

#The main action for selling a product. Requires a name and price and stores these values with the Buy-ID in a csv file. 
def sell_item(product_name, sell_price):  
    date = get_date()
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader) 
        sold_items_list = [line[1] for line in sold_reader] 
        find_sold_id = [0] 
        sold_file.seek(0) 
        next(sold_reader)
        for row in sold_reader:
            sold_id = int(row[0])
            find_sold_id.append(sold_id) 
        sold_id = max(find_sold_id)+1 #Determine the new sell_ID by taking the highest currently present ID and adding +1
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader)
        #Now the function checks for availability of the item: were there more products with this name bought than sold, and did these products not expire?
        stock = [line[0] for line in bought_reader if line[1] == product_name and datetime.datetime.strptime(line[4], "%Y-%m-%d").date() >= date and line[0] not in sold_items_list] #Creates a list of all items with that product name that are not expired nor sold
        if stock:
            bought_id = stock[0]
            with open('sold.csv', 'a', newline='') as sold_file:
                sold_item = csv.writer(sold_file)
                sold_item.writerow([sold_id, bought_id, date, sell_price])
        else:
            print('Item not in stock')

#Funtion to check the inventory on a given moment, using one argument: the date that is requested.
#Result is stored as a separate csv file with name "Inventory {date}" and also printed on the command line
def check_inventory(time):
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader) 
        sold_items_list = [line[1] for line in sold_reader if datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= time] #Creates a list of ids for all items sold
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader) 
        stock = [[line[1].lower(), line[3], line[4]] for line in bought_reader if datetime.datetime.strptime(line[4], "%Y-%m-%d").date() > time and line[0] not in sold_items_list and datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= time] #Creates a list of all items that are not expired nor sold
        unique_stock =[]
        for i in stock:
            if i not in unique_stock:
                unique_stock.append(i)
                unique_stock = sorted(unique_stock)
        fields = ['Product name', 'Count', 'Buy Price', 'Expiration Date']
        with open(f'Inventory {time}.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(unique_stock)
        inventory = f'Inventory saved as Inventory {time}.csv \nProduct name \tCount \tBuy Price \tExpiration Date' #eindresultaat opmaken
        for row in unique_stock:
            inventory = inventory + f'\n{row[0]} \t\t{stock.count(row)} \t{row[1]} \t\t{row[2]}'
        print(inventory)
        return inventory

#The main function to determine the revenue in a given period. Either one day, in which case both required
#arguments are equal, or a given period with a start and end date.
#Function returns the total revenue to the function that called it.
def revenue_period(date, date_upper_limit): 
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_values = [float(line[3]) for line in sold_reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_upper_limit]
        total_revenue = sum(sold_values)
        return total_revenue

#Helper function to find all find the Buy_ID's of products sold in a certain period.
def find_sold_items(date, date_upper_limit): 
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_items_id = [line[1] for line in sold_reader if date <= datetime.datetime.strptime(line[2], "%Y-%m-%d").date() <= date_upper_limit]
        return sold_items_id

#The main function to determine the profit in a given period. Either one day, in which case both required
#arguments are equal, or a given period with a start and end date.Profit is determined by comparing the
#revenue in that period to the costs of buying all products that are sold in that period.
#Function returns the total profit to the function that called it.
def profit(date, date_upper_limit):
    total_revenue = revenue_period(date, date_upper_limit)
    sold_items_id = find_sold_items(date, date_upper_limit)
    with open('bought.csv', newline='') as bought_file:
        bought_reader = csv.reader(bought_file)
        next(bought_reader) 
        costs = [float(line[3]) for line in bought_reader if line[0] in sold_items_id]
        total_costs = sum(costs)
        total_profit = total_revenue - total_costs
        return total_profit

#Helper function to identify the right time period to be used with the various functions, based on
#input from either the command line or the user interface
def determine_period(time):
    date = get_date()
    date_upper_limit = date
    if time == 'today' or time == 'now':
        date_upper_limit = get_date()
    elif time == 'yesterday':
        date = date + datetime.timedelta(days = -1)
        date_upper_limit = date
    else: #following lines based on YYYY-mm-dd format, as required.
        resolution = time.count('-') #Check if either a year, year-month or year-month-day is specified
        if resolution == 2:  #for year-month-day
            date = datetime.datetime.strptime(time, "%Y-%m-%d").date()
            date_upper_limit = date
        elif resolution == 1: #for year-month
            date = datetime.datetime.strptime(time, "%Y-%m").date()
            date_upper_limit = date
            date_month = date.strftime("%B")
#determine last day of the month, taking into account
#possible 28 (feb non-leap year) 29 (feb leap year), 30 of 31 day possibilities.
            for i in range(31): 
                date_upper_limit = date_upper_limit + datetime.timedelta(days = +1)
                if date_upper_limit.month > date.month:
                    date_upper_limit = date_upper_limit + datetime.timedelta(days = -1)
                    break
        elif resolution == 0 and len(time) == 4: #if only a year is given
            date = datetime.datetime.strptime(time, "%Y").date()
            date_upper_limit = datetime.date(date.year, 12, 31)
        elif resolution == 4 and len(time) == 21: #if a certain period is given in format YYYY-mm-dd-YYY-mm-dd
            date = datetime.datetime.strptime(time[0:9], "%Y").date()
            date_upper_limit = datetime.datetime.strptime(time[10:21], "%Y").date()
    return date, date_upper_limit

"""
The functions below are needed for the (optional) user interface to function properly.
"""
#This function describes the main window, with all the buy/sell/report options on the main screen.
def open_interface():
    window = Tk()
    window.geometry('650x450')
    window.title("SuperPy")
    date = get_date()
    lbl = Label(window, text="Welcome to SuperPy!")
    lbl.grid(column=0, row=0)
    lbl2 = Label(window, width=15, fg='red', text="Buy")
    lbl2.grid(column=0, row=1)
    lbl3 = Label(window, width=15,text="Product name")
    lbl3.grid(column=0, row=2, sticky=W)
    lbl4 = Label(window, width=15,text="Price")
    lbl4.grid(column=1, row=2, sticky=W)
    lbl5 = Label(window, width=15,text="Expiration date")
    lbl5.grid(column=2, row=2, sticky=W)
    buy_name = StringVar()
    buy_name_entry = ttk.Entry(window, width=10, textvariable=buy_name)
    buy_name_entry.grid(column=0, row=3)
    buy_price = StringVar()
    buy_price_entry = ttk.Entry(window, width=5, textvariable=buy_price)
    buy_price_entry.grid(column=1, row=3)
    buy_cal = DateEntry(window, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    buy_cal.grid(column=2, row=3)
    buy_cal.set_date(date)
    btn1 = Button(window, text="Buy product", command=lambda: command_buy_product(buy_name_entry, buy_price_entry, buy_cal, window))
    btn1.grid(column=3, row=3)
    blank1 = Label(window, width=15, fg='red', text=" ")
    blank1.grid(column=0, row=4, sticky=S)
    lbl6 = Label(window, width=15, fg='red', text="Sell")
    lbl6.grid(column=0, row=5, sticky=S)
    lbl7 = Label(window, width=15,text="Product name")
    lbl7.grid(column=0, row=6, sticky=W)
    lbl8 = Label(window, width=15,text="Price")
    lbl8.grid(column=1, row=6, sticky=W)
    item_list = create_sell_items()
    items_for_sale = StringVar()
    items_for_sale.set(item_list[0])
    select_sell = OptionMenu(window, items_for_sale, *item_list)
    select_sell.grid(column=0, row=7)
    sell_price = StringVar()
    sell_price_entry = ttk.Entry(window, width=5, textvariable=sell_price)
    sell_price_entry.grid(column=1, row=7)
    btn2 = Button(window, text="Sell product", command=lambda: command_sell_product(items_for_sale, sell_price_entry, window))
    btn2.grid(column=2, row=7)
    blank2 = Label(window, width=15, fg='red', text=" ")
    blank2.grid(column=0, row=8, sticky=W)
    lbl9 = Label(window, width=15, fg='red', text="Report")
    lbl9.grid(column=0, row=9, sticky=W)
    button_inventory = Button(window, text="Inventory", command= lambda: inventory_window(window))
    button_inventory.grid(column=0, row=10)
    button_revenue = Button(window, text="Revenue", command=lambda: revenue_window(window))
    button_revenue.grid(column=1, row=10)
    button_profit = Button(window, text="Profit", command= lambda: profit_window(window))
    button_profit.grid(column=2, row=10)
    blank3 = Label(window, width=15, fg='red', text=" ")
    blank3.grid(column=0, row=11, sticky=W)
    lbl10 = Label(window, width=15, fg='red', text="Date")
    lbl10.grid(column=0, row=12, sticky=W)
    lbl11 = Label(window, width=15, text="Current date")
    lbl11.grid(column=0, row=13, sticky=W)
    lbl12 = Label(window, width=15, text="Advance time\n(days)")
    lbl12.grid(column=1, row=13, sticky=W)
    lbl13 = Label(window, width=15, text="Advance time\n(select date)")
    lbl13.grid(column=4, row=13, sticky=W)
    date_label = Label(window, width=15, text=f"{date}") 
    date_label.grid(column=0, row=14, sticky=W)
    date_advance = StringVar()
    date_advance_entry = ttk.Entry(window, width=10, textvariable=date_advance)
    date_advance_entry.grid(column=1, row=14)
    button_date = Button(window, text="Submit", command=lambda: command_advance_time(date_advance_entry, window))
    button_date.grid(column=2, row=14)
    lbl14 = Label(window, width=15, text="or")
    lbl14.grid(column=3, row=14, sticky=W)
    date_select = Button(window, text="Select date", command=lambda: select_date(window, 'advance_time'))
    date_select.grid(column=4, row=14)
    blank4 = Label(window, width=15, fg='red', text=" ")
    blank4.grid(column=0, row=15, sticky=W)
    lbl10 = Label(window, width=15, fg='red', text="Results\nlast week")
    lbl10.grid(column=0, row=16, sticky=W)
    last_week_r = Button(window, text="Last weeks revenue", command=lambda: last_week('revenue'))
    last_week_r.grid(column=0, row=17)
    last_week_p = Button(window, text="Last weeks profit", command=lambda: last_week('profit'))
    last_week_p.grid(column=1, row=17)
    window.mainloop()

def refresh_window(window):
    window.destroy()
    open_interface()
    
#Function used to create a list of items for sale, to help the user specify what has been sold.
    #Only items in stock and with a suitable expiration date are shown.
def create_sell_items():
    date = get_date()
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)
        sold_list = [line[1] for line in sold_reader]
    with open('bought.csv', newline='') as bought_file: 
        bought_reader = csv.reader(bought_file)
        next(bought_reader)
        stock = [line[1] for line in bought_reader if datetime.datetime.strptime(line[4], "%Y-%m-%d").date() >= date and line[0] not in sold_list] #Creates a list of all items with that product name that are not expired nor sold
        stock = sorted(stock)
        unique_stock_names =["Select item"] #dubbele waarden verwijderen uit de lijst
        for i in stock:
            if i not in unique_stock_names:
                unique_stock_names.append(i)
                unique_stock = sorted(unique_stock_names)
    return unique_stock_names

#These functions are calles when one of the buttons on the main screen are pressed.
def command_buy_product(buy_name_entry, buy_price_entry, buy_cal, window): 
    product = buy_name_entry.get()
    if product == '':
        messagebox.showerror("Error", "Please provide a valid name")
        return
    price_box = buy_price_entry.get()
    if price_box == '':
        messagebox.showerror("Error", "Please provide a valid price")
        return
    price = float(price_box)
    ex_date =  buy_cal.get_date()
    buy_name_entry.delete(0,END)
    buy_price_entry.delete(0,END)
    buy_date = get_date()
    buy_item(product, price, ex_date, buy_date)
    messagebox.showerror("Bought!", f"{product} bought for {price}!")
    refresh_window(window)

def command_sell_product(items_for_sale, sell_price_entry, window): 
    product = items_for_sale.get()
    if product == 'Select item':
        messagebox.showerror("Error", "Please select item to sell")
        return
    price_box = sell_price_entry.get()
    if price_box == '':
        messagebox.showerror("Error", "Please provide a valid price")
        return
    price = float(price_box)
    sell_price_entry.delete(0,END)
    sell_item(product, price)
    messagebox.showinfo("Sold!", f"{product} sold for {price}!")
    refresh_window(window)

def command_advance_time(date_advance_entry, window):
    interval_box = date_advance_entry.get()
    if interval_box == '':
        messagebox.showerror("Error", "Please provide a number")
        return
    interval = int(interval_box)
    advance_time(interval)
    date = get_date()
    messagebox.showinfo("Time travel!", f"Date set to {date}")
    refresh_window(window)

# An extra feature of the main screen: to provide insight in last week's financial results, two buttons
# are added: one for last week's profit, another for revenue. This function generates a bar graph with these stats
def last_week(command):
    date_upper_limit = get_date()
    date = date_upper_limit + datetime.timedelta(days = -6)
    with open('sold.csv', 'r+', newline='') as sold_file:
        sold_reader = csv.reader(sold_file)
        next(sold_reader)      
        dates_list = []
        revenue_list = []
        profit_list = []
        if command == 'revenue':
            while date <= date_upper_limit:
                dates_list.append(str(date.strftime('%a')))
                revenue = revenue_period(date, date)
                revenue_list.append(revenue)
                date = date + datetime.timedelta(days = +1)
        elif command == 'profit':
            while date <= date_upper_limit:
                dates_list.append(str(date.strftime('%a')))
                daily_profit = profit(date, date)
                profit_list.append(daily_profit)
                date = date + datetime.timedelta(days = +1)
        y_axis = revenue_list if command == 'revenue' else profit_list
        plt.bar(dates_list, y_axis)
        plt.title(f'Last weeks {command}')
        plt.xlabel("Date")
        plt.ylabel(f"{command}")
        plt.show()

"""
The functions below create a new, Toplevel window when more input is required to perform an action.
"""
#Creates a window to ask for more details on the inventory report
def inventory_window(window):
    inventory_screen = Toplevel(window)
    i_lbl = Label(inventory_screen, text="Select an option")
    date = get_date()
    yesterday = date + datetime.timedelta(days = -1)
    i_lbl.grid(column=0, row=0)
    i_btn1 = Button(inventory_screen, text="Now", command= lambda: messagebox.showinfo(f"Inventory on {date}", (check_inventory(date)))) #check_inventory(date)) #lambda: set_date(cal))
    i_btn1.grid(column=0, row=1)
    i_btn2 = Button(inventory_screen, text="Yesterday", command= lambda: messagebox.showinfo(f"Inventory on {yesterday}", (check_inventory(yesterday)))) #lambda: set_date(cal))
    i_btn2.grid(column=1, row=1)
    i_btn3 = Button(inventory_screen, text="Select date", command= lambda: select_date(inventory_screen, 'inventory')) #lambda: set_date(cal))
    i_btn3.grid(column=2, row=1)
    i_btn4 = Button(inventory_screen, text="Close screen", command= lambda: inventory_screen.destroy()) #lambda: set_date(cal))
    i_btn4.grid(column=0, row=2)

#Creates a window to ask for more details on the revenue report
def revenue_window(window):  
    revenue_screen = Toplevel(window)
    date = get_date()
    yesterday = date + datetime.timedelta(days = -1)
    r_lbl = Label(revenue_screen, text="Select an option")
    r_lbl.grid(column=0, row=0)
    r_btn1 = Button(revenue_screen, text="Today", command= lambda: revenue_result.set(f'Today\'s revenue: {revenue_period(date, date)}')) #lambda: set_date(cal))
    r_btn1.grid(column=0, row=1)
    r_btn2 = Button(revenue_screen, text="Yesterday", command= lambda: revenue_result.set(f'Yesterday\'s revenue: {revenue_period(yesterday, yesterday)}')) #lambda: set_date(cal))
    r_btn2.grid(column=1, row=1)
    r_btn3 = Button(revenue_screen, text="Select date", command= lambda: select_date(revenue_screen, 'revenue')) #lambda: set_date(cal))
    r_btn3.grid(column=2, row=1)
    r_btn3 = Button(revenue_screen, text="Select period", command= lambda: select_period(revenue_screen, 'revenue')) #lambda: set_date(cal))
    r_btn3.grid(column=3, row=1)
    r_btn5 = Button(revenue_screen, text="Close screen", command= lambda: revenue_screen.destroy()) #lambda: set_date(cal))
    r_btn5.grid(column=0, row=2)
    revenue_result = StringVar()
    revenue_result_entry = ttk.Entry(revenue_screen, width=25, textvariable=revenue_result)
    revenue_result_entry.grid(column=0, row=3)

#Creates a window to ask for more details on the profit report
def profit_window(window):
    profit_screen = Toplevel(window)
    date = get_date()
    yesterday = date + datetime.timedelta(days = -1)
    p_lbl = Label(profit_screen, text="Select an option")
    p_lbl.grid(column=0, row=0)
    p_btn1 = Button(profit_screen, text="Today", command= lambda: profit_result.set(f'Today\'s profit: {profit(date, date)}')) #lambda: set_date(cal))
    p_btn1.grid(column=0, row=1)
    p_btn2 = Button(profit_screen, text="Yesterday", command= lambda: profit_result.set(f'Yesterday\'s profit: {profit(yesterday, yesterday)}')) #lambda: set_date(cal))
    p_btn2.grid(column=1, row=1)
    p_btn3 = Button(profit_screen, text="Select date", command= lambda: select_date(profit_screen, 'profit')) #lambda: set_date(cal))
    p_btn3.grid(column=2, row=1)
    p_btn4 = Button(profit_screen, text="Select period", command= lambda: select_period(profit_screen, 'profit')) #lambda: set_date(cal))
    p_btn4.grid(column=3, row=1)
    p_btn5 = Button(profit_screen, text="Close screen", command= lambda: profit_screen.destroy()) #lambda: set_date(cal))
    p_btn5.grid(column=0, row=2)    
    profit_result = StringVar()
    profit_result_entry = ttk.Entry(profit_screen, width=25, textvariable=profit_result)
    profit_result_entry.grid(column=0, row=3)    

#Creates a new screen to ask for a specific date, linked to one of the actions.
    #like changing the current date of specifying the desired date for one of the reports
def select_date(window, command):
    date_screen = Toplevel(window)
    d_lbl = Label(date_screen, text="Select prefered date")
    d_lbl.grid(column=0, row=0)
    d_lbl2 = Label(date_screen, width=15, text="Click here")
    d_lbl2.grid(column=0, row=1)
    cal = DateEntry(date_screen, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    cal.grid(column=0, row=2)
    current_date = get_date()
    cal.set_date(current_date)
    d_btn1 = Button(date_screen, text="Set date", command= lambda: [set_date(cal, command, window), date_screen.destroy()])
    d_btn1.grid(column=0, row=3)

def set_date(cal, command, window): 
    date = cal.get_date() 
    if command == 'inventory':
        messagebox.showinfo(f"Inventory on {date}", (check_inventory(date)))
    if command == 'revenue':
        total_revenue = revenue_period(date, date)
        messagebox.showinfo("Revenue", f"Total revenue on {date}: {total_revenue}")
    if command == 'profit':
        total_profit = profit(date, date)
        messagebox.showinfo("Profit", f"Total profit on {date}: {total_profit}")
    if command == 'advance_time':
        date = str(date)
        file = open('date.txt', 'w')
        file.write(date)
        file.close()
        messagebox.showinfo("Time travel!", f"Date set to {date}")
        refresh_window(window)

#Creates a new screen to ask for a specific period, linked to one of the actions.
    #like specifying the desired period for one of the reports   
def select_period(window, command):
    period_screen = Toplevel(window)
    d_lbl = Label(period_screen, text="Select prefered period")
    d_lbl.grid(column=0, row=0)
    d_lbl2 = Label(period_screen, width=15, text="From")
    d_lbl2.grid(column=0, row=1)
    cal1 = DateEntry(period_screen, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    cal1.grid(column=0, row=2)
    current_date = get_date()
    cal1.set_date(current_date)
    d_lbl2 = Label(period_screen, width=15, text="To")
    d_lbl2.grid(column=1, row=1)
    cal2 = DateEntry(period_screen, date_pattern='yyyy-mm-dd', width=12, background='darkblue', foreground='white', borderwidth=2)
    cal2.grid(column=1, row=2)
    cal2.set_date(current_date)
    d_btn1 = Button(period_screen, text="Set period", command= lambda: [set_period(cal1, cal2, command), period_screen.destroy()])
    d_btn1.grid(column=0, row=3)
    
def set_period(cal1, cal2, command): #command definieert wat je ermee wilt doen. 'revenue', 'profit' en nu gebruikt. Acties nog aan koppelen
    date1 = cal1.get_date()
    date2 = cal2.get_date()
    if command == 'revenue':
        total_revenue = revenue_period(date1, date2)
        messagebox.showinfo("Revenue", f"Total revenue for\n{date1} till {date2}: {total_revenue}")
    if command == 'profit':
        total_profit = profit(date1, date2)
        messagebox.showinfo("Profit", f"Total profit for\n{date1} till {date2}: {total_profit}")        

"""
End of the list of functions needed to run the user interface.
Below, under "if __name__ == '__main__': " are all possible conditions obtained from the command line with
their respective action using the functions described above.
The first line calls the startup() function, which checks for the presence of
the required date file and bought- and sold-items lists. 
"""

if __name__ == '__main__':
    startup()
    if args.open_interface:
        open_interface()
    if args.command == 'buy':
        buy_item(args.product_name, args.price, args.expiration_date, args.buy_date)
        print('OK')
    if args.command == 'sell':
        sell_item(args.product_name, args.price)
        print('OK')
    if args.command == 'inventory':
        if args.now == True:
            date, date_upper_limit = determine_period('now')
        elif args.yesterday == True:
            date, date_upper_limit = determine_period('yesterday')
        elif args.date:
            date, date_upper_limit = determine_period(args.date)
        check_inventory(date)
    if args.command == 'revenue':
        if args.today == True:          
            date, date_upper_limit = determine_period('today')
            print(f'Today\'s revenue so far: {revenue_period(date, date_upper_limit)}')
        elif args.yesterday == True:
            date, date_upper_limit = determine_period('yesterday')
            print(f'Yesterday\'s revenue: {revenue_period(date, date_upper_limit)}')
        elif args.date:
            date, date_upper_limit = determine_period(args.date)
            if args.date.count('-') == 2:
                date_month = date.strftime("%B")
                print(f'Revenue from {date.day} {date_month} {date.year}: {revenue_period(date, date_upper_limit)}')
            elif args.date.count('-') == 1:
                date_month = date.strftime("%B")
                print(f'Revenue from {date_month} {date.year}: {revenue_period(date, date_upper_limit)}')
            elif args.date.count('-') == 0 and len(args.date) == 4:
                print(f'Revenue from {date.year}: {revenue_period(date, date_upper_limit)}')
        elif args.period:
            date, date_upper_limit = determine_period(args.period)
            print(f'Revenue from {args.period}: {revenue_period(date, date_upper_limit)}')
    if args.command == 'profit':
        if args.today == True:          
            date, date_upper_limit = determine_period('today')
            print(f'Today\'s profit so far: {profit(date, date_upper_limit)}')
        elif args.yesterday == True:
            date, date_upper_limit = determine_period('yesterday')
            print(f'Yesterday\'s profit: {profit(date, date_upper_limit)}')
        elif args.date:
            date, date_upper_limit = determine_period(args.date)
            if args.date.count('-') == 2:
                date_month = date.strftime("%B")
                print(f'Profit from {date.day} {date_month} {date.year}: {profit(date, date_upper_limit)}')
            elif args.date.count('-') == 1:
                date_month = date.strftime("%B")
                print(f'Profit from {date_month} {date.year}: {profit(date, date_upper_limit)}')
            elif args.date.count('-') == 0 and len(args.date) == 4:
                print(f'Profit from {date.year}: {profit(date, date_upper_limit)}')
        elif args.period:
            date, date_upper_limit = determine_period(args.period)
            print(f'Profit from {args.period}: {profit(date, date_upper_limit)}')
    if args.advance_time:
        advance_time(args.advance_time)
        date = get_date()
        print(f'Date adjusted with {args.advance_time} days. Current system date now {date}')

