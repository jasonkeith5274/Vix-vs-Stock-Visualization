from logging import PlaceHolder, root
from os import close
from more_itertools.more import collapse
import quandl
from requests.api import get
quandl.ApiConfig.api_key = 'e6A7Umw7QR9EvkzcMaNA'
import pandas as pd
from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import yfinance as yf
from tkinter import ttk
import numpy as np

  
# plot function is created for 
# plotting the graph in 
# tkinter window



def bestfit(open_v, percents):
    
    fig = Figure(figsize = (6, 4),
                 dpi = 100,)
    plot2 = fig.add_subplot(111)
    plot2.set_xlabel("Volatility Rating")
    plot2.set_ylabel("Percent Difference Between Open and Close")
    
    print(open_v)
    
    x = np.array(open_v)
    y = np.array(percents)

    m, b = np.polyfit(x,y,1)
    plot2.plot(x,y, 'o')
    plot2.plot(x, m*x + b)
    
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().place(x=760, y=40)
    
    
    
    
    
    
    
    
    


def plot(ticker):
  
    open_data = plot_vix()
    print(ticker)
    # the figure that will contain the plot
    fig = Figure(figsize = (7, 4),
                 dpi = 100,)
    
    #data = quandl.get_table("WIKI/PRICES", ticker = ["FB"], 
    #                    qopts = { 'columns': ['ticker', 'date', 'adj_open','adj_close'] }, 
    #                    date = { 'gte': '2018-12-31', 'lte': '2020-12-31'}, 
    #                    paginate=True)
    
    # let stock be the ticker we passed as a parameter
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")
    hist.to_csv("output.csv")
    
  
    # adding the subplot
    plot1 = fig.add_subplot(111)
    
    # add title, x axis title, y axis title
    plot1.set_title(str(ticker))
    plot1.set_xlabel("Last 5 Trading Days")
    plot1.set_ylabel("Percent Difference Between Open and Close")
    
    # set the grid for the graph
    plot1.grid(color = 'green', linestyle='--', linewidth=.5)
    
    # parse the .csv file, create an array that can then be plotted, we will let
    # the x axis be dates, and y-axis be the percent change
    df = pd.read_csv("output.csv")
    open_df = df['Open']
    close_df = df['Close']
    dates_df = df['Date']

    if dates_df.size == 0:
        dates_df = [0,1,2,3,4] 
    
    # now we can cacluate the percent change for each day of this stock and graph this as the y's
    percents = [1,2,3,4,5]
    i = 0
    for n in open_df:
        change = ((n - close_df.get(i)) / n) * 100
        percents[i] = change
        i += 1
    #print(percents)
    bestfit(open_data, percents)
    # plotting the graph
    x = np.array(dates_df)
    y = np.array(percents)
    #print(x)
    #print(y)
    
    plot1.plot(x, y)
    
    # now we can sort the data array and allow it to be our x'
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    #toolbar = NavigationToolbar2Tk(canvas,
    #                               window)
    #toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().place(x=10, y=1)
  
# the main Tkinter window
window = Tk()
  
# setting the title 
window.title('Plotting in Tkinter')

#set background color
window.configure(bg="WHITE")

# dimensions of the main window
window.geometry("1400x800")

# add an entry box and edit its attributes
entry1 = Entry(window, bd=2, 
               bg="LIGHT GREY")
entry1.insert(0, "Enter Stock Ticker")
entry1.place(x=950, y=13, width=125, height=25)

  
# function to retrieve input from the textbox
def getInput():
    ticker = entry1.get()
    print(ticker)
    # call the plot function
    # here we can also get a lot of other api data that could be useful
    # we can then send that data to be put into another widget to be displayed on the right side of the screen 
    plot(ticker)
    return


# this function will plot the vix graph and place it in the bottom right of the screen
def plot_vix():
    fig = Figure(figsize = (7, 4),
                 dpi = 100,)
    
    # get vix data from yahoo
    
    
    plot1 = fig.add_subplot(111)
    plot1.set_title("VIX")
    plot1.set_xlabel("Last 5 Trading Days")
    plot1.set_ylabel("Volatility Rating")
    plot1.grid(color = 'green', linestyle='--', linewidth=.5)
    
    df = pd.read_csv("vix.csv")
    open_df = df['OPEN']
    dates_df = df['DATE']
    plot1.plot(dates_df, open_df)
    
    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    canvas.get_tk_widget().place(x=10, y=390)
    return open_df

    
open_vix = plot_vix()


# here we want to create a table to evaluate the major markets: NASDAQ, S&P, 
def create_table():
    '''
    sp = yf.Ticker("^GSPC")
    hist = sp.history(period="5d")
    hist.to_csv("sp500.csv")
    rows = []
    
    # the table will consist of a label that says what the market is
    # the left column will be a date, the right column will be the closing value with percent change
    # next to it
    
    columns = ('#1', '#2', '#3')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.column('#1', anchor=CENTER)
    tree.column('#2', anchor=CENTER)
    tree.column('#3', anchor=CENTER)
    tree.heading('#1', text='Date')
    tree.heading('#2', text='Closing Value')
    tree.heading('#3', text='Percent change')
    
    
    df = pd.read_csv("sp500.csv")
    dates = df['Date']
    close_df = df['Close']
    open_df = df['Open']
    
    change = []
    for n in range(5):
        temp = ((open_df.get(n) - close_df.get(n)) / close_df.get(n)) * 100
        change.append(temp)
        
    for n in range(5):
        tree.insert(parent = '',index=n, iid=n, text='', values=(dates.get(n), close_df.get(n), change[n]))
        
    tree.grid(row=0, column=0, sticky='nsew')
    tree.place(x=750, y=100)
    
    
    '''
    sp = yf.Ticker("^IXIC")
    hist = sp.history(period="5d")
    hist.to_csv("nasdaq.csv")
    rows = []
    
    # the table will consist of a label that says what the market is
    # the left column will be a date, the right column will be the closing value with percent change
    # next to it
    
    columns = ('#1', '#2', '#3')
    tree = ttk.Treeview(window, columns=columns, show='headings')
    tree.column('#1', anchor=CENTER)
    tree.column('#2', anchor=CENTER)
    tree.column('#3', anchor=CENTER)
    tree.heading('#1', text='Date')
    tree.heading('#2', text='Closing Value')
    tree.heading('#3', text='Percent Change')
    
    
    df = pd.read_csv("nasdaq.csv")
    dates = df['Date']
    close_df = df['Close']
    open_df = df['Open']
    
    change = []
    for n in range(5):
        temp = ((open_df.get(n) - close_df.get(n)) / close_df.get(n)) * 100
        change.append(temp)
        
    for n in range(5):
        tree.insert(parent = '',index=n, iid=n, text='', values=(dates.get(n), close_df.get(n), change[n]))
        
    tree.grid(row=0, column=0, sticky='nsew')
    tree.place(x=750, y=530)
    
    
    
    

    
    
    
    
    
'''
# add labels for the major markets
l1 = Label(window, text="S&P 500")
l1.config(width=20)
l1.config(font=("Calibri", 10))
l1.place(x=980, y=80)
'''

l2 = Label(window, text="NASDAQ Composite")
l2.config(width=20)
l2.config(font=("Calibri", 10))
l2.place(x=980, y=510)

    

create_table()

# button that displays the plot
# inside of here we will get the text from the entry box first
plot_button = Button(master = window, 
                     command = getInput,
                     height = 1, 
                     width = 8,
                     text = "Plot")
  
# place the button in main window
# we need a difference of 125 x-units and 1 y-unit in order to place the entry box and button next to eachtoher correctly
plot_button.place(x=1075, y=12)

# run the gui
window.mainloop()


################################################################################
# notes
'''
We can use the yahoo finance api to get the VIX volitiaty index
This would allow us to graph the VIX over the last 5 trading days
By doing this we would have real time analysis ability because we will
also use the quandl api in order to get ticker information over the last 5 days

At this point it has come down to deciding on what to display for the index 
Currently I believe it would be good to compare the last 5 trading days open and close values and graph the percent difference between them
We then can see a direct comaprision between the vix data and how that stock could be impacted by the overall fear index 
'''