from wsgiref import validate
from fastapi import FastAPI
from blockchain import Blockchain
import datetime
import hashlib
import json

app = FastAPI()

# Instance of Blockchain
blockchain = Blockchain()

@app.get("/")
async def root():
    index = 1
    timestamp =str(datetime.datetime.now())
    proof = 1
    previous_hash = 0
    block = {
                'index': index,
                'timestamp': timestamp,
                'proof': proof,
                'previous_hash': previous_hash
            }
    encoded_block = json.dumps(block, sort_keys = True).encode()
    current_hash = hashlib.sha256(encoded_block).hexdigest()
    return {
                'index': index,
                'timestamp': timestamp,
                'proof': proof,
                'block_hash': current_hash,
                'previous_hash': previous_hash
            }

@app.get("/mine_block")
def mine_block():
    previous_block = blockchain.get_previous_block()
    index = int(previous_block['index']) + 1
    previous_proof = previous_block['proof']
    pow = blockchain.proof_of_work(previous_proof)
    proof = pow['new_proof']
    previous_hash = previous_block['block_hash']
    timestamp = str(datetime.datetime.now())
    block_hash = blockchain.calculateHash(index, previous_hash, timestamp, proof)
    block = blockchain.create_block(index, proof, previous_hash, block_hash, timestamp)
    response = {
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'block_hash': block_hash,
                    'previous_hash': block['previous_block_hash']
                }
    return response

@app.get("/get_blockchain")
async def get_blockchain():
    return {
            'length': len(blockchain.chain),
            'blockchain': blockchain.chain
        }

@app.get("/get_chain_validation")
async def chain_validation():
    # is_valid = blockchain.is_chain_valid(blockchain.chain)
    previous_block = blockchain.chain[0]

    block_index = 1
    while block_index < len(blockchain.chain):
        current_block = blockchain.chain[block_index]
        
        #if hash of current block is equal to calculateHash of current block
        # validation_1 = {
        #     'hash' : current_block['block_hash'],
        #     'calculated_hash' : blockchain.calculateHash(current_block['index'], current_block['previous_block_hash'], current_block['timestamp'], current_block['proof'])
        # }
        # return validation_1
        if current_block['block_hash'] != blockchain.calculateHash(current_block['index'], current_block['previous_block_hash'], current_block['timestamp'], current_block['proof']):
            return {'message':'not valid'}

        #if previous hash of current block is equal to hash of previous block
        # validation_2 = {
        #     'previous_hash' : current_block['previous_block_hash'],
        #     'calculated_previous_hash' : blockchain.calculateHash(previous_block['index'], previous_block['previous_block_hash'], previous_block['timestamp'], previous_block['proof'])
        # }
        if current_block['previous_block_hash'] != blockchain.calculateHash(previous_block['index'], previous_block['previous_block_hash'], previous_block['timestamp'], previous_block['proof']):
            return {'message':'not valid'}

        #check if the pow is valid and starts with n amount of zero
        previous_block_proof = previous_block['proof']
        current_block_proof = current_block['proof']
        hash_operation = hashlib.sha256(str(current_block_proof**2 - previous_block_proof**2).encode()).hexdigest()
        # if hash_operation[:4] == '0000':
        #     validation_3 = {
        #         'previous_block_proof' : previous_block['proof'],
        #         'current_block_proof' : current_block['proof'],
        #         'hash_operation' : hash_operation
        #     }
        #     return validation_3
        # else:
        #     return {'error':'not valid'}
       
        if hash_operation[:4] != '0000':
            return {'message':'not valid'}

        previous_block = current_block
        block_index += 1

    return {'message':'chain is valid'}
   