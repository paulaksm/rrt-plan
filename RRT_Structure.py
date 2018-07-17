class RandomTree(object):

    def __init__(self, node, parent_node=None, cost=None, edge=[]):
        if parent_node is not None:
            assert isinstance(parent_node, RandomTree)
        self.node = node
        self.parent_node = parent_node
        self._cost = cost
        self.edge = edge

    @property
    def cost(self):
        return self._cost
      
    @cost.setter  
    def cost(self, dict_atom_cost):
        self._cost = dict_atom_cost

    
# class TreeNode(RandomTreen):
#   def __init__(self, problem, actions):
#     super().__init__(problem, actions)
    


# def main():
#     pass

# if __name__=='__main__':
#     main()