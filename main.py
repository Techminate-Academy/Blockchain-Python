from fastapi import FastAPI
from blockchain import Blockchain

app = FastAPI()

# Instance of Blockchain
blockchain = Blockchain()

@app.get("/")
async def root():
    # return {"message": "Hello World"}
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    return proof['new_proof']

@app.get("/mine_block")
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    pow = blockchain.proof_of_work(previous_proof)
    proof = pow['new_proof']
    block_hash = pow['hash_operation']
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'block_hash': block_hash,
                    'previous_hash': block['previous_hash']
                }
    return response