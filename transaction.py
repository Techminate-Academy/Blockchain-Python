def add_transaction(blockchain, sender, receiver, amount):
        blockchain.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = blockchain.get_previous_block()
        return previous_block['index'] + 1