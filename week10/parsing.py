# Import CSV library

import csv

# Define a read in BlockChain (.CSV) function

def ReadIn_CSV(csv_name, transaction_id):

    with open(csv_name, "r") as csvfile:

        spamreader = csv.reader(csvfile, delimiter=",")

for row in spamreader:

    block = " ".join(row[:4])

    transactions = row[4].split(",")

for transaction in transactions:

    if str(transaction_id) in transaction:

        block += "\n" + transaction

print(block)

exit()

# Declare Main

def main():


# Execute read in function

    ReadIn_CSV('student_blockchain.csv', "bab36d37b54c4acb8283319dac76db6a")

# Execute main function

main()
