def update_chain_with_new_block(blockchain):
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response =  {
                        'message': 'Chain is updated with the latest block',
                        'new_chain': blockchain.chain
                    }
    else:
        response = {'message': 'this node mined the last block',
                    'actual_chain': blockchain.chain}
    return response, 200