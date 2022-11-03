import networkx as nx
import random

DATA_LOCATION = "PageRankExampleData/"

RESULT_LOCATION = "Results"

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
    graph.nodes[node]["weight"] += 1


def initCountAttr(graph):
    for node in graph.nodes():
        graph.nodes[node]["weight"] = 0

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


def numberOfNodes(graph):
    return len(list(graph.nodes()))


def initialiseWeights(graph, n):
    n = 1/n
    for node in graph.nodes():
        graph.nodes[node]["weight"] = n

    return graph


def initialiseNSuccessors(graph):
    for node in graph.nodes():
        graph.nodes[node]["successors"] = len(list(graph.successors(node)))

    return graph


def getDanglingNodes(graph):
    dangling = []
    for node in graph.nodes():
        if len(list(graph.successors(node))) == 0:
            dangling.append(node)
    return dangling


def sumWeights(nodes, graph):
    return sum([graph.nodes()[node]["weight"] for node in nodes])


def getA(node, graph, reverseGraph):
    A = 0
    for predecessor in reverseGraph.successors(node):
        A += (1 / graph.nodes[predecessor]["successors"]) * \
            graph.nodes[predecessor]["weight"]
    return A


def pageRank(graph, depth, m):
    n = numberOfNodes(graph)

    graph = initialiseWeights(graph, n)
    graph = initialiseNSuccessors(graph)

    reverseView = nx.reverse_view(graph)

    danglingNodes = getDanglingNodes(graph)
    S = m * (1/n)

    top10 = []

    for i in range(1, depth+1):
        D = (1-m) * (1/n) * (sumWeights(danglingNodes, graph))

        for node in graph.nodes():
            A = getA(node, graph, reverseView)
            graph.nodes()[node]["weight"] = ((1-m) * A) + D + S

        if top10 == topNodes(graph):
            return graph, i
        else:
            top10 = topNodes(graph)

    return graph


def topNodes(graph):
    weights = nx.get_node_attributes(graph, "weight")
    sortedNodes = sorted(weights, key=lambda x: weights[x], reverse=True)
    return sortedNodes[:10]


def printSummary(filename, pageRankGraph, iterations, randomSurferGraph):
    print(f"The result for {filename}\n")

    print(f"The top nodes with the randomSurfer algorithm are:")
    for i, node in enumerate(topNodes(randomSurferGraph)):
        print(
            f"{i+1} Node {node}: {randomSurferGraph.nodes()[node]['weight']}")

    print(
        f"The top nodes with pageRank that stabilised after {iterations} iterations are:")
    for i, node in enumerate(topNodes(pageRankGraph)):
        print(f"{i+1}. Node {node}: {pageRankGraph.nodes()[node]['weight']}")
    print()


def printToCSV(filename, graph, algrithm):
    weights = nx.get_node_attributes(graph, "weight")
    sortedNodes = sorted(weights, key=lambda x: weights[x], reverse=True)

    with open(f"{RESULT_LOCATION}/{algrithm}_{filename}.csv", "w") as file:
        file.write("Node, Score\n")
        for node in sortedNodes:
            file.write(f"{node}, {graph.nodes()[node]['weight']}\n")


def main():
    for file in FILENAMES:
        graph = loadData(file)

        graph_pageRank, iterations = pageRank(graph, 10, 0.15)
        graph_pageRank = graph_pageRank.copy()

        graph_randomSurfer = randomSurfer(graph, 10000, 0.15)

        printSummary(file, graph_pageRank, iterations, graph_randomSurfer)

        printToCSV(file, graph_pageRank, "PageRank")
        printToCSV(file, graph_randomSurfer, "RandomSurfer")


if __name__ == "__main__":
    main()
