def new_transaction(blockchain, request):
        txs_data = request.get_json()
        transaction_keys = ['sender', 'receiver', 'amount']
        if not all(key in txs_data for key in transaction_keys):
            return 'Some elements of the transaction are missing', 400
        index = blockchain.add_transaction(txs_data['sender'], txs_data['receiver'], txs_data['amount'])
        response = {'message': f'This transaction will be added to Block {index}'}
        return response, 201