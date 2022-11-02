import networkx as nx
import random

DATA_LOCATION = "PageRankExampleData/"

RESULT_LOCATION = "Results/"

FILENAMES = ["bigRandom.txt", "medium.txt",
             "p2p-Gnutella08-mod.txt", "three.txt", "tiny.txt", "wikipedia.txt"]


def loadData(filename):
    with open(f"{DATA_LOCATION}{filename}", "rb") as file:
        G = nx.read_adjlist(file, create_using=nx.DiGraph())
    return G


def isDangling(graph, node):
    return len(list(graph.successors(node))) == 0


def randomNode(graph):
    return random.choice(list(graph.nodes()))


def addCount(graph, node):
    graph.nodes[node]["count"] += 1


def initCountAttr(graph):
    for node in graph.nodes():
        graph.nodes[node]["count"] = 0

    return graph


def randomSurfer(graph: nx.DiGraph(), n, m):
    graph = initCountAttr(graph)

    node = randomNode(graph)

    for _ in range(n):
        if random.random() > m:
            if isDangling(graph, node):
                node = randomNode(graph)
            else:
                node = random.choice(list(graph.successors(node)))
        else:
            node = randomNode(graph)
        addCount(graph, node)
    return graph


def pageRank(graph):
    return


def printSummary():
    pass


def printToCSV():
    pass


def main():
    graph = loadData(FILENAMES[4])
    for node in graph.nodes():
        print(len(list(graph.successors(node))))

    graph = randomSurfer(graph, 10000, 0.15)

    attrs = nx.get_node_attributes(graph, "count")
    print(attrs)

    print(nx.pagerank(graph))


if __name__ == "__main__":
    main()
