class Solution:
    def findRedundantConnection(self, edges):
        tree = [-1] * (len(edges)+1) # 點的總數

        for edge in edges:
            # 確認兩個點的老大是誰
            a = self.findRoot(edge[0], tree) # 邊的第一個點在哪個群組
            b = self.findRoot(edge[1], tree) # 邊的第二個點在哪個群組
            # 如果老大不同，連結他們
            if a != b:
                tree[a] = b
            # 如果相同，表示已經形成環，就把這個邊去掉
            else:
                return edge

    def findRoot(self, x, tree):
        if tree[x] == -1:
            return x
        else:
            root = self.findRoot(tree[x], tree)
            tree[x] = root
            return root
