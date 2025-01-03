from hexbytes import HexBytes
from web3 import Web3


# Establish a connection with the blockchain
def establish_connection():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))


# Build the transaction by passing in the to, from, value, and data
def build_transaction(provider, to_user, from_user, value, data):
    transaction = {
        'to' : to_user,
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


def main():
    try:
# Start by establishing the connection to the ganache block chain and getting the provider
        ganache_provider = establish_connection()
        print(ganache_provider.is_connected())

# Build the transaction
        transaction = build_transaction(ganache_provider,
        "0x0919E4260849142D8A8cB8f3126CeaF8F01Ee6Ad",
        "0xC53EdeE1a3c29A547c6D794AFf0CC72A4202576c",
        "50", "Steve:Jenny:Power")


# Write the transaction to the blockchain, return the transaction hash. hint: see web3.py documentation
        tx_hash = write_to_chain(ganache_provider, transaction)
# Get the result of the transaction.
        result = get_transaction(ganache_provider, tx_hash)
# Get the data string originally coded in the build transaction function.
        data_string = get_block_data(result['input'])
# Print the Decrypted Data to the console, remember to take a screenshotfor the submission.
        print(f'Decoded Data: {data_string}')

    except Exception as e:
        print(e)

main()
