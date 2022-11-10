import random
import networkx as nx

DATA_LOCATION = "PageRankExampleData"

RESULT_LOCATION = "Results"

FILENAMES = ["bigRandom.txt", "medium.txt",
             "p2p-Gnutella08-mod.txt", "three.txt", "tiny.txt", "wikipedia.txt"]

# Parameters
TOLERANCE = 1.0e-6
MAX_DEPTH = 100
M = 0.15
RANDOMSURFER_ITERATIONS = 100


def loadData(filename: str) -> nx.DiGraph:
    """Loads the data from {DATA_LOCATION}/{Filename} into a nx.DiGraph
    """
    with open(f"{DATA_LOCATION}/{filename}", "rb") as file:
        G = nx.read_adjlist(file, create_using=nx.DiGraph())
    return G


def isDangling(graph: nx.DiGraph, node: str) -> bool:
    """Checks if the node is dangling (Has no successors)
    Returns:
        bool: True if the node is dangling, else False
    """
    return len(list(graph.successors(node))) == 0


def randomNode(graph: nx.DiGraph) -> str:
    """Returns a random node from the graph
    """
    return random.choice(list(graph.nodes()))


def addCount(graph: nx.DiGraph, node: str) -> None:
    """Adds 1 to the 'weight' attribute of the Node (In place)
    """
    graph.nodes[node]["weight"] += 1


def initCountAttr(graph: nx.DiGraph) -> None:
    """Creates the attribute 'weight' with value 0 for all nodes (In place)
    """
    for node in graph.nodes():
        graph.nodes[node]["weight"] = 0


def randomSurfer(graph: nx.DiGraph(), iterations: int, m: float) -> tuple[nx.DiGraph, int]:
    """Implements a random surfer, that goes through the graph
        and adds 1 to 'weight' for every node it visits

    Args:
        graph (nx.DiGraph): A directed graph
        iterations (int): The number of steps the randomSurfer takes per node
        m (float): The chance, that the randomSurfer goes to a random node instead of a successor

    Returns:
        tuple[nx.DiGraph, int]:
            A graph with the counts of the random surfer in the 'weight' attribute
            Number of steps overall
    """
    initCountAttr(graph)

    node = randomNode(graph)
    for _ in range(iterations * numberOfNodes(graph)):
        if random.random() > m:
            if isDangling(graph, node):
                node = randomNode(graph)
            else:
                node = random.choice(list(graph.successors(node)))
        else:
            node = randomNode(graph)
        addCount(graph, node)
    return graph, iterations * numberOfNodes(graph)


def numberOfNodes(graph: nx.DiGraph) -> int:
    """Returns the number of Nodes in the graph
    """
    return len(list(graph.nodes()))


def initialiseWeights(graph: nx.DiGraph, n: int) -> None:
    """Creates the 'weight' attribute with value (1/n) for every node (In place)
    """
    n = 1/n
    for node in graph.nodes():
        graph.nodes[node]["weight"] = n


def initialiseNSuccessors(graph: nx.DiGraph) -> None:
    """Creates the 'Successors' attribute with the number of successors for every node (In place)
    '"""
    for node in graph.nodes():
        graph.nodes[node]["successors"] = len(list(graph.successors(node)))


def getDanglingNodes(graph: nx.DiGraph) -> list:
    """Returns a list of the dangling nodes in the graph
    """
    dangling = []
    for node in graph.nodes():
        if isDangling(graph, node):
            dangling.append(node)
    return dangling


def sumWeights(graph: nx.DiGraph, nodes: int) -> float:
    """Returns the sum of the value in the 'weight' attribute for the nodes
    """
    return sum([graph.nodes()[node]["weight"] for node in nodes])


def getA(graph: nx.DiGraph, reverseGraph: nx.DiGraph, node: str) -> float:
    """Calculates the parameter A
        A = The sum of (1/number of successors * weight) for each predecessor
    """
    A = 0
    for predecessor in reverseGraph.successors(node):
        A += (1 / graph.nodes[predecessor]["successors"]) * \
            graph.nodes[predecessor]["weight"]
    return A


def avgChange(lastNodes: list, newNodes: list, n: int) -> float:
    """Calculates the average difference from the new nodes to the old nodes"""
    return sum([abs(lastNode - newNodes) for lastNode, newNodes in zip(lastNodes, newNodes)]) / n


def pageRank(graph: nx.DiGraph, maxDepth: int, m: float) -> tuple[nx.DiGraph, int]:
    """The implementation of the page rank algorithm.
    Iterates over every node, and sets the weight value to: (1-m)(A+D) + mS
    m: The probability that a random node is used
    A: The weight of the previos node, spread over all the nodes it links to
    D: The weight of the dangling nodes, spread over all nodes
    S: With probabiliy m, the weight will go to a random node

    Args:
        graph (nx.DiGraph): The graph, where the nodes are pages to rank
        maxDepth (int): The maximum iterations of the algorithm
        m (float): The dampening factor

    Returns:
        tuple[nx.DiGraph, int]:
            The graph, where every node has the 'weight' corresponding to the importance score
            The number of iterations pageRank ran for
    """
    n = numberOfNodes(graph)

    initialiseWeights(graph, n)
    initialiseNSuccessors(graph)

    reverseView = nx.reverse_view(graph)

    danglingNodes = getDanglingNodes(graph)
    S = m * (1/n)

    for i in range(1, maxDepth+1):
        lastNodes = [graph.nodes()[node]["weight"] for node in graph.nodes()]

        D = (1-m) * (1/n) * (sumWeights(graph, danglingNodes))

        for node in graph.nodes():
            A = getA(graph, reverseView, node)
            graph.nodes()[node]["weight"] = ((1-m) * A) + D + S

        newNodes = [graph.nodes()[node]["weight"] for node in graph.nodes()]
        change = avgChange(lastNodes, newNodes, n)
        if change < TOLERANCE:
            return graph, i

    return graph, maxDepth


def topNodes(graph: nx.DiGraph) -> list:
    """Returns a list with the nodes that have the 10 highest values in the 'weight' attribute.
    """
    weights = nx.get_node_attributes(graph, "weight")
    sortedNodes = sorted(weights, key=lambda x: weights[x], reverse=True)
    return sortedNodes[:10]


def bold(String: str) -> str:
    """Returns the string to be printed bold
    """
    return f"\033[1m{String}\033[0m"


def printSummary(filename: str, pageRankGraph: nx.DiGraph, pageRankIterations: int, randomSurferGraph: nx.DiGraph, randomSurferIterations: int) -> None:
    """Prints a summary of the results from both pageRank and randomSurfer
        with the iteration and top nodes

    Args:
        filename (str): The name of the file containing the data
        pageRankGraph (nx.DiGraph): The graph pageRank returned, containing the weighted nodes
        pageRankIterations (int): The iterations, pageRank ran for
        randomSurferGraph (nx.DiGraph): Graph randomSurfer returned, containing the weighted nodes
        randomSurferIterations (int): The iterations, randomSurfer ran for
    """
    print(bold(f"The result for {filename[:-4]}"))

    print(
        f"\nThe top nodes with the randomSurfer algorithm, with {randomSurferIterations} iterations are:")
    for i, node in enumerate(topNodes(randomSurferGraph)):
        print(
            f"{(i+1):2}. Node {node:<4}: {randomSurferGraph.nodes()[node]['weight']} ({randomSurferGraph.nodes()[node]['weight']/randomSurferIterations})")

    print(
        f"\nThe top nodes with pageRank that stabilised after {pageRankIterations} iterations are:")
    for i, node in enumerate(topNodes(pageRankGraph)):
        print(
            f"{(i+1):2}. Node {node:<4}: {pageRankGraph.nodes()[node]['weight']}")
    print()


def printToCSV(filename: str, graph: nx.DiGraph, algorithm: str) -> None:
    """Prints the result to the file {RESULT_LOCATION}/{algorithm}_{filename[:-4]}.csv
    """
    weights = nx.get_node_attributes(graph, "weight")
    sortedNodes = sorted(weights, key=lambda x: weights[x], reverse=True)

    with open(f"{RESULT_LOCATION}/{algorithm}_{filename[:-4]}.csv", "w", encoding="utf-8") as file:
        file.write("Node, Score\n")
        for node in sortedNodes:
            file.write(f"{node}, {graph.nodes()[node]['weight']}\n")


def main():
    for file in FILENAMES[1:]:
        graph = loadData(file)

        graph_pageRank, PagerankIterations = pageRank(
            graph.copy(), MAX_DEPTH, M)

        graph_randomSurfer, RandomsurferIterations = randomSurfer(
            graph, RANDOMSURFER_ITERATIONS, M)

        printSummary(file, graph_pageRank, PagerankIterations,
                     graph_randomSurfer, RandomsurferIterations)

        printToCSV(file, graph_pageRank, "PageRank")
        printToCSV(file, graph_randomSurfer, "RandomSurfer")


if __name__ == "__main__":
    main()
