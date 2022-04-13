# 3.1 Undestand The Industry

### 1. Explain the money flow and the information flow in the acquirer market and the role of the main players.

* The payment information is sent from the Gateway to the **Acquirer** which will process the payment on behalf of a merchants, debit or credit, enabling stores to offer various payment conditions. The info is processed and passed to the card brand.
  
* **Card Brands** set business rules and standards for purchases made with credit cards, by which the Acquirer must process the payment insuring they fulfill the requirements. The information, therefore, is received from the Acquirer, validate the conditions, and send the data to the Issuing Bank.
  
* The financial institution actually responsible for collecting the value is the **Issuing Bank**. It will verify if the buyer has sufficient credit available, and is the final step in authorizing the sale. The value is then sent from the client to the acquirer, and finally back to the merchant (through their bank).


---
### 2. Explain the difference between acquirer, sub-acquirer and payment gateway and how the flow explained in question 1 changes for these players.

* **Payment Gateway** is the first player in the payment flow. It sends the payment request, and receives responses in order to know if it was approved. Acts as a terminal, integrating th transactions between all the players.
  
* The **Acquirer** will actually process the information sent by the Gateway, providing the various payment conditions, as it is responsible for the relationship in the payment card arrangement. It manages communication between credit associations and businesses, ensuring transaction security, fraud protection, and respecting various rules and guidelines. It will be the responsible in case of a data breach.
  
* Finally, the **sub-acquirer** is an intermediary player between the acquirer and store, not always present. Although it process payments and transmits the data, it doesn't completely replace the acquirer due to the lack of autonomy to perform all of their functions. Although usually costly for merchants, it's sometimes an important step, specially for small stores, because of the provided anti-fraud system and ease of integration. It can be usually identified by the redirection to its own page during the final steps of the checkout, which is sometimes responsible for withdraw from the buyer.
  
* The presence of a sub-acquirer on the payment flow alters it by including an extra step, where after the issuing bank sends the money to the acquirer, it is not sent directly to the merchant account, but first through the sub-acquirer.


---
### 3. Explain what chargebacks are, how they differ from cancellations and what is their connection with fraud in the acquiring world.
* With a **cancellation**, the company responsible for the sale agrees to return a payment (or other charge) to its costumers, upon request. Payment processing is handled by the players, and the values returned to their rightful owners.

* When the request by the costumers for the cancellation of the transaction is not requested, or if they can't reach the merchant, a **chargeback** is filed with the acquiring bank. 
  
* Chargeback is the term used to describe a request for the money to be returned to the consumer. It generates costs for all the players involved (including fees), so they should be avoided, by improvements on the payment system security and policies.

* With that said, fraud is only one of the reason for disputes, the other three main being authorization (merchant conduct not allowed), processing (wrong information was used) and consumer dispute (related to the product or service). 

* Disputes, therefore, can be considered any disagreement between merchant and consumer, fraud being merely one of the reasons.
  
* Fraud is an type of dispute, caused by a consumer being impersonated, or by their data being stolen, and used for unauthorized transactions.
  
* There is always a risk of fraudulent transactions, and the players should work hard to avoid them. Although not every dispute is caused by a fraud, a fraud **always** causes a dispute, generating fees and financial loss for all parts involved.