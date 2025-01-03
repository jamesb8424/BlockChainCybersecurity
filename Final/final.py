# Import the base file
from CS705_GUI_BaseFile import *
# Import tkinter
from tkinter import *
# Import hexbytes
from hexbytes import HexBytes
# Import web3
from web3 import Web3
import os
from datetime import datetime

FILENAME = "ItemTransactionHashes.bin"
FILENAME_CELEB = "CelebTransactionHashes.bin"



# Establish a connection with the blockchain
def establish_connection():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))


#  Build the transaction by passing in the to, from, value, and data
def build_transaction(provider, to_user, from_user, value, data):
    transaction = {
        'to' :  to_user,
        'from' : from_user,
        'value' : provider.to_wei(value, 'ether'),
        'gas' : 43255,
        'nonce' : provider.eth.get_transaction_count(from_user),
        'data' : str.encode(data)
    }

    return transaction

# Write to the chain established in the connection
def write_to_chain(provider, transaction):
    return provider.eth.send_transaction(transaction)

# Get transaction object from the passed in hash
def get_transaction(provider, hash):
    return provider.eth.get_transaction(hash)


# Get the data from the block (This is a complete function, do not modify)
def get_block_data(data):
    # Get the string as a HexBytes array
    hex_value = HexBytes(data)
    # Convert to hex value
    hex_obj = hex_value.hex()
    # If the string contains 0x, we need to strip it off
    if(hex_obj.__contains__('0x')):
        hex_obj = hex_obj.strip('0x')
    # Get the bytes from the hex value
    bytes_obj = bytes.fromhex(hex_obj)
    # Convert it to a human readable string
    result_string = bytes_obj.decode('utf-8')
    # Return the result string
    return result_string           


def updateToAdminAddItemPage(window, AddressVar):
    userAddress = AddressVar.get()
    
    for widget in window.winfo_children():
        widget.destroy()

    if userAddress.startswith("0x"):
        print("good!")
    else: 
        print("bad user address [no 0x]")
        errorLabel = Label(text="Invalid Eth address! Your Eth Address must start with 0x")
        errorLabel.config(font=("Courier", 20))
        errorLabel.pack()
        tryAgainButton = Button(text="Try Login Again? (Admin)", command=lambda window=window : updateToLoginPageAdmin(window))
        tryAgainButton.pack() 
        return
    
    if len(userAddress) != 42:
        print("bad eth address length")
        errorLabel = Label(text="Invalid Eth address! Your Eth Address must be atleast 42 characters long!")
        errorLabel.config(font=("Courier", 20))
        errorLabel.pack()
        tryAgainButton = Button(text="Try Login Again? (Admin)", command=lambda window=window : updateToLoginPageAdmin(window))
        tryAgainButton.pack() 
        return

    # Creating item labels and entry box
    itemLabel = Label(text="Item")
    itemLabel.config(font=("Courier", 20))
    itemLabel.pack()

    itemVar = StringVar()
    itemEntry= Entry(textvariable=itemVar)
    itemEntry.pack()

# Creating a Value label and Entry box
    valueLabel = Label(text="Value (ETH)")
    valueLabel.config(font=("Courier", 20))
    valueLabel.pack()

    valueVar = StringVar()
    valueEntry= Entry(textvariable=valueVar)
    valueEntry.pack()

    SubmitButton = Button(text="Submit", command=lambda window=window, itemVar=itemVar, valueVar=valueVar : handleItemCreation(window, itemVar, valueVar, AddressVar))
    SubmitButton.pack()

    build_listbox(establish_connection())

def handleItemCreation(window, itemVar, valueVar, AddressVar):
    provider = establish_connection()

    value = valueVar.get()
    try:
        value = float(value)
    except:
        for widget in window.winfo_children():
            widget.destroy()

        errorLabel = Label(text="Invalid value! The value must be a number or decimal value.")
        errorLabel.config(font=("Courier", 20))
        errorLabel.pack()
        tryAgainButton = Button(text="Try Add Item Again?", 
                                command=lambda window=window : updateToAdminAddItemPage(window, AddressVar))
        tryAgainButton.pack()
        build_listbox(establish_connection()) 
        return


    storeAddressOne = "0xCF4d17eA040C3784e3c54A4F7fd3C4f8Be31f2E2"
    storeAddressTwo = "0x49778E1276eA0e67f52228B4cEd575F056F5c93B"
    tiny = 1e-12
    data = "item:" + itemVar.get() + "; value:" + valueVar.get()


    tx = build_transaction(provider, storeAddressOne, storeAddressTwo, tiny, data)
    hash = write_to_chain(provider, tx)

    
    if not os.path.exists(FILENAME):
        with open (FILENAME, "wb") as fid:
            fid.write(hash)
    else:
        with open(FILENAME, "rb") as fid:
            content = fid.read()

        content += b"SPLITME" + hash
        with open(FILENAME, "wb") as fid:
            fid.write(content)

    for widget in window.winfo_children():
        widget.destroy()

    successLabel = Label(text="Item Created Successfully!")
    successLabel.config(font=("Courier", 20))
    successLabel.pack()

    SubmitButton = Button(text="Add a New Item", command=lambda window=window: updateToAdminAddItemPage(window, AddressVar))
    SubmitButton.pack()

    build_listbox(establish_connection())

    
def updateToCelebSignaturePage(window):
    for widget in window.winfo_children():
        widget.destroy()

         
    provider = establish_connection()

    signatures = []

    if os.path.exists(FILENAME_CELEB):
        with open(FILENAME_CELEB, "rb") as fid:
            hashes = fid.read()

        hashes = hashes.split(b"SPLITME")
        for tx_hash in hashes:
            result = get_transaction(provider, tx_hash)
            print("got transaction")

        # Get the data String originally coded in he build transaction function. 
            data_string = get_block_data(result['input'])
            signatures.append(data_string)
        

    if not os.path.exists(FILENAME):
        noItemLabel = Label(text="No Items were found. Ask admin to add item")
        noItemLabel.config(font=("Courier", 20))
        noItemLabel.pack()

        RefreshButton = Button(text="Refresh page", command=lambda window=window: updateToCelebSignaturePage(window))
        RefreshButton.pack()

    else:
        with open(FILENAME, "rb") as fid:
            hashes = fid.read()
            hashes = hashes.split(b"SPLITME")
        
        
        item_number = 0
        data_strings = []
        for tx_hash in hashes:
            item_number += 1
            result = get_transaction(provider, tx_hash)
            print("got transaction")

        
            data_string = get_block_data(result['input'])
            data_strings.append(data_string)
        
            print("got block data")
            print(f'Decrypted Data: {data_string}')


            data_string = data_string.split(";")[0]

            ItemAndValueLabel = Label(text=data_string)
            ItemAndValueLabel.config(font=("Courier", 20))
            ItemAndValueLabel.pack()

            isAuthenticated = False
            for signature in signatures:
                item_num_sig = signature.replace("was authenticated by LeBron James","")
                item_num_sig = item_num_sig.replace("item_number:", "")

                if str(item_number) == item_num_sig:
                    AuthenticatedLabel = Label(text="Item Autenticated by LeBron James")
                    AuthenticatedLabel.config(font=("Courier", 20))
                    AuthenticatedLabel.pack()
                    isAuthenticated = True


            if isAuthenticated == False:
                CelebAuthenticateButton = Button(text="Authenticate Item?", command=lambda window=window,item_number=item_number: handleCelebSignature(window, item_number))
                CelebAuthenticateButton.pack()

    build_listbox(establish_connection())


def handleCelebSignature(window, item_number):
    provider = establish_connection()
    print("item_number: ", item_number)

    storeAddressOne = "0xCF4d17eA040C3784e3c54A4F7fd3C4f8Be31f2E2"
    storeAddressTwo = "0x49778E1276eA0e67f52228B4cEd575F056F5c93B"
    tiny = 1e-12
    
    data = "item_number:" + str(item_number) + "was authenticated by LeBron James"
    tx = build_transaction(provider, storeAddressOne, storeAddressTwo, tiny, data)

    hash = write_to_chain(provider, tx)

    if not os.path.exists(FILENAME_CELEB):
        with open (FILENAME_CELEB, "wb") as fid:
            fid.write(hash)
    else:
        with open(FILENAME_CELEB, "rb") as fid:
            content = fid.read()

        content += b"SPLITME" + hash
        with open(FILENAME_CELEB, "wb") as fid:
            fid.write(content)

    for widget in window.winfo_children():
        widget.destroy()

    successLabel = Label(text="Item Authenticated Successfully!")
    successLabel.config(font=("Courier", 20))
    successLabel.pack()

    SubmitButton = Button(text="To Authenticate More Items, Click Here.", command=lambda window=window: updateToCelebSignaturePage(window))
    SubmitButton.pack()

    build_listbox(establish_connection())


# Function to let the customer choose an item.
def updateToCustomerChooseItem(window):
    for widget in window.winfo_children():
        widget.destroy()


    ## handle username (Eth Address) input Validation here. ##

    provider = establish_connection()

    signatures = []
    if os.path.exists(FILENAME_CELEB):
        with open(FILENAME_CELEB, "rb") as fid:
            hashes = fid.read()
        
        hashes = hashes.split(b"SPLITME")
        for tx_hash in hashes:
            result = get_transaction(provider, tx_hash)
            print("got transaction")

            data_string = get_block_data(result['input'])
            signatures.append(data_string)
    
    if not os.path.exists(FILENAME):
        noItemLabel = Label(text="No Items were found. Ask admin to add item")
        noItemLabel.config(font=("Courier", 20))
        noItemLabel.pack()

        RefreshButton = Button(text="Refresh page", command=lambda window=window: updateToCustomerChooseItem(window))
        RefreshButton.pack()
        return

    else:
        with open(FILENAME, "rb") as fid:
            hashes = fid.read()
            hashes = hashes.split(b"SPLITME")

        item_number = 0
        data_string = []
        for tx_hash in hashes:
            item_number += 1
            result = get_transaction(provider, tx_hash)
            print("got transaction")

            data_string = get_block_data(result['input'])
            

            print("got block data")
            print(f'Decrypted Data: {data_string}')

            ItemAndValueLabel = Label(text=data_string)
            ItemAndValueLabel.config(font=("Courier", 20))
            ItemAndValueLabel.pack()

            
            for signature in signatures:
                item_num_sig = signature.replace("was authenticated by LeBron James","")
                item_num_sig = item_num_sig.replace("item_number:","")

                if str(item_number) == item_num_sig:
                    AuthenticatedLabel = Label(text="Item Authenticated by LeBron James")
                    AuthenticatedLabel.config(font=("Courier", 20))
                    AuthenticatedLabel.pack()
                    
            
            BuyButton = Button(text="Buy Item", command=lambda window=window,item_number=item_number : updateToCustomerAddressEntry(window, item_number))
            BuyButton.pack()

    build_listbox(establish_connection())

def updateToCustomerAddressEntry(window, item_number):
    for widget in window.winfo_children():
        widget.destroy()

    
    adminAddItemTitle = Label(text="New Kicks (Inc.)")
    adminAddItemTitle.pack()

    # Creating a title for the GUI
    title = Label(text="NEW KICKS ORDER FORM")
    title.config(font=("Courier", 40))
    title.pack()

        # Creating a Item label and Entry box
    itemLabel = Label(text="Item")
    itemLabel.config(font=("Courier", 20))
    #itemLabel.pack()

    itemVar = StringVar()
    itemEntry= Entry(textvariable=itemVar)
    #itemEntry.pack()

# Creating a Value label and Entry box
    valueLabel = Label(text="Value (ETH)")
    valueLabel.config(font=("Courier", 20))
    #valueLabel.pack()

    valueVar = StringVar()
    valueEntry= Entry(textvariable=valueVar)
    #valueEntry.pack()

# Creating a From label and Entry box
    fromLabel = Label(text="Seller: (New Kicks,Inc.)")
    fromLabel.config(font=("Courier", 25))
    fromLabel.pack()

    fromVar = StringVar()
    fromEntry= Entry(textvariable=fromVar)
    #fromEntry.pack()

    
# Creating a To label and Entry box
    toLabel = Label(text="Customer Name")
    toLabel.config(font=("Courier", 30))
    toLabel.pack()  

    toVar = StringVar()
    toEntry= Entry(textvariable=toVar)
    toEntry.pack()

# Creating an Address label and Entry box
    streetLabel = Label(text="Street")
    streetLabel.config(font=("Courier", 20))
    streetLabel.pack()

    streetVar = StringVar()
    streetEntry= Entry(textvariable=streetVar)
    streetEntry.pack()

# Creating a City Label and Entry
    cityLabel = Label(text="City")
    cityLabel.config(font=("Courier", 20))
    cityLabel.pack()

    cityVar = StringVar()
    cityEntry= Entry(textvariable=cityVar)
    cityEntry.pack()
    

# Creating a State Label and Entry box
    stateLabel = Label(text="State")
    stateLabel.config(font=("Courier", 20))
    stateLabel.pack()

    stateVar = StringVar()
    stateEntry= Entry(textvariable=stateVar)
    stateEntry.pack()

# Creating a Zipcode Label and Entry box
    zipLabel = Label(text="Zipcode")
    zipLabel.config(font=("Courier", 20))
    zipLabel.pack()

    zipVar = StringVar()
    zipEntry= Entry(textvariable=zipVar)
    zipEntry.pack()

    ethLabel = Label(text="Your Ethereum Address for payment Processing")
    ethLabel.config(font=("Courier", 20))
    ethLabel.pack()

    ethVar = StringVar()
    ethEntry= Entry(textvariable=ethVar)
    ethEntry.pack()

    BuyButton = Button(text="Submit Address and Buy Item", command=lambda window=window,item_number=item_number,
                                                            toVar=toVar,streetVar=streetVar,cityVar=cityVar,stateVar=stateVar, zipVar=zipVar, ethVar=ethVar : 
                                                            handleBuyItem(window, item_number, toVar, streetVar, cityVar, stateVar, zipVar, ethVar)) 
    BuyButton.pack()

    build_listbox(establish_connection())


def handleBuyItem(window, this_item_number, toVar, streetVar, cityVar, stateVar, zipVar, ethVar):
    for widget in window.winfo_children():
        widget.destroy()

    ## Handle user input validation ##

    provider = establish_connection()

    with open(FILENAME, "rb") as fid:
        hashes = fid.read()
        hashes = hashes.split(b"SPLITME")

    item_number = 0
    data_strings = []
    for tx_hash in hashes:
        item_number += 1

        if item_number == this_item_number:

            result = get_transaction(provider, tx_hash)
            print("got transaction") 

            data_string = get_block_data(result['input'])
            
            break
    value = data_string.split(";")[1]
    value = value.split(":")[1]
    print(value)
    value = value.replace(" ","")
    value = float(value)

    if value > 100:
        print("Item too expensive for user balance")
        errorLabel = Label(text="Item costs more ETH than you have available.")
        errorLabel.config(font=("Courier", 20))
        errorLabel.pack()
        tryAgainButton = Button(text="Buy Item", command=lambda window=window,item_number=item_number : updateToCustomerAddressEntry(window, item_number))
        tryAgainButton.pack()
        return

    else:
        storeAddressOne = "0xCF4d17eA040C3784e3c54A4F7fd3C4f8Be31f2E2"
        data = "item_number:" + str(item_number) + "was bought by" + toVar.get() + \
                "shipping to street address = " + streetVar.get() + \
                    "and city = " + cityVar.get() + \
                    "and state = " + stateVar.get() + \
                    "and zip = " + zipVar.get()

        
        tx = build_transaction(provider, storeAddressOne, ethVar.get(), value, data)

        hash = write_to_chain(provider, tx)

        """similar to admin add item page, save hashes to file"""

        successLabel = Label(text="Item Bought Successfully!")
        successLabel.config(font=("Courier", 20))
        successLabel.pack()

        SubmitButton = Button(text="To Buy More Items, Click Here.", command=lambda window=window : updateToCustomerChooseItem(window))
        SubmitButton.pack()


# Function to update login page for Admin
def updateToLoginPageAdmin(window):
    for widget in window.winfo_children():
        widget.destroy()

    loginPageTitle = Label(text="Please login (Admin)")
    loginPageTitle.pack()

    AddressLabel = Label(text="Username (ETH Address)")
    AddressLabel.pack()

    AddressVar = StringVar()
    AddressEntry = Entry(textvariable=AddressVar)
    AddressEntry.pack()

    PasswordLabel = Label(text="Password")
    PasswordLabel.pack()

    PasswordVar = StringVar()
    PasswordEntry = Entry(textvariable=PasswordVar)
    PasswordEntry.pack()

    SubmitLoginButton = Button(text="Submit", 
                        command=lambda window=window, AddressVar=AddressVar : updateToAdminAddItemPage(window,AddressVar))
    SubmitLoginButton.pack()

    build_listbox(establish_connection())



# Function to update Celebrity Login
def updateToLoginPageCeleb(window):
    for widget in window.winfo_children():
            widget.destroy()

    loginPageTitle = Label(text="Please login (Celebrity)")
    loginPageTitle.pack()

    AddressLabel = Label(text="Username (ETH Address)")
    AddressLabel.pack()

    AddressVar = StringVar()
    AddressEntry = Entry(textvariable=AddressVar)
    AddressEntry.pack()

    PasswordLabel = Label(text="Password")
    PasswordLabel.pack()

    PasswordVar = StringVar()
    PasswordEntry = Entry(textvariable=PasswordVar)
    PasswordEntry.pack()

    SubmitLoginButton = Button(text="Submit", command=lambda window=window : updateToCelebSignaturePage(window))
    SubmitLoginButton.pack()

    build_listbox(establish_connection())


# Function to upodate Customer Login
def updateToLoginPageCustomer(window):
    for widget in window.winfo_children():
            widget.destroy()

    loginPageTitle = Label(text="Please login (Customer)")
    loginPageTitle.pack()

    AddressLabel = Label(text="Username (ETH Address)")
    AddressLabel.pack()

    AddressVar = StringVar()
    AddressEntry = Entry(textvariable=AddressVar)
    AddressEntry.pack()

    PasswordLabel = Label(text="Password")
    PasswordLabel.pack()

    PasswordVar = StringVar()
    PasswordEntry = Entry(textvariable=PasswordVar)
    PasswordEntry.pack()

    SubmitLoginButton = Button(text="Submit", command=lambda window=window : updateToCustomerChooseItem(window))
    SubmitLoginButton.pack()

    build_listbox(establish_connection())

def build_listbox(ganache_provider):
    myListbox = Listbox(width=1000)
    myListbox.pack()
    block = ganache_provider.eth.get_block("latest")
    print(block)
    print(block["number"])

    for block_number in range(int(block["number"]) +1):
        block = ganache_provider.eth.get_block(block_number)
           
        block_info = str(block["number"]) + ","

        unix_timestamp = block["timestamp"]
        datetime_object = datetime.fromtimestamp(unix_timestamp)

        
        block_info += str(datetime_object) + ","
        block_info += str(block["hash"].hex()) + "," 
        
        if block_number == 0:
            block_info += "0,"
            block_info += "[Genesis Block]"
        else:
            block_info += str(block["nonce"].hex()) + "[,"
            for tx in block["transactions"]:
                print(tx)
                result = get_transaction(ganache_provider, tx)
                print(result)

                block_info += result["hash"].hex() + ":"
                block_info += str(datetime_object) + ":"
                block_info += result["from"] + ":"
                block_info += result["to"] + ":"
                block_info += str(result["value"]/1e18) + ":"
                block_info += get_block_data(result['input'])
                
                
            block_info += "]"
            print(block_info)

        myListbox.insert(END, block_info)


    
def main():
    try:
        # Start by establishing the connection to the ganache block chain and getting the provider
        ganache_provider = establish_connection()
        print(ganache_provider.is_connected())
        print("established connection")

        
        

    # Start your GUI by creating the window using a Tk object
        window = Tk()
    
    # Add a title to the UI window
        studentFirstName = 'James'
        studentLastName = "Bowling"
        window.title(f'Final Project Python GUI {studentFirstName}-{studentLastName}')
    
    # Set the UI window size
        window.geometry("1280x1024")

        # Creating a title for the GUI
        title = Label(text="NEW KICKS INC.")
        title.config(font=("Courier", 40))
        title.pack()

        firstPageTitle = Label(text="Choose User Type")
        firstPageTitle.pack()
        adminButton = Button(text="Admin", command=lambda window=window : updateToLoginPageAdmin(window))
        adminButton.pack()
        celebButton = Button(text="Celebrity", command=lambda window=window : updateToLoginPageCeleb(window))
        celebButton.pack()
        customerButton = Button(text="Customer", command=lambda window=window : updateToLoginPageCustomer(window))
        customerButton.pack()

        blockchainLabel = Label(text="Blockchain Transactions")
        blockchainLabel.pack()
        build_listbox(establish_connection())
        

        #block = ganache_provider.eth.get_block(0)
        #print(block)
        #block_data = get_block_data(block)
        #print(block_data)

        

# Make the window locked in size (this helps minimize objects changing)
        window.resizable(False, False)
    
    # This creates the window to display on the screen
        window.mainloop()

        
    except Exception as e:
        print(e)



main()