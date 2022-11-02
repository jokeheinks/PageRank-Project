import networkx as nx

DATA_LOCATION = "PageRankExampleData/"

RESULT_LOCATION = "Results/"

FILENAMES = ["bigRandom.txt", "medium.txt",
             "p2p-Gnutella08-mod.txt", "three.txt", "tiny.txt", "wikipedia.txt"]


def loadData(filename):
    with open(f"{DATA_LOCATION}{filename}", "rb") as file:
        G = nx.read_adjlist(file, create_using=nx.DiGraph())
    return G


def randomSurfer(graph):
    return


def pageRank(graph):
    return


def printSummary():
    pass


def printToCSV():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
