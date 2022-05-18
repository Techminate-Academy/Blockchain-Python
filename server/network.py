def connect_to_network(blockchain, request):
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
                    'message': 'Connected to the network',
                    'total_nodes': list(blockchain.nodes)
                }
    return response, 201