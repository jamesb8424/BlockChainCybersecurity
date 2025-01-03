# Import the base file
from CS705_GUI_BaseFile import *
# Import tkinter
from tkinter import *

# Generate a random guid for the transaction
# def Generate_Random_UUID():

# Create a datetime stamp based on the current datetime
# def Get_DateStamp():

# Generate a SHA1 hashed based on the transaction list
# def Generate_SHA1(hash_data):

# Generate a transaction from the command line values
# def Generate_Transactions(to_person, from_person, quantity, what_item):

# Add the transaction to the blockchain and return the block chain to update the original
# def Add_To_BlockChain(blockChain, to_person, from_person, quantity_object, what_object):

# Add the transaction to the blockchain and return the block chain to update the original
# def Create_Block(blockChain, transaction):

# Create the genesis block
#def Generate_Genesis(blockChain):

# Update the list box object
#def updateList(item, listbox):

# Handle the button Press.
# def buttonPress(blockChain, listbox,ToEntry:Entry, FromEntry:Entry,ValueEntry:Entry, ItemEntry:Entry):

# Clear the fields after creating the block
# def clearFields(To:Entry, From:Entry, Value:Entry, Item:Entry):

# Validate the input so the user does not create empty blocks
# def validateInput(To, From, Value, Item):

# Define the main function
def main():

# Initialize the blockchain list object

    blockChain = []

# Create the genesis block

    blockChain = Generate_Genesis(blockChain)



# Start your GUI by creating the window using a Tk object

window = Tk()

# Add a title to the UI window

studentFirstName = 'James'

studentLastName = "Bowling"

window.title(f'Module 11 Python GUI {studentFirstName}-{studentLastName}')

# Set the UI window size

window.geometry("1280x1024")

### Students will complete the GUI per the Assignment instructions, See Tkinter documentation ###

# Creating a title for the GUI

title =Label(text="Create a new transaction")
title.config(font=("Courier", 30))
title.pack()

# Creating a From label and Entry box

fromLabel =Label(text="From Person")
fromLabel.config(font=("Courier", 30))
fromLabel.pack()

fromVar = StringVar()
fromEntry= Entry(textvariable=fromVar)
fromEntry.pack()

# Creating a To label and Entry box

toLabel = Label(text="To Person")
toLabel.config(font=("Courier", 30))
toLabel.pack()

toVar = StringVar()
toEntry= Entry(textvariable=toVar)
toEntry.pack()

# Creating a Value label and Entry box

valueLabel = Label(text="Value (Dollars)")
valueLabel.config(font=("Courier", 30))
valueLabel.pack()

valueVar = StringVar()
valueEntry= Entry(textvariable=valueVar)
valueEntry.pack()

# Creating a Item label and Entry box

itemLabel = Label(text="Item")
itemLabel.config(font=("Courier", 30))
itemLabel.pack()

itemVar = StringVar()
itemEntry= Entry(textvariable=itemVar)
itemEntry.pack()

# Creating a Listbox and setting the size

myListbox = Listbox(width=200)

# Creating the addBlockButton and updating the block to the listbox

addBlockbutton= Button(text="addBlock",command=lambda blockChain=blockChain,myListbox=myListbox,
toEntry=toEntry, fromEntry=fromEntry,valueEntry=valueEntry, itemEntry=itemEntry : buttonPress(blockChain, myListbox,
toEntry, fromEntry, valueEntry, itemEntry))


addBlockbutton.pack()

myListbox.pack()

# Make the window locked in size (this helps minimize objects changing)

window.resizable(False, False)

# This creates the window to display on the screen

window.mainloop()

# Call the main function
main()
