from fastapi import FastAPI, status
from blockchain import Blockchain
from mineblock import mine_block
from validation import chain_validation
from transaction import add_transaction
#instance of FastAPI
app = FastAPI()

# Instance of Blockchain
blockchain = Blockchain()

@app.get("/")
async def root():
    return 'ok'

@app.get("/mine_block")
async def mine_new_block():
    return mine_block(blockchain)

@app.get("/get_blockchain")
async def list_blockchain():
    return blockchain.get_blockchain()

@app.get("/get_chain_validation")
async def blockchain_validation():
    return chain_validation(blockchain)
   
@app.get("/add_transaction/", status_code=status.HTTP_200_OK,)
async def add_new_transaction(sender:str, reciever:str, amount:int):
    txs_data = {'sender': sender, 'reciever':reciever, 'amount':amount}
    transaction_keys = ['sender', 'reciever', 'amount']
    if not all(key in txs_data for key in transaction_keys):
        return 'Some elements of the transaction are missing'
    index = blockchain.add_transaction(txs_data['sender'], txs_data['reciever'], txs_data['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return response


# Connecting new nodes
@app.get('/connect_node', status_code=status.HTTP_200_OK,)
async def connect_node(node:str):
    if node is None:
        return "No node", 400
    blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': blockchain.nodes}
    return response

