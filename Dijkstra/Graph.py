from collections import deque, namedtuple

from Errors.errors import WrongEdgesError, NodeDoestExist

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost):
    return Edge(start, end, int(cost))


class Graph:
    def __init__(self, edges):
        # Check if the input data has 3 arguments: start-end-cost
        wrong_edges = [i for i in edges if len(i) != 3]
        if wrong_edges:
            raise WrongEdgesError('Wrong edges data: {}'.format(wrong_edges))

        # treat the elements of this iterable as positional arguments to this function call.
        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def nodes(self):
        # set make each element unique, for instance: This input [1,2],[2,2],[3,2],[4,2],[5,2] will be [1,2,3,4,5]
        return set(
            # take only the nodes of each Edge, e.g: ('GRU', 'BRC', '10') will be ['GRU', 'BRC']
            # Add the result with a empty array, so make a array of arrays into a unique array
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    @property
    def neighbours(self):
        # This will create the neighbours for each node. Setting set() first, will ensure each neighbour to be unique.
        neighbours = {node: set() for node in self.nodes}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        # Check if the source and destination are present in the nodes
        if source not in self.nodes or dest not in self.nodes:
            raise NodeDoestExist('The node informed doesnt exist. Please inform a valid one')
        # The visited nodes will add each node we've already visited. Then each loop we can check if the destination
        # was already reached, which means we've already have the best route.
        visited_nodes = []
        shortest_distance_from_source = {node: inf for node in self.nodes}
        previous_nodes = {
            node: None for node in self.nodes
        }
        shortest_distance_from_source[source] = 0
        nodes = self.nodes.copy()

        while nodes:
            # The current, or visited_node, will be the one with the lowest cost
            current_node = min(nodes, key=lambda node: shortest_distance_from_source[node])
            nodes.remove(current_node)

            # If there is no path to the destination
            if shortest_distance_from_source[current_node] == inf:
                break

            # Now the cost for the neighbours will be updated according to the cost relative to the source
            # If is shorter, the shortest distance will be updated along with the previous_node
            # indicating we now have a shortest path.
            for neighbour, cost in self.neighbours[current_node]:
                alternative_route = shortest_distance_from_source[current_node] + cost
                if alternative_route < shortest_distance_from_source[neighbour]:
                    shortest_distance_from_source[neighbour] = alternative_route
                    previous_nodes[neighbour] = current_node

            # Append the current node to the visited_nodes
            visited_nodes.append(current_node)
            # If the destination is in the visited_nodes array we can stop the search
            if dest in visited_nodes:
                nodes = []

        # Now it's necessary to "reconstruct" the path from the destination to the source.
        path, current_node = deque(), dest
        while previous_nodes[current_node] is not None:
            path.appendleft(current_node)
            current_node = previous_nodes[current_node]
        if path:
            path.appendleft(current_node)
        return path, shortest_distance_from_source[dest]
