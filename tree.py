class Node():
    def __init__(self,value,parent):
        self.value = value
        self.parent = parent
        self.children = []

    def add_children(self,children):
        for child in children:
            node = Node(child,parent=self)
            self.children.append(node)

    def get_parents(self):
        parents = []
        parent = self.parent
        while True:
            if parent:
                parents.append(parent)
                parent = parent.parent
            else:
                break
        return list(reversed(parents))
    
    def get_path(self):
        
        parents = self.get_parents()
        parents += [self]
        return parents
    
    def __repr__(self):
        return f'Node: {self.value}'
    
class Tree():
    def __init__(self,root):
        self.root = Node(root,parent=None,)
    
    