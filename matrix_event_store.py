from matrix_event import MatrixEvent

class MatrixEventStore:

    HeadNode = None
    NodeMap = dict()

    def Add(self, node):
        if self.HeadNode is None:
            node.Next = None
            node.Prev = None
            self.HeadNode = node
            self.LastNode = node
        else:
            node.Next = None
            node.Prev = self.LastNode
            self.LastNode.Next = node
            self.LastNode = node

        if (node.Id in self.NodeMap) is False:
            self.NodeMap[node.Id] = node

    def AddPrev(self, node, from_node):
        node.Prev = from_node.Prev
        node.Next = from_node
        from_node.Prev = node
        if from_node is self.HeadNode:
            self.HeadNode = node

        if (node.Id in self.NodeMap) is False:
            self.NodeMap[node.Id] = node

    def AddNext(self, node, from_node):
        node.Next = from_node.Next
        node.Prev = from_node
        from_node.Next = node
        if from_node is self.LastNode:
            self.LastNode = node

        if (node.Id in self.NodeMap) is False:
            self.NodeMap[node.Id] = node

    def Delete(self, node):
        curr_node = self.HeadNode

        while True:
            if curr_node is node:
                prev_node = curr_node.Prev
                next_node = curr_node.Next
                if prev_node is not None:
                    prev_node.Next = next_node

                if next_node is not None:
                    next_node.Prev = prev_node

                if curr_node is self.HeadNode:
                    self.HeadNode = next_node

                if curr_node is self.LastNode:
                    self.LastNode = prev_node
                break

            curr_node = curr_node.Next
            if curr_node is None:
                break

        if node.Id in self.NodeMap:
            del self.NodeMap[node.Id]

    def HasNode(self, id):
        if id in self.NodeMap:
            return True
        else:
            return False

    def GetNode(self, id):
        if id in self.NodeMap:
            return self.NodeMap[id]
        else:
            return None

    def Delete(self, id):
        if id in self.NodeMap:
            self.Delete(self.NodeMap[id])
            return self.NodeMap[id]
