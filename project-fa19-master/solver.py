import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import networkx as nx
#import dimod

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""




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
    #G = nx.steiner_tree(nx.from_numpy_matrix(adjacency_matrix), list_of_homes + [starting_car_location]);
    #how to find a path to chosen node, then dropoff?
    #edges = nx.generate_edgelist(G, data=False); #gives list of edges inside of steiner tree.
    #G = nx.traveling_salesperson(nx.from_numpy_matrix(adjacency_matrix), dimod.ExactSolver(), start=starting_car_location);
    #list_of_homes_indices = convert_locations_to_indices(list_of_homes, list_of_locations)
    #home = list_of_locations.index(starting_car_location)

    '''
    #shortest paths to each location solution
    G = adjacency_matrix_to_graph(adjacency_matrix)[0]
    list = []
    path = nx.shortest_path(G, list_of_locations.index(starting_car_location), list_of_locations.index(list_of_homes[0]), weight="weight")
    list.extend(path)
    list.pop() #get rid of duplicate
    output = {}
    output[list_of_locations.index(list_of_homes[0])] = [list_of_locations.index(list_of_homes[0])]
    for i in range(len(list_of_homes) - 1):
        path = nx.shortest_path(G, list_of_locations.index(list_of_homes[i]), list_of_locations.index(list_of_homes[i+1]), weight="weight")
        list.extend(path)
        list.pop()
        output[list_of_locations.index(list_of_homes[i])] = [list_of_locations.index(list_of_homes[i])]
    output[list_of_locations.index(list_of_homes[len(list_of_homes) - 1])] = [list_of_locations.index(list_of_homes[len(list_of_homes) - 1])]
    path = nx.shortest_path(G, list_of_locations.index(list_of_homes[len(list_of_homes) - 1]), list_of_locations.index(starting_car_location), weight="weight")
    list.extend(path)
    print(list)
    return list, output
    #sp to all locations solution end
    '''

    G = nx.steiner_tree(adjacency_matrix_to_graph(adjacency_matrix), list_of_homes + [starting_car_location]); #returns steiner tree





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
