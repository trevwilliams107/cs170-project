#!/usr/bin/env python3

import networkx as nx
import numpy as np
import random
import student_utils as su



def generate_random_graph(n, max_weight):
    G = nx.Graph()
    G.add_nodes_from(np.arange(1, n + 1))
    count = 0
    for j in np.arange(1, n + 1):
        weight = random.randrange(1, max_weight)
        G.add_edge(j, j + 1, weight = weight)
        count += 1
    i = 1
    while i < 5 * n:
        #count += 1
        u = random.randrange(1, n)
        v = random.randrange(1, n)
        w = random.randrange(1, max_weight + 1)
        if (u == v):
            v = v + 1
        neighbors = G[u]
        if (v not in neighbors) :
            G.add_edge(u, v, weight = w)
            count += 1
        else:
            #i -= 1
            continue
        i += 1

    delete = {}
    shortest = dict(nx.floyd_warshall(G))
    for u1, v1, datadict in G.edges(data=True):
        if abs(shortest[u1][v1] - datadict['weight']) >= 0.00001:
            if (not (u1 in delete.keys())):
                delete.setdefault(u1, [])
            delete[u1].append(v1)
    for key in delete:
        for val in delete[key]:
            G.remove_edge(key, val)



        # shortest = dict(nx.floyd_warshall(G))
        # vtou = shortest[u][v]
        #
        # if (w>vtou):
        #     G.remove_edge(u, v)
        #     count -= 1
        #
        #
        #
        #
        # #sp_v_to_u = nx.single_source_dijkstra_path_length(G, v, cutoff=None, weight='weight')[u]
        # #sp_u_to_v = nx.single_source_dijkstra_path_length(G, u, cutoff=None, weight='weight')[v]
        # #if (sp_v_to_u < w or sp_u_to_v < w):
        # #    G.remove_edge(u, v)
        # #    count -= 1
        #     #i -= 1
        # else:
        #     i += 1

        #f.write("hi" + str(i) + '\n')
    file = open("matrix.txt", "w")
    matrix = nx.to_numpy_matrix(G, weight='weight', nonedge=0)
    asarray_matrix = np.asarray(matrix)
    #a = '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix])

    b = [[0 for x in range(n + 1)] for y in range(n + 1)]
    for i in np.arange(n + 1):
        for j in np.arange(n + 1):
            b[i][j] = asarray_matrix[i][j]

    for i in np.arange(n + 1):
        for j in np.arange(n + 1):
            if (b[i][j] == 0.0):
                file.write('x' + ' ')
            else:
                file.write(str(b[i][j]) + ' ')
        file.write('\n')

    homes = np.arange(1, n, 2)
    file.write(str(n + 1) + '\n')
    file.write(str(len(homes)) + '\n')
    file.write(str(np.arange(1, n + 2)) + '\n')
    file.write(str(homes) + '\n')
    print(homes)
    file.close()
    #print("count is " + str(count))
    return matrix
    #return nx.number_of_edges(G)


n = 49
a = generate_random_graph(n, 50)
asar = np.asarray(a)
b = [[0 for x in range(n + 1)] for y in range(n + 1)]
for i in np.arange(n + 1):
    for j in np.arange(n + 1):
        b[i][j] = asar[i][j]
print(len(asar[1]))

#graph = su.adjacency_matrix_to_graph(asar)

#metric = su.is_metric(a)


#print(asar)
#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in b]))
#print(np.matrix(b))

#print(len(asar))
#print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in a]))
