import datetime
from uuid import uuid4

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

def mine_block(blockchain):
    previous_block = blockchain.get_previous_block()
    index = int(previous_block['index']) + 1
    previous_proof = previous_block['proof']
    pow = blockchain.proof_of_work(previous_proof)
    proof = pow['new_proof']
    previous_hash = previous_block['block_hash']
    blockchain.add_transaction(sender = node_address, receiver = 'minor_address_ea477673c3d04ca79bdd659ce3fcdfb6', amount = 1)
    timestamp = str(datetime.datetime.now())
    block_hash = blockchain.calculateHash(index, previous_hash, timestamp, proof)
    block = blockchain.create_block(index, proof, previous_hash, block_hash, timestamp)
    
    response = {
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'proof': block['proof'],
                    'block_hash': block_hash,
                    'previous_hash': block['previous_block_hash'],
                    'transactions': block['transactions']
                }
    return response