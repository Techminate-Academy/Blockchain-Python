import datetime
import hashlib
import json

class Blockchain:

    #constructor
    def __init__(self):
        self.chain = []
        #genesis block
        self.create_block(proof = 1, previous_hash = '0')
    
    #create block
    def create_block(self, proof, previous_hash):
        block = {
                    'index': len(self.chain) + 1,
                    'timestamp': str(datetime.datetime.now()),
                    'proof': proof,
                    'previous_hash': previous_hash
                }
        self.chain.append(block)
        return block
        
    #previous block
    def get_previous_block(self):
        return self.chain[-1]

    #proof of work algorithm
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #any hard to calculate math operation
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #hashing data or block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #validate the chain / block
    def is_chain_valid(self, chain):
        previous_block = chain[0]

        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            
            #check if previous hash of the block is valid
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            #check if previous proof is valid
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True
