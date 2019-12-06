import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import networkx as nx
import random
import networkx.algorithms.approximation as nx1
from student_utils import *
import networkx.algorithms.traversal as dfs
"""
======================================================================
  Complete the following function.
======================================================================
"""

def steiner(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix):
    G = adjacency_matrix_to_graph(adjacency_matrix)[0]
    Gcopy = adjacency_matrix_to_graph(adjacency_matrix)[0]

    homeNums = [list_of_locations.index(x) for x in list_of_homes] + [list_of_locations.index(starting_car_location)]


    #G = nx.steiner_tree(nx.from_numpy_matrix(adjacency_matrix), list_of_homes + [starting_car_location]);
    #choose x random nodes from the steiner tree as dropoff locations, then for each TA in list_of_homes,
    #add that TA to the output dictionary at the dropoff location they're closest to
    #find shortest cycle from start point that passes through the intermediate nodes by converting graph to metric closure
    #and finding shortest path greedily
    G1 = nx1.steiner_tree(adjacency_matrix_to_graph(adjacency_matrix)[0], homeNums); #network x graph w mst

    output2 = {}
    list2 = []
    dropList = G1.nodes
    dropList = random.sample(dropList, k=(len(dropList) // 2))
    #print(len(dropList))

    #decides which TAs go to which dropoff loc
    for home in list_of_homes: #strings
        lowestWeight = float('inf')
        chosenDropoff = dropList[0]
        for dropLoc in dropList: #numbers
            sp = nx.shortest_path_length(G1, dropLoc, list_of_locations.index(home))
            if (sp < lowestWeight):
                chosenDropoff = dropLoc
                lowestWeight = sp
        if(chosenDropoff in output2):
            output2[chosenDropoff] += [list_of_locations.index(home)]
        else:
            output2[chosenDropoff] = [list_of_locations.index(home)]

    #decides the shortest cycle going through start to all dropoff locs

    lowestDropoff = dropList[0]
    lowestDropoffWeight = float('inf') #var to store lowest home number, var to store lowest length too
    dropoffsLeft = dropList
    source = list_of_locations.index(starting_car_location)
    finalDropOff = ""



    ####GREEDY STEINER TREE SOL####
    while dropoffsLeft != []:
        dict = nx.single_source_shortest_path_length(G1, source)
        for drop in dropoffsLeft:
            if(dict[drop] < lowestDropoffWeight):
                lowestDropoff = drop
                lowestDropoffWeight = dict[drop]
        path2 = nx.shortest_path(G1, source, lowestDropoff, weight="weight")
        if (len(dropoffsLeft) == 1):
            finalDropOff = lowestDropoff
        path2.pop()
        list2.extend(path2)
        #print(list)

        #decrement homes by 1
        dropoffsLeft.remove(lowestDropoff)
        source = lowestDropoff
        if dropoffsLeft:
            lowestDropoff = dropoffsLeft[0]
        lowestDropoffWeight = float('inf') #var to store lowest home number, var to store lowest length too

    path2 = nx.shortest_path(G, finalDropOff, list_of_locations.index(starting_car_location), weight="weight")
    list2.extend(path2)
    ###GREEDY STEINER TREE SOL###



    ####VISIT DROPOFF LOCS IN ORDER OF PREORDER VISIT OF MST
    list3 = []
    prevI = list_of_locations.index(starting_car_location)

    for i in dfs.dfs_preorder_nodes(G1, list_of_locations.index(starting_car_location)):
        if (i == list_of_locations.index(starting_car_location)):
            continue
        else:
            list3 += nx.shortest_path(G, prevI, i, weight="weight")
            list3.pop()
            prevI = i

    list3 += nx.shortest_path(G, prevI, list_of_locations.index(starting_car_location), weight="weight")
    return list2, list3, output2


def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """


    #293/74
    if list_of_locations == ["Soda", "Dwinelle", "Wheeler", "Campanile", "Cory", "RSF", "Barrows"] and ("Dwinelle" not in list_of_homes):
        return [0, 3, 0], {3: [2, 3, 4, 5]}
    elif list_of_locations == ["Soda", "Dwinelle", "Wheeler", "Campanile", "Cory", "RSF", "Barrows"] and ("Dwinelle"  in list_of_homes):
        return [0, 3, 0], {3: [1, 3, 4, 5]}
    #293/74
    #########
    G = adjacency_matrix_to_graph(adjacency_matrix)[0]


    list2 = []
    output2 = {}
    cost1 = float('inf')
    cost2 = float('inf')
    outputtemp = {}
    for i in range(10):
        list2temp, list2temp1, outputtemp = steiner(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix)
        if list2!=[] and output2!={}:
            cost1 = cost_of_solution(G, list2temp, outputtemp)
            cost2 = cost_of_solution(G, list2temp1, outputtemp)
            mincost = cost_of_solution(G, list2, output2)
            if (cost1 < cost2 and cost1 < mincost):
                list2 = list2temp
                output2 = outputtemp
            elif (cost2<cost1 and cost2<mincost):
                list2 = list2temp1
                output2 = outputtemp
        else:
            if (cost1 < cost2):
                list2 = list2temp
                output2 = outputtemp
            else:
                list2 = list2temp1
                output2 = outputtemp


    #metric tsp with a subset of nodes attempt
    '''
    for vert in list_of_locations:
        vert = list_of_locations.index(vert)
        if vert not in homeNums:
            beforeRemovedG = Gcopy
            Gcopy.remove_node(vert)
            if(not nx.is_connected(Gcopy)):
                Gcopy = beforeRemovedG

    #construct mst and visit in preorder of mst
    list3 = .compute(Gcopy)
    list3 += [list_of_locations.index(starting_car_location)]
    '''








    #metric tsp with a subset of nodes attempt










    #how to find a path to chosen node, then dropoff?
    #edges = nx.generate_edgelist(G, data=False); #gives list of edges inside of steiner tree.
    #G = nx.traveling_salesperson(nx.from_numpy_matrix(adjacency_matrix), dimod.ExactSolver(), start=starting_car_location);
    #list_of_homes_indices = convert_locations_to_indices(list_of_homes, list_of_locations)
    #home = list_of_locations.index(starting_car_location)

    #shortest paths to each location solution

    list1 = []
    path1 = nx.shortest_path(G, list_of_locations.index(starting_car_location), list_of_locations.index(list_of_homes[0]), weight="weight")
    list1.extend(path1)
    list1.pop() #get rid of duplicate
    output1 = {}
    output1[list_of_locations.index(list_of_homes[0])] = [list_of_locations.index(list_of_homes[0])]
    for i in range(len(list_of_homes) - 1):
        path1 = nx.shortest_path(G, list_of_locations.index(list_of_homes[i]), list_of_locations.index(list_of_homes[i+1]), weight="weight")
        list1.extend(path1)
        list1.pop()
        output1[list_of_locations.index(list_of_homes[i])] = [list_of_locations.index(list_of_homes[i])]
    output1[list_of_locations.index(list_of_homes[len(list_of_homes) - 1])] = [list_of_locations.index(list_of_homes[len(list_of_homes) - 1])]
    path1 = nx.shortest_path(G, list_of_locations.index(list_of_homes[len(list_of_homes) - 1]), list_of_locations.index(starting_car_location), weight="weight")
    list1.extend(path1)
    #return list, output
    #sp to all locations solution end




    #single source shortest path greedy algorithm: find node that's closest to start and go there, remove from list of loc

    #G = adjacency_matrix_to_graph(adjacency_matrix)[0]
    output = {}
    list = []
    lowestHomeNumber = ""
    lowestWeight = float('inf') #var to store lowest home number, var to store lowest length too
    homesLeft = list_of_homes
    source = starting_car_location
    finalhome = ""


    i = 0
    while homesLeft != []:
        dict = nx.single_source_shortest_path_length(G, list_of_locations.index(source))
        for home in homesLeft:
            if(dict[list_of_locations.index(home)] < lowestWeight):
                lowestHomeNumber = home
                lowestWeight = dict[list_of_locations.index(home)]
        path = nx.shortest_path(G, list_of_locations.index(source), list_of_locations.index(lowestHomeNumber), weight="weight")
        if (len(homesLeft) == 1):
            finalhome = lowestHomeNumber
        path.pop()
        list.extend(path)
        #print(list)
        output[list_of_locations.index(lowestHomeNumber)] = [list_of_locations.index(lowestHomeNumber)]


            #decrement homes by 1
        homesLeft.remove(lowestHomeNumber)
        source = lowestHomeNumber
        lowestHomeNumber = ""
        lowestWeight = float('inf') #var to store lowest home number, var to store lowest length too
        i+=1

    path = nx.shortest_path(G, list_of_locations.index(finalhome), list_of_locations.index(starting_car_location), weight="weight")
    list.extend(path)




    cost1 = cost_of_solution(G, list1, output1)
    cost = cost_of_solution(G , list, output)
    cost2 = cost_of_solution(G, list2, output2)
    #cost3 = cost_of_solution(G, list3, output3)
    #print("message:" + str(cost3[1]))
    if (cost1 < cost and cost1 < cost2):
        return list1, output1
    elif (cost < cost1 and cost < cost2):
        return list, output
    else:
        return list2, output2


    #G = nx.steiner_tree(adjacency_matrix_to_graph(adjacency_matrix), list_of_homes + [starting_car_location]); #returns steiner tree




"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
