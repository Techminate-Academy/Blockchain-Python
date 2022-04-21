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
    previous_proof = previous_block['proof']
    pow = blockchain.proof_of_work(previous_proof)
    proof = pow['new_proof']
    block_hash = pow['hash_operation']
    previous_hash = blockchain.hash(previous_block)
    timestamp = str(datetime.datetime.now())
    block = blockchain.create_block(proof, previous_hash, block_hash, timestamp)
    response = {
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'block_hash': block_hash,
                    'previous_hash': block['previous_hash']
                }
    return response

@app.get("/get_blockchain")
async def get_blockchain():
    return {
            'length': len(blockchain.chain),
            'blockchain': blockchain.chain
        }