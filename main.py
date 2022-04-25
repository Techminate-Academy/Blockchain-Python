from fastapi import FastAPI
from blockchain import Blockchain
from mineblock import mine_block
from validation import chain_validation

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
   