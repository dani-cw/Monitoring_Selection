# 3.2 - Get your hands dirty

### 1. Analyze the data provided and present your conclusions (consider that all transactions are made using a mobile device).

* By sorting the data provided by different conditions, we can emphasize some anomalies. I split transaction times from dates to ease the analysis.

``` SQL
CREATE TABLE transactions_data (
	table_id SERIAL PRIMARY KEY,
	merchant_id INT,
	user_id INT,
	card_number VARCHAR(20),
	transaction_date CHAR(10),
	transaction_time CHAR(15),
	transaction_amount NUMERIC(14,2),
	device_id INT,
	has_cbk BOOL
);

COPY transactions_data(transaction_id,merchant_id,user_id,card_number,transaction_date,transaction_time,transaction_amount,device_id,has_cbk)
FROM 'C:\sampledir\transactional-sample-edited.csv'
DELIMITER ','
CSV HEADER;
```

* We start by sorting the ```'has_cbk_' bool```, as it exhibit the fraudulent transactions. Sorted by time.

``` SQL
SELECT * FROM transactions_data WHERE has_cbk IS true ORDER BY transaction_date ASC, transaction_time ASC;
```

* The first evident examples of possible frauds are many transaction by the same user, in a small amount of time. This suggests bust-out activity, where a usage pattern is abused with numerous charges instead of a big, more noticeable one. This can be found among many transactions on this data chart, e.g. ```user_id 75710```

``` SQL
transaction_id,merchant_id,user_id,card_number,transaction_date,transaction_time,transaction_amount,device_id,has_cbk

2934,21323331,77130,75710,"554482******7640","2019-11-08","23:05:13.814924",540.81,NULL,True
2933,21323330,77130,75710,"554482******7640","2019-11-08","23:11:18.971808",320.96,NULL,True
2932,21323329,77130,75710,"554482******7640","2019-11-08","23:12:00.465991",254.37,NULL,True
2931,21323328,77130,75710,"554482******7640","2019-11-08","23:14:35.977303",386.82,NULL,True
2930,21323327,77130,75710,"554482******7640","2019-11-08","23:15:05.322183",599.13,NULL,True
2929,21323326,77130,75710,"554482******7640","2019-11-08","23:17:08.619645",473.44,NULL,True
2928,21323325,77130,75710,"554482******7640","2019-11-08","23:18:28.634342",254.25,NULL,True
2924,21323321,77130,75710,"554482******7640","2019-11-09","00:17:27.310174",559.01,NULL,True
2923,21323320,77130,75710,"554482******7640","2019-11-09","00:58:24.689418",593.78,NULL,True
```

* We can also find some suggestions of Card Block Fraud, where a script generate a block of card numbers, used by the fraudster to brute force their way into an approval. This can be shown by the small interval between transactions, the same BIN (first 6 digits), and _usually_ one purchase per card, e.g. ```CSV '406655 ...' ```

``` SQL
transaction_id,merchant_id,user_id,card_number,transaction_date,transaction_time,transaction_amount,device_id,has_cbk

741,21321138,4705,91637,"406655******7631","2019-11-29","01:20:14.182107",930.6,563499,True
735,21321132,1308,96025,"406655******5763","2019-11-29","02:02:30.874661",2904.6,438940,True
732,21321129,1308,96025,"406655******4608","2019-11-29","02:10:25.828340",2819.59,438940,True
730,21321127,1308,96025,"406655******5764","2019-11-29","02:35:55.206318",2774.51,438940,True
729,21321126,1308,79054,"406655******7948","2019-11-29","02:52:00.400886",2019.47,101848,True
728,21321125,1308,79054,"406655******5763","2019-11-29","02:58:04.351521",1834.09,101848,True
725,21321122,1308,96025,"406655******4572","2019-11-29","03:17:30.558440",1648.3,438940,True
724,21321121,1308,96025,"406655******5764","2019-11-29","03:30:43.934091",2486.7,438940,True
710,21321107,1308,96025,"406655******5764","2019-11-29","11:32:14.313926",2412.28,438940,True
709,21321106,1308,79054,"406655******5169","2019-11-29","11:40:49.445144",2251.02,101848,True
706,21321103,1308,79054,"406655******7948","2019-11-29","11:49:14.553339",2183.76,101848,True
693,21321090,1308,79054,"406655******7343","2019-11-29","12:51:17.927921",2231.98,101848,True
```

* Note that the ```user_id``` isn't necessarily the same, as the perpetrator might try using more then one user to avoid account locking. Notice, as well, the irregular time intervals.
  
* In fact, if we filter by ```merchant_id```, it can be noted that ```merchant_id == 1308``` is usually involved on the ```CSV '406655 ...' ``` cases, maybe as a victim, but probably as the perpetrator.

``` SQL
-- Ordering by merchants can help seeing the ones with a lot of chargebacks.
SELECT * FROM transactions_data WHERE has_cbk IS true ORDER BY merchant_id ASC

-- With the following query, we can analyze the whole merchant_id = 1308 transaction history
SELECT * FROM transactions_data WHERE merchant_id = 1308 ORDER BY transaction_date ASC, transaction_time ASC;

-- Which shows all of their transactions are fraudulent
"table_id","transaction_id","merchant_id","user_id","card_number","transaction_date","transaction_time","transaction_amount","device_id","has_cbk"
735,21321132,1308,96025,"406655******5763","2019-11-29","02:02:30.874661",2904.60,438940,True
732,21321129,1308,96025,"406655******4608","2019-11-29","02:10:25.828340",2819.59,438940,True
730,21321127,1308,96025,"406655******5764","2019-11-29","02:35:55.206318",2774.51,438940,True
729,21321126,1308,79054,"406655******7948","2019-11-29","02:52:00.400886",2019.47,101848,True
728,21321125,1308,79054,"406655******5763","2019-11-29","02:58:04.351521",1834.09,101848,True
725,21321122,1308,96025,"406655******4572","2019-11-29","03:17:30.558440",1648.30,438940,True
724,21321121,1308,96025,"406655******5764","2019-11-29","03:30:43.934091",2486.70,438940,True
710,21321107,1308,96025,"406655******5764","2019-11-29","11:32:14.313926",2412.28,438940,True
709,21321106,1308,79054,"406655******5169","2019-11-29","11:40:49.445144",2251.02,101848,True
706,21321103,1308,79054,"406655******7948","2019-11-29","11:49:14.553339",2183.76,101848,True
693,21321090,1308,79054,"406655******7343","2019-11-29","12:51:17.927921",2231.98,101848,True
604,21321001,1308,96025,"406655******4980","2019-11-29","16:36:00.073092",2261.25,438940,True
597,21320994,1308,96025,"406655******7343","2019-11-29","16:46:59.421700",2288.47,438940,True
570,21320967,1308,96025,"406655******7343","2019-11-29","17:42:40.460221",2259.99,438940,True
566,21320963,1308,96025,"406655******4980","2019-11-29","17:49:01.844537",2141.93,438940,True
```
* By running a script for detecting which merchants **ONLY** have ```has_cbk == true```, we can see ```merchant_id = 1308``` is a probable fraudster.

``` python
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
        
        #result = validate_merchant(merchants, transaction) 
        result = validate_users(users, transaction)
        
# Debug for merchant dictionary.   
#    print (merchants)

    # Print fraudsters, based on choice (1 for merchants, 2 for users).
    # Add (,) to the print(key) if you wish to use the results on a SQL query. -> print(key, ",")
    if(result == 1):
        for key in merchants.keys():
            if (merchants[key]["isFraudster"] == 0):
                print(key)
    elif(result == 2):            
        for key in users.keys():
            if (users[key]["isFraudster"] == 0):
                print(key)    
    # For SQL query usage, drop the results between 'transactions_data WHERE merchant_id IN (HERE)' 
    # or  'transactions_data WHERE user_id IN (HERE)'.
```
* Which returns:
```
77570
41354
8942 
70899
25932
45399
7535 
94053
74450
9292
89943
25199
75917
65241
11911
1017
96692
84902
38337
62988
52897
8787
74211
35917
76239
2842
54603
1175
62613
5763
44927
59875
91352
67075
3109
73922
73271
73205
13096
46609
21281
5252
81795
48126
1308 -> The aforementioned merchant.
18768
83982
38568
15326
23531
3531
15950
4694
83142
72723
99644
92215
11570
5533
62194
67764
49710
56977
11470
53816
68657
```
* Using the same script, but for users, you can also find out ```user_id = 75710```, responsible for the bust-out fraud activity earlier, also only have transactions with ```has_cbk = true```.

* You can observe similar patterns and behaviors in other transactions, but the aforementioned examples sum up the reason for most of the chargebacks and probable frauds, at lease with the amount of data given.

---
### 2. In addition to the spreadsheet data, what other data would you look at to try to find patterns of possible frauds?

> IP address and/or coordinates of user device usage:
* Large discrepancies between places of usage for a single user could suggest security breaches.
* The identity theft could be caused from a variety of reasons, from convenience, to social engineering or hacking.
* IPs from different countries, or known VPN might flag illegal activity.

> User and merchant personal data (CPF, full name, family ties):
* Finding links between merchant and user might indicate self-funding or family-funding, using payment advancements for working capital. 
* Fake sales might be done involving those agents for money laundering activity.

> Merchant business data (CNPJ, business partners, commercial activity, anticipate rule):
* Sales between business associates suggests self-funding or business-funding.
* Commercial activity indicate certain transactions with unusual values might not be regular.
* Additionally, some commercial activities might restrict certain payment methods (e.g. asking to deliver ready-to-eat perishable food to another state)

> Public or private presence (of merchants and users) in white, warn or hot lists: 
* White lists allow the completion of suspicious transactions that might otherwise be blocked, because of already justifies behavior.
* Warm lists warn users and merchants whom are already being investigated for suspicious behavior. Transactions must be carefully analyzed, and might generate a block.
* Hot lists are responsible for warning about proven fraudsters, or merchants/users involved with illicit activities, like involvement with terrorism financing, for example.

> Time between transaction and chargeback request, and reason given:
* Treatment for satisfaction or non-reception chargebacks severely differs from credit card fraud or identity theft frauds. This changes the outcome for the merchant and user, as well as the analysis made.
* Return policies might be abused by consumer fraudsters, whom request devolution, and chargebacks, by cause of dissatisfaction. The reiterated occurrence, or a long period before asking for devolution, might help reduce those occurrences.

> Denied transaction requests:
* Non successful transaction requests help on denying many frauds before they actually happen. Card block fraud can be stopped by blocking users on the first attempts. 
* Many denied transactions should warm list the user and merchant, for further investigation, and possibly blocking, white listing, or other adequate measures.

> For e-markets, shipping address:
* Many sales to the same shipping address might suggest a drop off point, which criminal organizations can use to collect the bought products without compromising their address.

> Merchant social media pages and transaction records can't be quickly analyzed through a data spreadsheet, but are useful for manual checks.


