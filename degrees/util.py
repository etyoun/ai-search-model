class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        """Appends a node to the frontier."""
        self.frontier.append(node)

    def contains_state(self, state):
        """Returns True if the state is in the frontier."""
        for node in self.frontier:
            if node.state == state:
                return True
        return False

    def empty(self):
        """Returns True if the frontier is empty."""
        return len(self.frontier) == 0

    def remove(self):
        """Removes and returns the first node in the frontier."""
        raise NotImplementedError


class StackFrontier(Frontier):
    def remove(self):
        """Removes and returns the first node in the frontier."""
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop(0)


class QueueFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop(0)
