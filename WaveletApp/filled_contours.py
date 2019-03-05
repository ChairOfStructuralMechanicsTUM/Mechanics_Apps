# converts a filled isocontours to a set of polygons for plotting in bokeh

import numpy as np
import networkx as nx

from scipy.spatial import Delaunay

def triangulated_graph(polygons):
	tri = Delaunay(np.vstack(polygons))

	#create ring identifiers and indices into ring vertices
	ring_index = []
	local_dex = []
	for i,poly in enumerate(polygons):
		ring_index.append(i+np.zeros(len(poly), dtype=np.int))
		local_dex.append(np.arange(len(poly)))
	ring_index = np.hstack(ring_index)
	local_dex = np.hstack(local_dex)

	edges = set()
	for simplex in tri.simplices:
		edges.add(tuple(sorted([simplex[0], simplex[1]])))
		edges.add(tuple(sorted([simplex[0], simplex[2]])))
		edges.add(tuple(sorted([simplex[1], simplex[2]])))

	#put undirected edges in graph
	triangle_graph = nx.Graph()
	for e0,e1 in edges:
		triangle_graph.add_edge(e0, e1, weight=np.linalg.norm(tri.points[e0]-tri.points[e1]))

	# put node data in graph
	for i,p in enumerate(tri.points):
		triangle_graph.add_node(i,ring=ring_index[i], local = local_dex[i])

	return triangle_graph


""" Create a graph of ring islands. some islands will have two bridges joining them """
def create_islands(graph):
	#create minimum spanning tree from undirected edges
	mst_edges = sorted(list(nx.minimum_spanning_edges(graph,data=True)))
	islands = nx.Graph()
	for e0, e1, w in mst_edges:
		ring0 = graph.node[e0]['ring']
		ring1 = graph.node[e1]['ring']
		local0, local1 = graph.node[e0]['local'], graph.node[e1]['local']
		if  ring0 != ring1:
			islands.add_edge(ring0, ring1, weight = w, 
							connection = [e0, e1, local0, local1], 
							)
	return islands

""" Inserts degenerate edge, replacing nodes with new ones
 0 -> 1a 1b -> 2      0 -> 1a -> 3b -> 4 -> 5 -> 3a -> 1b -> 2
      |   |
 4 <- 3b 3a <- 5 <- 4
"""
def insert_branch(graph, edge):
	for e in edge:
		prev, next = list(graph.predecessors(e)), list(graph.successors(e))

		if len(prev) > 0: 
			graph.add_edge(prev[0],e-.1)
			graph.node[e-.1].update(graph.node[e])

		if len(next) > 0:
			graph.add_edge(e+.1,next[0])
			graph.node[e+.1].update(graph.node[e])

		graph.remove_node(e)

	# link new nodes. Order won't matter when doing shortest path query
	graph.add_edge(edge[0]+.1, edge[1]-.1)
	graph.add_edge(edge[0]-.1, edge[1]+.1)
	return graph
	
# create a directed graph from polygons
def polygon_graph(polygons):
	g = nx.DiGraph()
	shift = 0
	for i,poly in enumerate(polygons):	
		g.add_cycle(range(shift,shift+len(poly)))
		shift += len(poly)
	return g

"""Get the shortest path that traverses the edges """
def get_merged_path(poly_graph):
	#select an edge, remove it and find path that circles back
	edge = poly_graph.edges[0]; e1, e0 = edge
	ug = poly_graph.to_undirected()
	ug.remove_edge(e0,e1)
	# round to get the index of the original vertices
	return [int(round(x)) for x in nx.shortest_path(ug,e0)[e1]]

"""Connect each island through one bridge"""
def merge_islands(islands, polygons):
	poly_graph = polygon_graph(polygons)

	mst_islands = nx.minimum_spanning_tree(islands, 0)
	for r_0, r_1 in mst_islands.edges():
		e0, e1, _, _ = mst_islands[r_0][r_1]['connection']
		poly_graph = insert_branch(poly_graph,(e0,e1))
	
	return poly_graph

def rgb_to_hex(color_rgb):
    return '#%02x%02x%02x' % color_rgb

def filled_contours(p, cn, simplify_threshold=0.01):
	"""Creates a bokeh plot of filled contours
    Args:
    	p (bokeh.plotting.Figure): Bokeh plot instance
        cn (contours): Contours generated from plt.contourf()
        simplify_threshold (Optional[float]): Resolution of the output contours in screenspace. Defaults to .01
    Returns:
        None
    """
	for cc in cn.collections:
		face_color = np.array(cc.get_facecolor()[0])
		color = rgb_to_hex(tuple((255*face_color[:-1]).round().astype(int)))
		alpha = face_color[-1]
	
		for path in cc.get_paths():
			path.simplify_threshold = simplify_threshold
			polygons = path.to_polygons()
			if len(polygons) == 1:
				p.patch(polygons[0][:,0], polygons[0][:,1], line_alpha=alpha, line_color=color, fill_alpha=alpha, fill_color=color)
			else:
				vertices = np.vstack(polygons)
				graph = triangulated_graph(polygons)
				islands = create_islands(graph)
				poly_graph = merge_islands(islands,polygons)
				merged_path = get_merged_path(poly_graph)

				p.patch(vertices[merged_path][:,0],vertices[merged_path][:,1], line_alpha = alpha, line_color = color, fill_alpha = alpha, fill_color = color)
