
class Queue():
    # copied from util.py
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def bft(linkages, starting_node):
    # ancestors is guaranteed acyclic, so no need for visited
    q = Queue()
    q.enqueue(starting_node)
    final_path = []
    while q.size() > 0:
        node = q.dequeue()
        final_path.append(node)
        for next_vert in linkages[node]:
            q.enqueue(next_vert)
    return final_path

def earliest_ancestor(ancestors, starting_node):
    # create the linkages child -> parent
    # ancestors are recorded as (parent, child)
    linkages = {}
    for pair in ancestors:
        if pair[0] not in linkages:
            linkages[pair[0]] = set()
        if pair[1] not in linkages:
            linkages[pair[1]] = set()
        linkages[pair[1]].add(pair[0])   

    # return -1 if the starting node has no parents
    if linkages[starting_node] == set():
        return -1

    # the last element in a BFT should be an oldest ancestor
    return bft(linkages, starting_node)[-1]



if __name__ == "__main__":
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                      (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    print(earliest_ancestor(test_ancestors, 3))