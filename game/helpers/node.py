class Node:

    point = None
    previous_node = None
    action = None

    def __init__(self, point):
        self.point = point

    def __eq__(self, other):
        return self.point == other.point

    def __hash__(self):
        return hash(str(self.point.x)+str(self.point.y))