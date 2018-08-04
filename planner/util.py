import heapq
import inspect
import sys


"""
 Data structures useful for implementing Best-First Search
"""

class FrontierPriorityQueueWithFunction(object):
    '''
    FrontierPriorityQueueWithFunction class implement a search frontier using a
    PriorityQueue for ordering the nodes and a set for
    constant-time checks of states in frontier.

    OBSERVATION: it receives as input a function `f` that
    itself receives a node and returns the priority for
    the given node. Check util.PriorityQueueWithFunction for
    more details.
    '''

    def __init__(self, f):
        self._queue = PriorityQueueWithFunction(f)
        self._set = set()

    def __contains__(self, node):
        ''' Return true if `node.state` is in the frontier. '''
        return node.state in self._set

    def __len__(self):
        ''' Return the number of nodes in frontier. '''
        assert(len(self._queue) == len(self._set))
        return len(self._queue)

    def is_empty(self):
        ''' Return true if frontier is empty. '''
        return self._queue.isEmpty()

    def push(self, node):
        ''' Push `node` to frontier. '''
        self._queue.push(node)
        self._set.add(node.state)

    def pop(self):
        ''' Pop `node` from frontier. '''
        node = self._queue.pop()
        self._set.discard(node.state) # antes era remove
        return node

    def __str__(self):
        ''' Return string representation of frontier. '''
        return str(self._queue)



class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def __init__(self):
        self.heap = []
        self.count = 0

    def __contains__(self, item):
        for (_, _, i) in self.heap:
            if i == item:
                return True
        return False

    def __len__(self):
        return len(self.heap)

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                #print("priority in heap: {}, requested priority: {}".format(p, priority))
                if p <= priority: 
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

    def __str__(self):
        return str([(p, str(item)) for (p, _, item) in self.heap])


class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))

class Queue:
    # ref: https://www.pythoncentral.io/use-queue-beginners-guide/
    def __init__(self):
      self.queue = list()

    def push(self,data):
      #Checking to avoid duplicate entry (not mandatory)
      if data not in self.queue:
          self.queue.insert(0,data)
          return True
      return False

    def pop(self):
      if len(self.queue)>0:
          return self.queue.pop()
      return ("Queue Empty!")

    def isEmpty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]
    print("*** Method not implemented: `%s` at line %s of %s" % (method, line, fileName))
    sys.exit(1)