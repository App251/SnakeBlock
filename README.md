# SnakeBlock
This project is to build own block chain, which is code scratch based on following articles:

https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d

## Following packages are expected to be installed

  Python 2.7
  
  Flask
  
  Requests
  
## How to launch the app

  python app.py
  
## Examples

  Show all blocks
  
    curl localhost:5000/blocks
  
  Mine a new block
  
    curl localhost:5000/mine
    
  Make transaction
  
    curl "localhost:5000/transaction" \
     -H "Content-Type: application/json" \
     -d '{"from": "johnnyv", "to":"zidane", "amount": 3}'
