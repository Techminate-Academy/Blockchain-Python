
from flask import Flask, request
from uuid import uuid4

from blockchain import Blockchain
from mineblock import mine_block
from validation import chain_validation
from transaction import new_transaction
from network import connect_to_network
from consensus import update_chain_with_new_block

# Creating a Web App
app = Flask(__name__)

# Blockchain instance
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_new_block():
    return mine_block(blockchain)

@app.route('/get_blockchain', methods = ['GET'])
def list_blockchain():
    return blockchain.get_blockchain()

@app.route('/get_chain_validation', methods = ['GET'])
def blockchain_validation():
    return chain_validation(blockchain)

@app.route('/add_transaction', methods = ['POST'])
def add_new_transaction():
        return new_transaction(blockchain, request)

# Connecting new nodes
@app.route('/connect_to_network', methods = ['POST'])
def connect_node():
    return connect_to_network(blockchain, request)

# Replacing the chain by the longest chain if needed
@app.route('/update_chain', methods = ['GET'])
def update_chain():
  return update_chain_with_new_block(blockchain)

# Running the app
app.run(host = '0.0.0.0', port = 5000)