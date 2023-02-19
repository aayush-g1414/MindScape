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
data = ['operating system', ['resource management', 'process management', 'memory management'], [['cpu', 'memory', 'storage'], ['execution', 'simultaneously'], ['allocates', 'deallocates']], [[['security', 'mechanisms'], ['protect', 'unauthorized access', 'malware']], [['user interface', 'interact']]]]
data2 = ['types of operating systems', ['single-tasking', 'multi-tasking', 'real-time', 'network', 'mobile', 'embedded'], [['one program', 'one program at a time'], ['multiple programs or processes', 'simultaneously'], ['real-time applications', 'strict timing requirements'], ['manage', 'administer'], ['smartphones', 'tablets'], ['cars', 'appliances', 'medical devices']]]
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
graph1.write_png('set1_tree.png')
graph2.write_png('set2_tree.png')