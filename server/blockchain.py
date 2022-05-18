import datetime
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    #constructor
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        #genesis block
        self.genesis_block()
    
    #create block
    def create_block(self, index, proof, previous_hash, block_hash, timestamp):
        block = {
                    'index': index,
                    'timestamp': timestamp,
                    'proof': proof,
                    'previous_block_hash': previous_hash,
                    'block_hash': block_hash,
                    'transactions': self.transactions
                }
        self.transactions = []
        self.chain.append(block)
        return block

    #hashing data or block
    def calculateHash(self, index, previous_hash, timestamp, proof):
        data = {
                    'index': index,
                    'previous_block_hash': previous_hash,
                    'timestamp': timestamp,
                    'proof': proof
                }
        encoded_block = json.dumps(data, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    #create genesis block
    def genesis_block(self):
        index = 1
        timestamp = str(datetime.datetime.now())
        proof = 1
        previous_hash = 0
        block_hash = self.calculateHash(index, previous_hash, timestamp, proof)
        self.create_block(index=index, proof = proof, previous_hash = previous_hash, block_hash=block_hash, timestamp=timestamp)
      
    #previous block
    def get_previous_block(self):
        return self.chain[-1]

    #proof of work algorithm
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #any math operation
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        response = {
                        'new_proof':new_proof, 
                        'hash_operation':hash_operation
                    }
        return response
    
    #validate the chain / block
    def is_chain_valid(self, chain):
        previous_block = chain[0]

        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            
            #if hash of current block is equal to calculateHash of current block
            if current_block['block_hash'] != self.calculateHash(current_block['index'], current_block['previous_block_hash'], current_block['timestamp'], current_block['proof']):
                return False

            #if previous hash of current block is equal to hash of previous block
            if current_block['previous_block_hash'] != self.calculateHash(previous_block['index'], previous_block['previous_block_hash'], previous_block['timestamp'], previous_block['proof']):
                return False
            
            #check if previous proof is valid
            previous_proof = previous_block['proof']
            proof = current_block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False

            previous_block = current_block
            block_index += 1
        return True

    #list blockchain
    def get_blockchain(self):
        return  {
            'length': len(self.chain),
            'blockchain': self.chain
        }
    
    #add new transaction
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender':sender,
            'receiver':receiver,
            'amount':amount
        })

        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    #add node in the network
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
