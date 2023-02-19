import os


def mapImage(notes):
    import pydot

    def create_node(graph, parent, value):
        node = pydot.Node(value)
        graph.add_node(node)
        
        if parent is not None:
            edge = pydot.Edge(parent, node)
            graph.add_edge(edge)
        
        return node

    def create_binary_tree(data):
        graph = pydot.Dot(graph_type='graph')
        root = create_node(graph, None, data[0])
        nodes = [root]
        
        for i in range(1, len(data)):
            parent_index = (i - 1) // 2
            parent = nodes[parent_index]
            node = create_node(graph, parent, data[i])
            nodes.append(node)
        
        return root, graph
    #data should be a response from openai GPT3
    import openai
    max_tokens = 2000
    openai.api_key = os.getenv('OPEN_AI_API_KEY')
    question = "Create an outputs similar to this set: ['pets', ['dog', 'cat'], [['bark', 'walk'], ['meow', 'purr']], [[['noise', 'dog noise'], ['action', 'action again']], [['noise', 'cat noise'], ['action', 'cat action']]]] \n\n where the first word is byitself/the root, noise and dog noise relate to bark, action and action again relate to walk, noise and cat noise relate to meow, and action and cat action relate to purr\n\nso that each successive layer has an extra set of brackets using this text instead (make sure to extract keywords only and only create the output based on similarity/correlation between the keywords and key reminder is that you should create 2 different sets so that you don't have to relate stuff that isn't related to each other -> do this in the form of Set1:  \n Set2: ): \n\n" + notes
    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=question,
                        temperature=0.1,
                        max_tokens=max_tokens,
                        top_p=1.0,
                        frequency_penalty=0.0,
                        presence_penalty=0.0
                    )
    print(response["choices"][0]["text"].strip())
    response = response["choices"][0]["text"].strip()
    #data = list(response["choices"][0]["text"].strip())
    import ast
    data = response.split(":")[1][1:-5].strip()
    data2 = response.split(":")[-1][1:].strip()
    print(response)
    print('data: '+str(data))
    print('data2: ' + str(data2))
    data = ast.literal_eval(data)
    data2 = ast.literal_eval(data2)

    print(type(data[0]))



    def flatten(lst):
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(flatten(item))
            else:
                result.append(item)
        return result

    data = flatten(data)
    data2 = flatten(data2)
    root1, graph1 = create_binary_tree(data)
    root2, graph2 = create_binary_tree(data2)
    #graph1.add_edge(pydot.Edge(root1, root2, dir='none'))
    #nx.draw(graph1)

    #download images on frontend
    graph1.write_png(f'mindmaps/set1_tree{notes[:10]}.png')
    return f'set1_tree{notes[:10]}.png'
    graph2.write_png('mindmaps/set2_tree.png')