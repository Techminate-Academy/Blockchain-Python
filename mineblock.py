import datetime

def mine_block(blockchain):
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