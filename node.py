class Node(object):

    ''' Search Node representation '''

    def __init__(self, state, action=None, parent=None, g=0, h=0):
        self._state  = state
        self._action = action
        self._parent = parent
        self._g  = g
        self._h  = h

    # getters
    @property
    def state(self):
        return self._state

    @property
    def action(self):
        return self._action

    @property
    def parent(self):
        return self._parent

    @property
    def g(self):
        '''
        Return the path cost from initial initial state
        to the current state referred to by the node.
        '''
        return self._g

    @property
    def h(self):
        ''' Return the heuristic value of the state referred to by the node. '''
        return self._h

    def __eq__(self, other):
        ''' Return true if two nodes refer to the same state. '''
        return str(self._state) == str(other._state)

    def __str__(self):
        ''' Return the node string as the representation of the state it refers to. '''
        return str(self._state)

    def path(self):
        '''
        Return a list of actions in the path from initial state
        to the current state referred to by the node.
        '''
        actions = []
        node = self
        while node._parent is not None:
            actions = [node._action] + actions
            node = node._parent
        return actions
