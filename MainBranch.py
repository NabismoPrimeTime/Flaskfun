import tkinter as tk
import csv

#window = tk.Tk()
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta


app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():
    if request.method == "POST":
        user = request.form["ent"]
        print(user)
        return render_template('base.html')
    return render_template('index.html')



"""@app.route("/entry", methods=["POST", "GET"])
def entry():
    if request.method == "POST":
        user = request.form["ent"]
        print(user)
        return render_template('base.html')
"""

# Class where all entry data is stored
class UserEntry:
    def __init__(self, date, price, entry_num, current_price, USD_amt):
        self.date = date
        self.price = price
        self.entry_num = entry_num
        self.current_price = current_price
        self.invest_amt = USD_amt

    def __str__(self):
        return ('{} : {} : {} : {}'.format(self.entry_num,self.date, self.price, self.invest_amt))

    def calculations(self):
        amt_of_BTC = float('{:.8f}'.format(float(self.invest_amt) / self.price))
        current_value_of_investment = float('{:.2f}'.format(amt_of_BTC * self.current_price))
        self.btc_amt = amt_of_BTC
        self.current_value = current_value_of_investment
        return amt_of_BTC, current_value_of_investment

    def calc_roi(self):
        self.netprofit = self.current_value - self.invest_amt
        self.roi = float('{:.2f}'.format((self.netprofit / self.invest_amt) * 100))
        return self.roi, self.netprofit


#Master lists
entry_list = []
sum_of_investment = 0
current_value_investment = 0
csv_title_rows = ["Entry Number", "Date Purchased", "Price Purchased", "Investment Amount", "Amount of Bitcoin",
                  "Current Value", "Net Profit", "ROI"]
real_close_price = []
close_floats = []

#DCA function
def dca():
    global sum_of_investment, current_value_investment
    if len(entry_list) > 0 :
        for entry in entry_list:
            global sum_of_investment, current_value_investment
            sum_of_investment += entry.invest_amt
            current_value_investment += entry.current_value
            dca_label = tk.Label( text = 'The sum of your investments is ${}\n Which would now be worth ${:.2f}'.format(sum_of_investment, current_value_investment),
            fg="white",
            bg="black",
            width=50,
            height=5 )
            dca_label.grid(row = 5, column = 1)

#Button to calculate DCA
dca_button = tk.Button(text = "Calculate DCA Amount", command = dca)



# Counter to calculate entry numbers
class Counter:
    def __init__(self):
        self.count = 0
test_counter = Counter()

# Functions

#Button to format date and collect data from entry boxes as well as create instances of USERENtry class
def date_button():
    global format_date
    user_date = entrystuff.get()
    months = [ 'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec' ]
    month_digits = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]
    month_seg = user_date[0:2]

    date_seg = user_date[3:5]
    year_seg = user_date[6:10]


    place_holder = month_digits.index(month_seg)
    month_code = months[place_holder]
    format_date = '{} {}, {}'.format(month_code, date_seg, year_seg)
    test_counter.count +=1
    entry_num = 'Entry number {}'.format(test_counter.count)
    current = get_current_price()
    investment = entry_usd.get()
    if format_date in dates:
        date_index = dates.index(format_date)
        matching_price = close_floats[date_index]
        entry_list.append(UserEntry(format_date, matching_price, entry_num, current, investment))

    entry_list[(test_counter.count -1)].calculations()
    entry_list[(test_counter.count - 1)].calc_roi()

    results_label = tk.Label(
        text = '{}% Return on Investment\n ${:.2f}'.format(entry_list[(test_counter.count - 1)].calc_roi()[0], entry_list[(test_counter.count - 1)].calc_roi()[1]),
        fg = "white",
        bg = "black",
        width=50,
        height=3

    )
    results_label.grid(row = 6, column = 0)
    results_summary = tk.Label(
        text = 'If you invested ${:.2f} on {},\n that would buy you {} Bitcoin'.format(entry_list[(test_counter.count -1)].invest_amt,
        entry_list[(test_counter.count -1)].date ,entry_list[(test_counter.count -1)].calculations()[0]),
        fg="white",
        bg="black",
        width=50,
        height=5
    )

    results_summary.grid(row= 5, column = 0)


# Wigets
greeting = tk.Label(text = "Welcome to Bitcoin ROI/DCA calculator")

date_label = tk.Label(
    text = "Please enter a past date you would like to buy Bitcoin on\n"
           "From May 2013 on,\n" "MM/DD/YY",
    fg = "white",
    bg = "black",
    width =80,
    height=3
)
entrystuff = tk.StringVar()

entry_for_date = tk.Entry(
    textvariable = entrystuff,
    bg = "white",
    fg = "black",
    width = 30)

# Button to capture data from entry boxes and calculate ROI
button_for_date = tk.Button(text = "Calculate ROI", command = date_button)


usd_amt_label = tk.Label(
    text = "Please enter a dollar amount you would like to invest",
    fg = "white",
    bg = "black",
    width = 50,
    height = 3,
)
entry_usd = tk.IntVar()
#Entry box for investment amount
entry_for_USD = tk.Entry(
    textvariable = entry_usd,
    bg = "white",
    fg = "black",
    width = 30)

#Function to export entries as csv
def exportcsv():
    with open('entries.csv', 'w') as csvfile:
        export_writer = csv.writer(csvfile)

        export_writer.writerow(csv_title_rows)
        for entry in entry_list:
            cated = [entry.entry_num,entry.date,entry.price,entry.invest_amt,entry.btc_amt, entry.current_value,entry.netprofit, entry.roi]


            export_writer.writerow(cated)

csv_button = tk.Button( text = "Export", command = exportcsv)



# Layout for wigets
greeting.grid(row = 0, column = 0)
date_label.grid(row = 1, column = 0)
entry_for_date.grid(row = 2, column =0)
button_for_date.grid(row = 3, column = 1)
usd_amt_label.grid(row = 3, column = 0)
entry_for_USD.grid(row = 4, column = 0)
dca_button.grid(row= 4, column = 1)
csv_button.grid(row= 4, column = 2)








import bs4
import requests
from bs4 import BeautifulSoup


#Lists to help seperate data from tables

rows_in_table = []
cells_in_table = []
dates = []
sliced_close_price = []
class RegexStuff():
    def  __init__(self):
        self.pattern = "[,]"
        self.pattern2 = "[a-zA-Z]"

regextool = RegexStuff()

# Function to import data from the table
def import_table():
    r = requests.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20200507')
    soup = bs4.BeautifulSoup(r.text, features="html.parser")
    table = soup.find('div', {'class': 'cmc-tab-historical-data ctxmt9-0 ASvFA'})
    rows = table.find_all('tr')

    global rows_in_table
    global cells_in_table

    for row in rows:
        if row != rows[0]:
            rows_in_table.append(row.text)
        #print(row.text)
            for cell in row:
                if cell.text != 'Date':
                    cells_in_table.append(cell.text)

#Extract prices and dates from lists
def extract_close_prices(list_to_review):
    global list_dates, list_close_price, dates, sliced_close_price
    list_dates = list_to_review[0:-1:7]

    dates.append(list_dates)
    list_close_price = list_to_review[4:-1:7]

    return list_dates, list_close_price
#appened master lists
def append_master_lists():
    global list_dates, list_close_price
    for date in list_dates:
        dates.append(date)
    """for price in list_close_price:
        split = price.split(',')
        joined = split[0] + split[1]
        price_float = float(joined)
        sliced_close_price.append(price_float)"""

#Function to get current price data
def get_current_price():
    r = requests.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/')
    soup = bs4.BeautifulSoup(r.text, features="html.parser")
    # price = soup.find('div', {'class': 'cmc-details-panel-price__price'})
    price = soup.find('div', {'class': 'cmc-details-panel-price jta9t4-0 fcilTk'}).find('span').text
    almost_finished_price = ''
    for char in price:
        if char.isdigit() == True:
            almost_finished_price += char
    finished_price = float(almost_finished_price) // 100
    return finished_price

def get_close_price(list_to_review):
    date = list_to_review.pop(0)
    date2 = list_to_review.pop(0)
    date3 = list_to_review.pop(0)
    date4= list_to_review.pop(0)
    close = list_to_review[0:-1:7]

    """print(close)
    print(cells_in_table)"""
    real_close_price.append(close)
    #print(real_close_price)
i = 0
def close_price_to_float(list_to_review):
    global i
    for cell in list_to_review:
        for cell2 in cell:
            if len(cell2) > 6:
                split = cell2.split(',')
                joined = split[0] + split[1]
                price_float = float(joined)
                close_floats.append(price_float)

            else:
                small_float = float(cell2)
                close_floats.append(small_float)


import_table()

extract_close_prices(cells_in_table)

append_master_lists()
get_close_price(cells_in_table)
close_price_to_float(real_close_price)
#window.mainloop()




if __name__ == "__main__":
    app.run(debug=True)