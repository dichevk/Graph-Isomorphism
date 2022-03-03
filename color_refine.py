from graph import *
from graph_io import *


def get_slice_indices(sorted_vertices):
    slice_indices = [0]
    for i in range(1, len(sorted_vertices)):
        if sorted_vertices[i].colornum != sorted_vertices[i - 1].colornum:
            slice_indices.append(i)
    slice_indices.append(len(sorted_vertices))

    return slice_indices


def refine_colors_step(graph1: Graph, graph2: Graph) -> (Graph, Graph):
    copyvertices = []

    for vertex in graph1.vertices + graph2.vertices:
        copyvertices.append(vertex)

    sorted_vertices = sorted(copyvertices, key=lambda v: v.colornum)

    slice_indices = get_slice_indices(sorted_vertices)

    next_color = 0
    for i in range(len(slice_indices) - 1):

        group = sorted_vertices[slice_indices[i]:slice_indices[i + 1]]

        neighbours_new = {}

        for vertex in group:
            nbc = tuple(sorted([c.colornum for c in vertex.neighbours]))
            if nbc not in neighbours_new:
                neighbours_new[nbc] = next_color
                next_color += 1
            vertex.next_color = neighbours_new[nbc]

    for vertex in sorted_vertices:
        vertex.colornum = vertex.next_color

    return len(slice_indices) != len(get_slice_indices(sorted_vertices))


def refine_colors(graph1: Graph, graph2: Graph):
    # for v in graph1.vertices + graph2.vertices:
    #     v.colornum = v.degree

    while refine_colors_step(graph1, graph2):
        pass

    return graph1, graph2


if __name__ == "__main__":
    with open('Graphs2/trees11.grl') as f:
        L = load_graph(f, read_list=True)

    g, h = refine_colors(L[0][0], L[0][3])

    with open('colorful0.dot', 'w') as f:
        write_dot(g, f)
