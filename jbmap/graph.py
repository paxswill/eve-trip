from collections.abc import Iterable

class Vertex(object):
    """Represents a graph vertex or node.

    edges in a mapping of Vertex objects to weights. In other words, keys are
    Vertex objects, values are a number.

    name is a nice name of this vertex.
    """
    def __init__(self, name=None, links=None)
        """Initialize a Vertex.

        name is the human readable name of the vertex.

        links is an iterable if Vertex objects. If links is a dict,
        keys are Vertex objects and values are numbers. If links is not a
        mapping type, weights are initialized to 0.0.
        """
        self.name = name
        if links:
            assert isinstance(links, Iterable), "links must be iterable"
            if isinstance(links, dict):
                self.edges = links
            else:
                self.edges = map()
                for vertex in links:
                    links[vertex] = 0.0
        else:
            self.edges = map()


class Graph(object):
    """Represents a graph.

    vertices is a set of Vertex objects.
    """
    def __init__(self, vertices=None):
        pass
