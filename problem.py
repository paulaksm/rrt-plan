import itertools


class Problem(object):

    ''' STRIPS problem representation. '''

    def __init__(self, name, domain, objects, init, goal):
        self._name = name
        self._domain = domain
        self._objects = {}
        for obj in objects:
            self._objects[obj.type] = self._objects.get(obj.type, [])
            self._objects[obj.type].append(str(obj.value))
        self._init = set(map(str, init))
        self._goal = set(map(str, goal))

    # getters
    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        return self._domain

    @property
    def objects(self):
        return self._objects.copy()

    @property
    def init(self):
        ''' Return fluents which are true in initial state. '''
        return self._init.copy()

    @property
    def goal(self):
        ''' Return fluents which are true in a goal state. '''
        return self._goal.copy()

    def ground_all_actions(self, domain):
        '''
        Return all actions grounded from all operators in `domain`
        with respect to objects defined in the problem.
        '''
        actions = []
        for operator in domain.operators:
            params = operator.params
            variables = [ param.name for param in params ]
            objects   = [ self._objects[param.type] for param in params ]
            for prod in itertools.product(*objects):
                subst = dict(zip(variables, prod))
                valid = True
                for pre in operator.precond:
                    if pre.is_negative():
                        predicate = pre.predicate
                        assert(predicate.name == '=')
                        lhs = subst[predicate.args[0]]
                        rhs = subst[predicate.args[1]]
                        if lhs == rhs:
                            valid = False
                            break
                if valid:
                    actions.append(operator.instantiate(subst))
        return actions

    def __str__(self):
        problem_str  = '@ Problem: {0}\n'.format(self._name)
        problem_str += '>> domain: {0}\n'.format(self._domain)
        problem_str += '>> objects:\n'
        for type, objects in self._objects.items():
            problem_str += '{0} -> {1}\n'.format(type, ', '.join(sorted(objects)))
        problem_str += '>> init:\n{0}\n'.format(', '.join(sorted(self._init)))
        problem_str += '>> goal:\n{0}\n'.format(', '.join(sorted(self._goal)))
        return problem_str
