import networkx as nx
import numpy as np
import GraphParser
# Provides the eigenvalue of the graph for calibrating the viruses

# test_graph = GraphParser.read_graph_from_edge_file('peer.all.020515')  # insert graph in question here

graph_1 = GraphParser.read_graph_from_edge_file('peer.all.020515')
print(nx.is_connected(graph_1))
"""total_ev = 0
number_of_tests = 20
# ev_array = []
for x in range(number_of_tests):
    test_graph = nx.barabasi_albert_graph(4039, 22)  # GraphParser.read_graph_from_edge_file('peer.all.020515')  # insert graph in question here
    L = nx.adjacency_matrix(test_graph)
    e = np.linalg.eigvals(L.A)
    max_e = max(e)
    total_ev += max_e
    # ev_array.append(max_e)
    print('Number of nodes: ', nx.number_of_nodes(test_graph))
    print('Number of edges: ', nx.number_of_edges(test_graph))
    print('Largest eigenvalue test: ', max_e)
total_ev = total_ev / number_of_tests
# ev_array.append(total_ev)
# save_as_name = 'Eigenvalues.txt'
# np.savetxt(save_as_name, ev_array)
print("Largest eigenvalue test average:", total_ev)"""
exit()
