import pickle
import argparse
from itertools import chain
from pprint import pprint
from utils import Manager


def add_edge(graph, costs, source, target):
    key = (source, target)
    if source in graph:
        if target in graph[source]:
            costs[key] += 1
        else:
            graph[source].append(target)
            costs[key] = 1
    else:
        graph[source] = [target]
        costs[key] = 1
    return graph, costs


def parse_nodes(data):
    nodes = {}
    edges = []
    i = 0
    print "Processing data ..."
    for s,t in data:
        for node in (s, t):
            if node not in nodes:
                nodes[node] = i
                i += 1
        edges.append((nodes[s], nodes[t]))
    print "Done"
    del nodes
    return edges

def parse(nodes):
    edges, costs = {}, {}
    print "Processing nodes ..."
    for source, target in nodes:
        edges, costs = add_edge(edges, costs, source, target)
    print "Done."
    return edges, costs


def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    if len(path) > MAX_LEN:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None

def find_all_paths(graph, start):
    max_node = max(graph.keys())
    for i in range(max_node):
        if i in graph:
            path = find_path(graph, start, i)
            if path:
                print "Found: ", i, path 

def load_data_bin(filename):
    global GRAPH, COSTS
    print "Loading integers..."
    with open(filename) as fin:
        data = [l[:-1] for l in fin.readlines()]
        data = [l.split(' ') for l in data]
        data = [[int(n) for n in s] for s in data]
        nodes = data
        GRAPH, COSTS = parse(nodes)
     

def load_data(filename):
    print "Converting hash data..."
    with open(filename) as fin:
        data = [l[:-1] for l in fin.readlines()]
        data = [l.split(' ') for l in data]
        nodes = parse_nodes(data)
        with open(filename + '.bin', 'w') as fout:
            data = '\n'.join([' '.join([str(s) for s in l]) for l in nodes])
            fout.write(data)
    print "Data converted"
 

FILE = 'anony-100k.txt.bin'
MAX_LEN = 3
START = 2
GRAPH = None
COSTS = None

manager = Manager()

#@manager.command
#def convert():
#    pass # convert to a binary format

@manager.command
def analyse(filename=None):
    filename = filename or FILE
    if filename.endswith('.bin'):
        load_data_bin(filename)
    else:
        load_data(filename)
        return
    print "Keys:", len(GRAPH.keys())
    print "Edges:", len(COSTS.keys()) 
    print "Max node:", max(GRAPH.keys() + list(chain(*GRAPH.values())))
    values = COSTS.values()
    print "Max cost value:", max(values), "Avg cost: ", float(sum(values))/len(values)
    interactions = [len(v) for v in GRAPH.values()]
    print "Max edge:", max(interactions), "Avg edge: ", float(sum(interactions)/len(interactions))


if __name__ == '__main__':
    manager.run() 
