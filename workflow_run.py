import json
import time
import sys

def all_possible_paths(json_graph, node, total_time = 0, nodes_list = [], visited={}):
    '''
    Finds all paths in DAG using DFS traversal, and adds each node along with time from root.
    :param json_graph: Graph representation in JSON format
    :param node: Current node
    :param total_time: total time from root till current node along current path
    :param nodes_list: Final list containing all (time, node) tuples
    :param visited: Tracks which nodes have been visited in current path
    :return: Nothing. Output of this function is stored in nodes_list
    '''
    visited[node] = True
    nodes_list.append((total_time, node))

    for child_node in json_graph[node]['edges']:
        if child_node not in visited or not visited[child_node]:
            child_time = json_graph[node]['edges'][child_node]
            all_possible_paths(json_graph, child_node, total_time+child_time, nodes_list, visited)

    visited[node] = False
    return nodes_list

def find_start_node(json_graph):
    '''
    Obtains the start node by looking through the JSON DAG
    :param json_graph: Graph representation in JSON format
    :return: The start node which contains start=True in node dictionary
    '''
    for node in json_graph.keys():
        if 'start' in json_graph[node]:
            return node


def workflow_executer(workflow_json):
    '''
    Takes an input DAG in JSON format and prints every node after the wait time corresponding to the edge
    :param workflow_json: File containing the DAG in JSON format
    :return: None
    '''
    json_fileobj = open(workflow_json)
    json_struct = json.load(json_fileobj)

    # Get starting node based on start keyword in input JSON
    start_node = find_start_node(json_struct)

    # Obtain list of all nodes along with time from root to print, along every possible path
    nodes_list = all_possible_paths(json_struct, start_node)

    # Sort the list based on time from root
    nodes_list = sorted(nodes_list)

    print("Nodes in order of printing and 'T' seconds after which they should be printed:")
    print(nodes_list)
    # Print with wait time
    print(nodes_list[0][1])
    for i in range(1, len(nodes_list)):
        pair = nodes_list[i]
        prev_pair = nodes_list[i-1]
        time.sleep(pair[0]-prev_pair[0])
        # print(pair[1])
        print("Printing %s after %d seconds" % (pair[1], pair[0]-prev_pair[0]))


if __name__ == "__main__":
    workflow_executer(sys.argv[1])


