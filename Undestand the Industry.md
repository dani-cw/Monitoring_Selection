# 3.1 Undestand The Industry

### 1. Explain the money flow and the information flow in the acquirer market and the role of the main players.

* The payment information is sent from the Gateway to the **Acquirer** which will process the payment on behalf of a merchants, debit or credit, enabling stores to offer various payment conditions. The info is processed and passed to the card brand.
  
* **Card Brands** set business rules and standards for purchases made with credit cards, by which the Acquirer must process the payment insuring they fulfill the requirements. The information, therefore, is received from the Acquirer, validate the conditions, and send the data to the Issuing Bank.
  
* The financial institution actually responsible for collecting the value is the **Issuing Bank**. It will verify if the buyer has sufficient credit avaiable, and is the final step in authorizing the sale. The value is then sent from the client to the acquirer, and finally back to the merchant (through their bank).


---
### 2. Explain the difference between acquirer, sub-acquirer and payment gateway and how the flow explained in question 1 changes for these players.

* **Payment Gateway** is the first player in the payment flow of a sale in Brazil. It sends the payment request, and receives responses in order to know if it was approved. Acts as a terminal, integrating th transactions between all the players.
  
* The **Acquirer** will actually process the information sent by the Gateway, providing the various payment conditions, as it is responsible for the relationship in the payment card arrangement. It manages communication between credit associations and businesses, ensuring transaction security, respecting various rules and guidelines. It will be the responsible in case of a data breach.
  
* Finally, the **sub-acquirer** is an intermediary player between the acquirer and store, not always present. Although it process payments and transmits the data, it doesn't completely replace the acrquirer due to the lack of autonomy to perform all of their functions. Although usually costly for mechants, it's sometimes an important step, specially for small stores, because of the provided anti-fraud system and ease of integration. It can be usually identified by the redirection to its own page during the final steps of the checkout, which is sometimes responsible for withdrawl from the buyer.
  
* The presence of a sub-acquirer on the payment flow alters it by including an extra step, where the after the issuing bank sends the money to the acquirer, it is not sent directly to the merchant account, but first through the sub-acquirer.


---
### 3. Explain what chargebacks are, how they differ from cancellations and what is their connection with fraud in the acquiring world.