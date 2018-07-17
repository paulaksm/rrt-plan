class State(set):

    '''
    State representation as a set of ground atoms.
    It makes the CWA (Closed World Assumption).
    '''

    def __str__(self):
        return str(sorted(map(str, self)))

    def __hash__(self):
        return hash(str(self))

    def union(self, predicates):
        ''' Return a new state with ground `predicates` added to the set. '''
        return State(self | predicates)

    def intersect(self, predicates):
        ''' Return a new state with the ground `predicates` in intersection of sets. '''
        return State(self & predicates)

    def difference(self, predicates):
        ''' Return a new state with ground `predicates` in the difference of sets. '''
        return State(self - predicates)
