import tkinter
from tkinter import *
from tkinter import ttk
import csv

# main window
root = tkinter.Tk()
root.title("User Interface")
# main frame
mainframe = ttk.Frame(root) # attach frame to window
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S)) # idk what this does
root.columnconfigure(0, weight = 1) # in case frame is adjusted
root.rowconfigure(0, weight = 1) # in case fram is adjusted
# menu bar
menuBar = Menu(root)

scrollbar = Scrollbar(mainframe) # attach scrollbar to main frame
scrollbar.pack( side = RIGHT, fill = Y )

# commands/functions

def ViewClintonData ():
   filewin = Toplevel(root)
   button = Button(filewin, text = "Clinton Data")
   button.grid()

def ViewCongressData ():
   filewin = Toplevel(root)
   button = Button(filewin, text = "Congress Data")
   button.grid()

def ViewTrumpData ():
   filewin = Toplevel(root)
   button = Button(filewin, text = "Trump Data")
   button.grid() 

# widgets



# open clinton file
with open("clinton_raw.csv", encoding='utf8', newline = "") as file:
   reader = csv.reader(file)

   # r and c tell us where to grid the labels
   r = 0
   for col in reader:
      c = 0
      for row in col:
         # i've added some styling
         label = tkinter.Label(root, width = 15, height = 2, \
                               text = row, relief = tkinter.RIDGE)
         label.grid(row = r, column = c)
         c += 1
      r += 1
      if r == 10:
         break


root.mainloop()

