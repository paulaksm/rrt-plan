class Literal(object):

    def __init__(self, predicate, positive):
        self._predicate = predicate
        self._positive  = positive

    @property
    def predicate(self):
        return self._predicate

    def is_positive(self):
        return self._positive

    def is_negative(self):
        return not self._positive

    def ground(self, subst):
        ground_predicate = self._predicate.ground(subst)
        if self.is_positive():
            return Literal.positive(ground_predicate)
        if self.is_negative():
            return Literal.negative(ground_predicate)

    @classmethod
    def positive(cls, predicate):
        return Literal(predicate, True)

    @classmethod
    def negative(cls, predicate):
        return Literal(predicate, False)

    def __str__(self):
        if self.is_positive():
            return str(self._predicate)
        if self.is_negative() and self._predicate.name == '=':
            lhs = str(self._predicate.args[0])
            rhs = str(self._predicate.args[1])
            return '{0} != {1}'.format(lhs, rhs)
        if self.is_negative():
            return 'not {}'.format(str(self._predicate))
