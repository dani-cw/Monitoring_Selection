from asyncio.windows_events import NULL
from operator import truediv
from os import device_encoding
from pickle import TRUE
from unittest import result
import pandas as pd

def validate_merchant(merchants, transaction):
    
    merchant_id = transaction[2]
    has_cbk = transaction[8]

    # Creates merchant profile    
    if merchant_id not in merchants:
        merchants[merchant_id] = {"isFraudster": 0}
        
    # If already not fraudster, skip    
    if merchants[merchant_id]["isFraudster"] > 0:
        return 1

    # Otherwise, if a transaction is valid, merchant is not fraudster. Increase int by 1.
    if has_cbk == False:
        merchants[merchant_id]["isFraudster"] += 1
    
    # Returning 1 makes the program generate merchant list at ending.
    return 1

def validate_users(users, transaction):
    
    user_id = transaction[3]
    has_cbk = transaction[8]

    # Creates users profile    
    if user_id not in users:
        users[user_id] = {"isFraudster": 0}
        
    # If already not fraudster, skip        
    if  users[user_id]["isFraudster"] > 0:
        return 2

    # Otherwise, if a transaction is valid, user is not fraudster. Increase int by 1.
    if has_cbk == False:
        users[user_id]["isFraudster"] += 1
    
    # Returning 2 makes the program generate users list at ending.    
    return 2

def main():

    # Read CSV
    
    dataset = pd.read_csv('./Data/transactional-sample.csv')
    dataset = dataset.sort_values(by="transaction_date")
    
    # Assigned variables
    result = 0
    merchants = {}
    users = {}
    
    # Saving transaction data
    # For loop treats 1 transaction at a time
    
    i = 0
    for transaction in dataset.itertuples():
        if i == 3200:
            break
        i += 1
        
        # Naming variables
        index = transaction[0]
        transaction_id = transaction[1]
        merchant_id = transaction[2]
        user_id = transaction[3]
        card_number = transaction[4]
        transaction_date = transaction[5]
        transaction_amount = transaction[6]
        device_id = transaction[7]
        has_cbk = transaction[8]
        
        # Debug for assigned 
         #print(index, transaction_id, merchant_id, user_id, card_number, transaction_date, transaction_amount, device_id, has_cbk)
        
        # Comment the one you don't want to run.
        
        result = validate_merchant(merchants, transaction) 
        #result = validate_users(users, transaction)
        
# Debug for merchant dictionary.   
#    print (merchants)

    # Print fraudsters, based on choice (1 for merchants, 2 for users).
    # Add ( ,) to the print if you wish to use the results on a SQL query.
    if(result == 1):
        for key in merchants.keys():
            if (merchants[key]["isFraudster"] == 0):
                print(key)
    elif(result == 2):            
        for key in users.keys():
            if (users[key]["isFraudster"] != 0):
                print(key)    

if __name__ == '__main__':
    main()