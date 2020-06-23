import networkx as nx


# reads from an input file at <filename> and returns a networkx graph
# the file hast to contain for each line exactly one edge represented by one pair of nodes (as numbers) separated by ":"
# Example:
# 1:4
# 42:256
# 4:256
def read_graph_from_edge_file(filename):
    net_graph = nx.Graph()
    with open(filename) as f_obj:
        lines = f_obj.readlines()
    for line in lines:
        nodes = line.rstrip().split(':')
        for node in nodes:
            node = int(node)
        net_graph.add_edge(int(nodes[0]), int(nodes[1]))
    # maps node names to consecutive integers (this function can label them with their old name if necessary)
    net_graph = nx.convert_node_labels_to_integers(net_graph)
    return net_graph
