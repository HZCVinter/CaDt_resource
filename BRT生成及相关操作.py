print(end="")
'''
  基于树的查找法又被称为树表查找法，是指在树结构中查找某一个指定的数据，
能够将待查表组织成特定树的形式，并且能够在树结构上实现查找。基于树的查找
主要包括二叉排序树、平衡二叉树和B树。

  二叉排序树算法基础：
  二叉排序树又被称为二叉查找树，这是一种特殊结构的二叉树，在现实中通常
被定义为一颗空树，或者被描述为具有如下性质的二叉树：
    ①如果它的左子树非空，则左子树上所有节点的值均小于根节点的值
    ②如果它的右子树非空，则右子树上所有节点的值均大于根节点的值
    ③左右子树都是二叉排序树
  由此可见，对二叉排序树的定义可以用一个递归定义的过程来描述。由上述定义
可知二叉树的一个重要性质：当中序遍历一个二叉排序树时，可以得到一个递增的
有序序列。
  见附图1所示的二叉树就是两颗二叉排序树，如果中序遍历图8-2(a)所示的排
序二叉树，可得到如下递增有序序列：1-2-3-4-5-6-7-8-9
  
  插入与生成：
  已知一个关键字值为key的节点J，如果将其插入到二叉排序树中，需要保证插
入后仍然符合二叉排序树的定义。可以使用下面的方法进行插入操作：
    ①如果二叉排序树是空树，则key成为二叉排序树的根
    ②如果二叉排序树非空，则将key于二叉排序树的根进行如下比较：
        a. 如果key的值等于根节点的值，则停止插入
        b. 如果key的值小于根节点的值，则将key插入左子树
        c. 如果key的值大于根节点的值，则将key插入右子树    
  假如有一个元素序列，可以利用上述算法创建一颗二叉排序树。首先，将二叉排
序树初始化为一颗空树，然后逐个读入元素。每读入一个元素就建立一个新的节点，
将这个节点插入到当前已生成的二叉排序树中，通过调用上述二叉树的插入算法可
以将新节点插入。假设关键字的输入顺序为45、24、53、12、28、90，按上述算
法生成的二叉排序树的过程如附图2上图所示。
  对于同样的一些元素值，如果输入顺序不同，所创建的二叉树的形态也不同。假
如在上面的例子总的输入顺序为24、53、90、12、28、45，则生成的二叉排序树
如附图2下图所示。

  删除操作：
  从二叉树中删除某个节点，就是仅删除这个节点，而不把以该节点为根的所有子
树都删除掉，并且还要保证删除后得到的二叉树仍满足二叉排序树的性质。即在二叉
排序树中删除一个节点相当于删除所有有序序列中的一个节点。
  在删除操作之前，首先要查找确定被删除节点是否在二叉排序树中，如果不在则不
需要做任何操作。假设要删除的节点是p，节点p的双亲节点是f，如果节点p是以节点
f的左孩子，在删除时需要分如下三种情况来讨论：
    ①如果p为叶节点，则可以直接将其删除
    ②如果p节点只有左子树或只有右子树，则可将p的左子树或右子树，直接改为
其双亲节点f的左子树或右子树  
    ③如果p既有左子树，也有右子树，如附图3-a所示，此时有如下两种处理方法：
      a.首先找到p节点在中序序列中的直接前驱s节点，如附图3-b所示，然后将
    p的左子树改为f的左子树，而将p的右子树改为s的右子树: 
    f -> lchild = p -> lchild; s -> rchild = p -> rchild; free(p)
    结果如附图3-c所示；
      b.首先找到p节点在中序序列中的直接前驱s节点，如附图3-b所示，然后用
    s节点的值，代替p节点的值，再将s节点删除，原s节点的左子树改为s的双亲节
    点q的右子树：
    p -> data = s -> data; q -> rchild = s -> lchild; free(s)
    结果如附图3-d所示。

  查找操作：
  可以将二叉排序树看作是一个有序表，在这颗二叉排序树上可以进行查找操作。
二叉排序树的查找过程是一个逐步缩小查找范围的过程，可以根据二叉排序树的特点，
首先将待查关键字k与根节点关键字t进行比较，如果k=t，返回根节点地址，如果
k<t，进一步查找左子树，如果k>t，则进一步查右子树。
    
遍历：
深度优先遍历：
    先序遍历
        1.先访问根节点
        2.访问左节点
        3.访问右节点

    中序遍历
        1.先访问左节点
        2.访问根节点
        3.访问右节点
        
    后序遍历
        1.先访左根节点
        2.访问右节点
        3.访问根节点

广度优先遍历：
    层次遍历：
        每次出队一个元素，就将该元素的孩子节点加入队列中，
        直至队列中元素个数为0时，出队的顺序就是该二叉树的层次遍历结果。
'''


# 构建二叉树
class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.print())

    # 输出结果为：(left, data, right)
    def print(self, node="Unknown"):
        if node == "Unknown":
            node = self
        if type(node) is int:
            return node
        if node is None:
            return None
        if node.left is None and node.right is None:
            return node.data
        return self.print(node.left), node.data, self.print(node.right)


# 二叉树操作
# 搜索、插入和删除只适用于BST(二叉查找树)
class BTO:
    def __init__(self):
        self.root = None

    def __node__(self):
        return self.root

    # 生成二叉查找树，输入元素列表
    # 只适用于int列表和char列表
    def generate_BST(self, node_list):
        # 将第一个元素放中间
        self.root = Node(node_list[0])
        for data in node_list[1::]:
            self.insert(data)

    # 直接创建一个二叉树
    def create_binary_tree(self, tree):
        if tree is not None:
            self.root = tree

    # 插入
    def insert(self, data):
        is_found, n, p = self.search(self.root, self.root, data)
        if not is_found:
            if data > p.data:
                p.right = Node(data)
            if data < p.data:
                p.left = Node(data)

    # 搜索
    def search(self, node, parent, data):
        if node is None:
            return False, node, parent
        if node.data == data:
            return True, node, parent
        if node.data > data:
            return self.search(node.left, node, data)
        if node.data < data:
            return self.search(node.right, node, data)

    # 删除
    def delete(self, data, root="Unknown"):
        if root == "Unknown":
            root = self.root
        is_found, n, p = self.search(root, root, data)
        if is_found is False:
            print("没有该节点")
            return "Error"
        # 1.如果n为叶结点，则直接删除
        if n.left is None and n.right is None:
            n.data = None
        # 2.如果只有单侧树
        elif n.left is None and n.right is not None:
            n.data = n.right.data
            n.right = None
        elif n.left is not None and n.right is None:
            n.data = n.left.data
            n.left = None
        # 3.左右均非空
        else:
            # 方法一
            ls = n.right
            n.data = n.left.data
            n.right = n.left.right
            n.left = n.left.left
            new = root
            while new.right is not None:
                new = new.right
            new.right = ls
        return root

    # 先序遍历
    def pre_order_traverse(self, node="Unknown", res=None):
        if res is None:
            res = []
        if node == "Unknown":
            node = self.root
        if node is None:
            return False
        res.append(node.data)
        self.pre_order_traverse(node.left, res)
        self.pre_order_traverse(node.right, res)
        return res

    # 中序遍历
    def in_order_traverse(self, node="Unknown", res=None):
        if res is None:
            res = []
        if node == "Unknown":
            node = self.root
        if node is None:
            return False
        self.in_order_traverse(node.left, res)
        res.append(node.data)
        self.in_order_traverse(node.right, res)
        return res

    # 后序遍历
    def post_order_traverse(self, node="Unknown", res=None):
        if res is None:
            res = []
        if node == "Unknown":
            node = self.root
        if node is None:
            return False
        self.post_order_traverse(node.left, res)
        self.post_order_traverse(node.right, res)
        res.append(node.data)
        return res

    # 广度优先遍历-层次遍历
    def breath_first_traverse(self, node="Unknown"):
        res = []
        if node == "Unknown":
            node = self.root
        queue = [node]
        while len(queue) > 0:
            res.append(queue[0].data)
            if queue[0].left is not None:
                queue.append(queue[0].left)
            if queue[0].right is not None:
                queue.append(queue[0].right)
            queue.pop(0)
        return res


t1 = BTO()
t1.generate_BST([45, 24, 53, 12, 28, 90])
print(t1.root)
print()
node = Node(45, Node(12), Node(53, Node(46, right=Node(47)), Node(90)))
print(node)
t2 = BTO()
t2.create_binary_tree(node)
t2.delete(46)
print(t2.root)
print()
a = BTO()
a.generate_BST(['e', 'b', 'h', 'g', 'i', 'd', 'a', 'f', 'c'])
print(a.root)
print(a.pre_order_traverse())
print(a.in_order_traverse())
print(a.post_order_traverse())
print(a.breath_first_traverse())