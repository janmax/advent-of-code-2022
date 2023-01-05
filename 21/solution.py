puzzle = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

from collections import namedtuple
from dataclasses import dataclass


@dataclass
class Node:
    name: str
    left: "Node"
    right: "Node"
    value: int
    op: str

    def __repr__(self):
        return f"Node(name={self.name}, left={self.left and self.left.value}, right={self.right and self.right.value}, value={self.value}, op={self.op}"


with open("puzzle.in") as f:
    puzzle = f.read()

nodes_raw = dict(line.split(": ") for line in puzzle.strip().split("\n"))
nodes = {name: Node(name, None, None, None, value) for name, value in nodes_raw.items()}

for name, node in nodes.items():
    if " " in node.op:
        left, op, right = node.op.split()
        left, right = nodes[left], nodes[right]
        node.left = left
        node.right = right
        node.op = op
    else:
        node.value = int(node.op)
        node.op = None


def get_function(op):
    match op:
        case "+":
            return lambda a, b: a + b
        case "-":
            return lambda a, b: a - b
        case "*":
            return lambda a, b: a * b
        case "/":
            return lambda a, b: a // b


def dfs(node):
    if node.name == "humn":
        node.value = "humn"
        return "humn"
    if node.value:
        return node.value
    left_value = dfs(node.left)
    right_value = dfs(node.right)
    if "humn" in (left_value, right_value):
        node.value = "humn"
    else:
        node.value = get_function(node.op)(left_value, right_value)
    return node.value


root = nodes["root"]
dfs(nodes["root"])
if root.left.value == "humn":
    current = root.left
    target = root.right.value
else:
    current = root.right
    target = root.left.value


def dfs_print(node, d=0):
    if node is None:
        return
    print(". " * d, node, sep="")
    dfs_print(node.left, d + 1)
    dfs_print(node.right, d + 1)


# dfs_print(root)


def inverse(op, target, value, left):
    match op, left:
        case "+", _:
            return target - value
        case "*", _:
            return target // value
        case "-", True:
            return target + value
        case "-", False:
            return value - target
        case "/", True:
            return target * value
        case "/", False:
            return value // target


while current.name != "humn":
    if left := current.left.value == "humn":
        target = inverse(current.op, target, current.right.value, True)
        current = current.left
    else:
        target = inverse(current.op, target, current.left.value, False)
        current = current.right

print(target)
