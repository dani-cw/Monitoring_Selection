from asyncio.windows_events import NULL
from operator import truediv
from os import device_encoding
from pickle import TRUE
import pandas as pd
from datetime import datetime

def diff_date(date1, date2):
    
    # Transaction speedtest, uses datetime library.
    date1,_ = date1.split(".")
    date2,_ = date2.split(".")
    date1 = datetime.strptime(date1, '%Y-%m-%dT%H:%M:%S')
    date2 = datetime.strptime(date2, '%Y-%m-%dT%H:%M:%S')
    
    return (date1 - date2).total_seconds() / 60.0
    
def validate_merchant(merchants, transaction):

    index = transaction[0]
    transaction_id = transaction[1]
    merchant_id = transaction[2]
    user_id = transaction[3]
    card_number = transaction[4]
    transaction_date = transaction[5]
    transaction_amount = transaction[6]
    device_id = transaction[7]
    has_cbk = transaction[8]

    # Creates merchant profile    
    if merchant_id not in merchants:
        merchants[merchant_id] = { "isBlocked": False, "totalSales": 0, "totalAmount": 0.0, "score": 0 }
    
    # Set variables
    min_transaction_amt = 5
    amount_alert_threshold = 5
    
    if merchants[merchant_id]["isBlocked"]:
        return False
    
    # First the script checks if there is already a sales profile for the merchant, and create or improves it.
    # If the transaction value is much higher then the sum of last merchant's sales, it takes an action, from alerting to blocking them.
    if(merchants[merchant_id]["totalSales"] < min_transaction_amt):
        merchants[merchant_id]["totalSales"] += 1
        merchants[merchant_id]["totalAmount"] += transaction_amount
    else:
        if transaction_amount*amount_alert_threshold > (merchants[merchant_id]["totalAmount"]/merchants[merchant_id]["totalSales"]): # Alert
            merchants[merchant_id]["score"] += (transaction_amount/100)*(merchants[merchant_id]["totalAmount"]/merchants[merchant_id]["totalSales"])  # Adds score based on value
            
        if merchants[merchant_id]["score"] > 5: # Blocks merchant based on value
            merchants[merchant_id]["isBlocked"] = True
            return False
        
        merchants[merchant_id]["totalSales"] += 1
        merchants[merchant_id]["totalAmount"] += transaction_amount
        
    return True
            
def validate_user(users_transactions, transaction):
    
    index = transaction[0]
    transaction_id = transaction[1]
    merchant_id = transaction[2]
    user_id = transaction[3]
    card_number = transaction[4]
    transaction_date = transaction[5]
    transaction_amount = transaction[6]
    device_id = transaction[7]
    has_cbk = transaction[8]
    
    # Creates user profile    
    if user_id not in users_transactions:
        users_transactions[user_id] = { "isBlocked": False, "lastTransactionTime": '1000-01-01T01:01:01.000001', "last_device": {"device_id" : NULL, "used_amount" : 0 }, "user_device": NULL }
    
    # Set variables
    device_threshold = 3
    time_threshold = -180.0  #datetime.minute(180) #3 #hours
    night_max_amount = 700.00
    accepted_time_early = 6 #o' clock
    accepted_time_late = 22 #o' clock
    
    # Sets hour of transaction, for late night blocking
    transaction_hour,_ = transaction_date.split(".")
    transaction_hour = datetime.strptime(transaction_hour, '%Y-%m-%dT%H:%M:%S')
    transaction_hour = transaction_hour.hour
    
    # Checks and sets device. About 2x for y, being x false_positives and y positives.
    
    if device_id != NULL:
        if users_transactions[user_id]["last_device"]["device_id"] == NULL:
            if users_transactions[user_id]["last_device"]["device_id"] == device_id:
                users_transactions[user_id]["last_device"]["used_amount"] += 1
                if users_transactions[user_id]["last_device"]["used_amount"] == device_threshold:
                    users_transactions[user_id]["user_device"] = users_transactions[user_id]["last_device"]["device_id"]
            else:
                users_transactions[user_id]["last_device"]["device_id"] = device_id
        elif users_transactions[user_id]["user_device"] != device_id:
            users_transactions[user_id]["isBlocked"] = True
            return False
        
    # Checks time difference between transactions, blocking too many transactions in a row
    timeBetweenTransactions = diff_date(users_transactions[user_id]["lastTransactionTime"], transaction_date)
    users_transactions[user_id]["lastTransactionTime"] = transaction_date
    
    # Checks if transaction was made late night, and if it respected max value for those period
    if transaction_hour >= accepted_time_late or transaction_hour <= accepted_time_early:
        if transaction_amount > night_max_amount:
            users_transactions[user_id]["isBlocked"] = True
            return False
    
    
    if users_transactions[user_id]["isBlocked"]:
        return False
    
    return True

def main():

    # Read CSV
    
    dataset = pd.read_csv('./Data/transactional-sample.csv')
    dataset = dataset.sort_values(by="transaction_date")
    
    users_transactions = {}
    merchants = {}
    
    # Saving transaction data
    # For loop treats 1 transaction at a time
    
    i = 0
    negative = 0
    positive = 0
    fake_negative = 0
    fake_positive = 0
    for transaction in dataset.itertuples():
        
        isValid = True
        
        if i == 3200:
            break
        i += 1
        
        # Naming variables
        #index = transaction[0]
        transaction_id = transaction[1]
        #merchant_id = transaction[2]
        #user_id = transaction[3]
        #card_number = transaction[4]
        #transaction_date = transaction[5]
        #transaction_amount = transaction[6]
        #device_id = transaction[7]
        has_cbk = transaction[8]
        
        #print(index, transaction_id, merchant_id, user_id, card_number, transaction_date, transaction_amount, device_id, has_cbk)
        
        # Sale validation.
        # Merchant validation commented out because it induced many false negatives.
        # isValid = isValid and validate_merchant(merchants, transaction)
        isValid = isValid and validate_user(users_transactions, transaction)
        
        # Print results.
        if(isValid):
            print(transaction_id, 'CBK:', has_cbk, 'Recomendation:', 'Approve')
        else:
            print(transaction_id, 'CBK:', has_cbk, 'Recomendation:', 'Deny')
        
        
    # Script evaluation.
        isValid = not isValid
        if isValid == True and has_cbk == True:
            negative += 1
        elif isValid == True and has_cbk == False:
            fake_negative += 1
        elif isValid == False and has_cbk == True:
            fake_positive += 1
        elif isValid == False and has_cbk== False:
            positive += 1
        
        total_errors = fake_positive + fake_negative
           
    print("Positive:", positive) 
    print("Negative:", negative) 
    print("Fake Positive:", fake_positive) 
    print("Fake Negative:", fake_negative) 
    print("Error Count:", total_errors)
        
    
if __name__ == '__main__':
    main()
    