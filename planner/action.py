class Operator(object):

    ''' STRIPS operator class '''

    def __init__(self, name, params, precond, effects):
        self._name    = name
        self._params  = params
        self._precond = precond
        self._effects = effects

    # getters
    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params[:]

    @property
    def precond(self):
        return self._precond[:]

    @property
    def effects(self):
        return self._effects[:]

    def instantiate(self, subst):
        ''' Given a mapping from variable to constants `subst`return a ground action. '''
        args = [ str(subst.get(param.name, param)) for param in self._params ]
        precond = { str(l.predicate.ground(subst)) for l in self._precond if l.is_positive() }
        pos_effect = set()
        neg_effect = set()
        for eff in self._effects:
            ground_predicate = eff.predicate.ground(subst)
            if eff.is_positive():
                pos_effect.add(str(ground_predicate))
            elif eff.is_negative():
                neg_effect.add(str(ground_predicate))
        return Action(self._name, args, precond, pos_effect, neg_effect)

    def __str__(self):
        operator_str  = '{0}({1})\n'.format(self._name, ', '.join(map(str, self._params)))
        operator_str += '>> precond: {0}\n'.format(', '.join(map(str, self._precond)))
        operator_str += '>> effects: {0}\n'.format(', '.join(map(str, self._effects)))
        return operator_str


class Action(object):

    '''
    Ground action with preconditions and
    positive and negative effects separated.
    All atoms are represented as plain strings.
    '''

    def __init__(self, name, args, precond, pos_effect, neg_effect):
        self._name = name
        self._args = args
        self._precond = precond
        self._pos_effect = pos_effect
        self._neg_effect = neg_effect

    # getters
    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args[:]

    @property
    def precond(self):
        ''' Return a list of precondition atoms represented as strings. '''
        return self._precond.copy()

    @property
    def pos_effect(self):
        ''' Return a list of positive effect atoms represented as strings. '''
        return self._pos_effect.copy()

    @property
    def neg_effect(self):
        ''' Return a list of negative effect atoms represented as strings. '''
        return self._neg_effect.copy()

    def __str__(self):
        action_str  = '{0}({1})\n'.format(self._name, ', '.join(self._args))
        action_str += '>> pre:  {0}\n'.format(', '.join(sorted(self._precond)))
        action_str += '>> eff+: {0}\n'.format(', '.join(sorted(self._pos_effect)))
        action_str += '>> eff-: {0}\n'.format(', '.join(sorted(self._neg_effect)))
        return action_str

    def __repr__(self):
        return '{0}({1})'.format(self._name, ', '.join(self._args))
