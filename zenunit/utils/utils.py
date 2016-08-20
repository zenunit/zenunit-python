"""This module contains utilities"""

def tree_layout(tree):
    LINE_SPACE = 2 
    def pos_node(node, px, py, pos):
        i = 0 
        j = 0 
        for i, subnode in enumerate(tree.successors(node)):
            pos_x = px + 1 
            pos_y = py - i*LINE_SPACE - j 
            pos[subnode] = (pos_x, pos_y)
            j += pos_node(subnode, pos_x, pos_y, pos)
        return i*LINE_SPACE + j 

    pos = {}
    pos[tree.rootnode] = (0, 0)
    pos_node(tree.rootnode, 0, 0, pos)

    return pos 

## BFS
#def tree_layout(tree):
#    pos = {}
#    pos[tree.rootnode] = (0, 0)
#
#    queue = [(tree.rootnode, 0, 0)]
#    while queue:
#        vertex, px, py = queue.pop(0)
#        for i, subnode in enumerate(tree.successors(vertex)):
#            pos[subnode] = (px+i, py-1)
#            queue.append((subnode, px+i, py-1))
#
#    return pos

