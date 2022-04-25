import hashlib

def chain_validation(blockchain):
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