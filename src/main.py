class Node:
    def __init__(self, name, is_or=True):
        self.name = name
        self.is_or = is_or  # True if OR node, False if AND node
        self.children = []  # List of tuples (child_node, cost)
        self.h = float('inf')  # Heuristic value
        self.g = 0  # Cost from the start node
        self.f = float('inf')  # Estimated total cost (f = g + h)
        self.parent = None
        self.best_child = None

    def add_child(self, child, cost):
        self.children.append((child, cost))
        child.parent = self

    def __repr__(self):
        return f"Node({self.name})"


def ao_star(start_node, goal_node):
    open_list = [start_node]
    closed_list = []

    def update_heuristics(node):
        if node.is_or:
            # OR node: choose the minimum cost child
            min_cost = float('inf')
            for child, cost in node.children:
                total_cost = cost + child.f
                if total_cost < min_cost:
                    min_cost = total_cost
                    node.best_child = child
            node.h = min_cost
        else:
            # AND node: sum the costs of all children
            node.h = sum(cost + child.f for child, cost in node.children)
            node.best_child = node.children

        node.f = node.g + node.h

    while open_list:
        current_node = open_list.pop(0)
        closed_list.append(current_node)

        if current_node == goal_node:
            break

        for child, cost in current_node.children:
            if child not in closed_list:
                child.g = current_node.g + cost
                open_list.append(child)

        update_heuristics(current_node)
        open_list.sort(key=lambda n: n.f)

    # Extract the solution path
    path = []
    node = start_node
    while node != goal_node:
        path.append(node.name)
        if node.is_or:
            node = node.best_child
        else:
            for child, _ in node.best_child:
                path.append(child.name)
            break
    path.append(goal_node.name)

    return path


# Example usage
if __name__ == "__main__":
    A = Node('A', is_or=True)
    B = Node('B', is_or=False)
    C = Node('C', is_or=True)
    D = Node('D', is_or=True)
    E = Node('E', is_or=True)
    F = Node('F', is_or=True)
    G = Node('G', is_or=True)

    A.add_child(B, 1)
    A.add_child(C, 2)
    B.add_child(D, 3)
    B.add_child(E, 1)
    C.add_child(F, 4)
    C.add_child(G, 1)
    D.add_child(G, 2)
    E.add_child(G, 3)
    F.add_child(G, 2)

    goal_node = G

    path = ao_star(A, goal_node)
    print(f"Solution path: {' -> '.join(path)}")
