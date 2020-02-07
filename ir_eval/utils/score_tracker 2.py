from heapq import *
import random
from collections import defaultdict

REMOVED = -1


class ScoreTracker:
    """
    This is a class for keeping track of top N scores in main memory.
    Use add_score() function to add a score to a document
    Use get_top() function to retrieve the best document and score values (with limit and skip capabilities)

    # Example usage:
    tracker = ScoreTracker()
    for term in ["I", "am", "your", "father"]:  # replace with query terms
        for doc_id in range(75000000):  # replace with docs that contain the term
            tracker.add_score(doc_id, random.gauss(0.5, 0.25))  # instead of random, compute score
            # if doc_id % 500000 == 0:
            #     print("{} - {}".format(term, doc_id))
            #     print("Size: {}\nKeeping removed: {}\nMin score: {}".format(len(tracker.heap), tracker.removed_count,
                                                                            tracker.heap[0][0]))
    top_scores = tracker.get_top(50, 0)
    """

    def __init__(self, max_size=100000):
        # This will be a list of [score, doc_id] entries, where heap[0] entry always has the minimum score:
        self.heap = []
        # For more info: https://docs.python.org/2/library/heapq.html
        self.entry_finder = {}  # doc_id -> [score, id_or_REMOVED]
        self.removed_count = 0  # keep track of how many removed entries we are still keeping in memory
        self.max_size = max_size

    def add_score(self, id, score):
        if id in self.entry_finder:
            score += self.entry_finder[id][0]
        if len(self.heap) >= self.max_size and score <= self.heap[0][0]:
            # the score is not even better than the worst entry in the full heap. So this score can be safely discarded
            return

        # Congratulations, the entry is a suitable candidate for Top `max_size`.
        self.__remove_entry_if_exists(id)
        entry = [score, id]
        self.entry_finder[id] = entry
        heappush(self.heap, entry)
        self.__cleanup()

    def get_top(self, n: int, skip=0):
        # get top N results (skipping the first `skip` results)
        # return a list of (id, score) tuples, sorted from highest to lowest by score (e.g. [(19, 1.5), (6, 1.46), ...]
        top_results = sorted(filter(lambda x: x[1] is not REMOVED, self.heap), reverse=True)
        return list(map(lambda x: (x[1], x[0]), top_results[skip:skip+n]))

    def __remove_entry_if_exists(self, id):
        if id in self.entry_finder:
            # mark the entry as removed
            entry = self.entry_finder.pop(id)
            entry[1] = REMOVED  # set doc_id to removed, so we know the score is no longer valid.
            self.removed_count += 1

    def __cleanup(self):
        # attempt to tidy up removed entries, and reduce size to max_size
        while True:
            if len(self.heap) == 0:
                break
            if self.heap[0][1] is REMOVED:
                heappop(self.heap)
                self.removed_count -= 1
                continue
            if len(self.heap) > self.max_size:  # here we know that id is not removed, but we have exceeded the size limit
                score, id = heappop(self.heap)
                del self.entry_finder[id]
                continue
            break  # nothing was removed, so the cleanup has finished. Exit the loop



"""
Alternative way of adding scores - DO NOT USE (storing everything in main memory takes ~7GB of RAM):
scores = defaultdict(float)
for term in ["I", "am", "your", "father"]:
    for doc_id in range(75000000):
        scores[doc_id] += random.gauss(0.5, 0.25)
        if doc_id % 50000 == 0:
            print("{} - {}".format(term, doc_id))

"""