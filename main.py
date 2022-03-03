# from graph import *
from graph_io import *
import color_refine
import time


# First give each vertex a color
# Then grab all vertices with the same color
# Check those vertices on their neighbours
# One dict contains all vertices with the same color
# The keys of that dict are the neighbourhood colors
# Skip the first key so that one color remains

# Data structure Dict with keys of colors, the values are dicts with keys of neighbours and those values are the
# vertices with that neighbourhood So, Colors{blue: Neighbourhoods{(2,2): Vertex A, Vertex B, Vertex C },
# green: Neighbourhoods{(3,2,1): Vertex D, Vertex E, (1): Vertex F }}


def updateColors(g: Graph, h: Graph):
    colors = {}
    firstnbc = []
    for v in g.vertices + h.vertices:
        # If the color already exists in the dictionary
        if v.colornum in colors:
            # Create the neighbourhoods based on color
            nbc = tuple(sorted([c.colornum for c in v.neighbours]))
            # If the nbc already exists in the dictionary
            if nbc in colors[v.colornum]:
                # Add the vector to that element
                colors[v.colornum][nbc].append(v)
            else:
                # Create an element with key nbc
                colors[v.colornum][nbc] = [v]
        else:
            # Create an element in the dictionary with the key nbc and initialize it with the first vector
            nbc = tuple(sorted([c.colornum for c in v.neighbours]))
            colors[v.colornum] = {nbc: [v]}
            # Keep track of the first entries of the dictionary
            firstnbc.append(nbc)
            firstnbc.append(v.colornum)
    return colors, firstnbc


def color_ref(g: Graph, h: Graph, single: bool = True) -> tuple[Graph, Graph]:
    # Give each vertex a color for initialization
    if single:
        for v in g.vertices + h.vertices:
            v.colornum = v.degree

    changed = True
    while changed:
        colors, firstnbc = updateColors(g, h)
        highest = max(colors) + 1
        changed = False
        for i in list(colors.keys()):
            # Cut off the first nbc because those do not need to be changed
            # Loop through the rest of the neighbourhoods
            if len(list(colors[i].keys())) > 1:
                changed = True
            for j in list(colors[i].keys())[1:]:
                # If the neighbourhood exists already on the first place in another color
                if j in firstnbc:
                    # Change each vertex' color to that colour and add that vertex to that element
                    for v in colors[i][j]:
                        v.colornum = firstnbc[firstnbc.index(j) + 1]
                        colors[v.colornum][j].append(v)
                # Loop through the vertices
                else:
                    for v in colors[i][j]:
                        # Assign a new color to the vertex
                        v.colornum = highest
                        # If the color already exists in the dictionary
                        if v.colornum in colors:
                            # Add the vertex
                            colors[v.colornum][j].append(v)
                        else:
                            # If not, initialize it
                            colors[v.colornum] = {j: [v]}
                            firstnbc.append(j)
                            firstnbc.append(v.colornum)
                # Up the highest color number by one and delete the key from the original place
                highest = max(colors) + 1
                del colors[i][j]

    return g, h


# Compare whether two dictionaries are equal
def checkDicts(gdict, hdict) -> bool:
    for i in gdict:
        if i not in hdict or not len(gdict[i]) == len(hdict[i]):
            return False
    for i in hdict:
        if i not in gdict or not len(gdict[i]) == len(hdict[i]):
            return False
    return True


def checkBijection(g: Graph, h: Graph) -> 1:
    """
        Check for balance and bijection definition between two graphs.
        :param g: graph g
        :param h: graph h
        :return: 0 if unbalanced, 1 if bijection, 2 if only balanced
    """
    if checkDicts(g.getDict(), h.getDict()):
        if len(g.getDict()) == len(g.vertices):
            return 1
        else:
            return 2
    else:
        return 0


def countIsomorphism(list1, list2, graph1: Graph, graph2: Graph) -> int:
    num = 0

    # Set color of all vertices to 0
    for v in graph1.vertices + graph2.vertices:
        v.colornum = 0

    start = 1

    # Assign colors to all vertices in d and i
    for i, j in zip(list1, list2):
        i.colornum, j.colornum = start, start
        start += 1

    # If coloring is unbalanced or defines a bijection, no need to count
    graph1, graph2 = color_refine.refine_colors(graph1, graph2)
    result = checkBijection(graph1, graph2)

    if result == 0 or result == 1:
        return result

    graph1dict = graph1.getDict()
    graph2dict = graph2.getDict()

    colors = []
    [colors.append((i,len(graph1dict[i]) + len(graph2dict[i]))) for i in graph1dict if len(graph1dict[i]) + len(graph2dict[i]) >= 4]
    color = sorted(colors, key=lambda tup: tup[1])[0][0]

    for j in graph2dict[color]:
        num += countIsomorphism(list1 + [graph1dict[color][0]], list2 + [j], graph1, graph2)

    return num


if __name__ == '__main__':
    with open('Graphs1/colorref_largeexample_4_1026.grl') as f:
        L = load_graph(f, read_list=True)

    # print(L[0][3].isCyclicConnected())
    startTree = time.time()
    print(f'{L[0][1].isTree()} in {time.time() - startTree}')
    treeTime = time.time() - startTree

    startCycle = time.time()
    print(f'{not L[0][1].isCyclic()} in {time.time() - startCycle}')
    cycleTime = time.time() - startCycle

    # for i in L[0]:
    #     for j in L[0]:
    #         if L[0].index(i) < L[0].index(j):
    #             i, j = color_ref(i, j, True)
    #             if not checkBijection(i, j) == 0:
    #                 print(f'Graph {L[0].index(i)} and {L[0].index(j)} are ismorphic with {countIsomorphism([], [], i, j)} automorphisms')

    # with open('colorful0.dot', 'w') as f:
    #    write_dot(k1, f)

    # print(countIsomorphism([], [], k1, m1))


