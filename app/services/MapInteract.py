def mapInteract(notes):
    import networkx as nx

    def create_node(graph, parent, value):
        graph.add_node(value)
        
        if parent is not None:
            graph.add_edge(parent, value)
        
        return value

    def create_binary_tree(data):
        graph = nx.DiGraph()
        root = create_node(graph, None, data[0])
        nodes = [root]
        
        for i in range(1, len(data)):
            parent_index = (i - 1) // 2
            parent = nodes[parent_index]
            node = create_node(graph, parent, data[i])
            nodes.append(node)
        
        return root, graph

    import openai
    max_tokens = 2000
    question = "Create an outputs similar to this set: ['pets', ['dog', 'cat'], [['bark', 'walk'], ['meow', 'purr']], [[['noise', 'dog noise'], ['action', 'action again']], [['noise', 'cat noise'], ['action', 'cat action']]]] \n\n where noise and dog noise relate to bark, action and action again relate to walk, noise and cat noise relate to meow, and action and cat action relate to purr\n\nso that each successive layer has an extra set of brackets using this text instead (make sure to extract keywords only and only create the output based on similarity/correlation between the keywords and key reminder is that you should create 2 different sets so that you don't have to relate stuff that isn't related to each other -> do this in the form of Set1:  \n Set2: ): \n\n" + notes
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
    #data = list(response["choices"][0]["text"].strip())
    data = []
    data2 = []
    data = flatten(data)
    data2 = flatten(data2)
    root1, graph1 = create_binary_tree(data)
    root2, graph2 = create_binary_tree(data2)
    # add the nodes and edges of the second graph to the first graph
    for node, data in graph2.nodes(data=True):
        graph1.add_node(node, **data)
    for edge in graph2.edges():
        graph1.add_edge(*edge)
    #pos = nx.spring_layout(graph1, scale = 5)

    # Draw the graph
    #nx.draw(graph1, pos=pos, with_labels=True, node_size=500)
    nx.draw(graph1, with_labels=True,pos=nx.kamada_kawai_layout(graph1),   node_size=100, font_size=12)
    import matplotlib.pyplot as plt

    import networkx as nx
    import plotly.graph_objs as go
    G = graph1
    # Create a graph

    # Set the layout of the graph
    pos = nx.spring_layout(G, scale=10)

    # Create the edges
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    # Create the nodes
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([f'{node}'])
        node_trace['marker']['color'] += tuple([len(list(G.neighbors(node)))])
        
    def node_hover_callback(trace, points, state):
        node_name = points.point_name
        # Do something with node_name, such as displaying additional info about the node
        
    node_trace.on_hover(node_hover_callback)

    def edge_hover_callback(trace, points, state):
        edge_idx = points.point_index
        # Do something with edge_idx, such as highlighting the edge
        
    edge_trace.on_hover(edge_hover_callback)

    def node_click_callback(trace, points, state):
        node_name = points.point_name
        subgraph_nodes = nx.descendants_at_distance(G, node_name, 2)
        # Create a new graph using the subgraph nodes and edges
        subgraph_G = G.subgraph(subgraph_nodes)
        pos = nx.spring_layout(subgraph_G)
        # Create the edge and node traces using the subgraph graph
        ...
        # Update the figure with the new traces
        fig.data = [edge_trace, node_trace]
        
    node_trace.on_click(node_click_callback)


    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>My Network Graph</br>',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002 )],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    #show fig on browser
    fig.show()
