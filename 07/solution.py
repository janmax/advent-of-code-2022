with open("puzzle.in") as f:
    commands = f.read().strip().split("\n")


def new_node():
    return {"files": [], "subdirs": {}, "parent": None}


root = new_node()
root["parent"] = root
current_node = root
i = 0

for command in commands:
    if command == "$ cd /":
        current_node = root
    elif command == "$ cd ..":
        current_node = current_node["parent"]
    elif command.startswith("$ cd"):
        target = command.split()[2]
        target_node = current_node["subdirs"].setdefault(target, new_node())
        target_node["parent"] = current_node
        current_node = target_node
    elif command == "$ ls":
        pass
    elif command.startswith("dir "):
        target = command.split()[1]
        current_node["subdirs"].setdefault(target, new_node())
    else:
        size, filename = command.split()
        current_node["files"].append(int(size))


def dfs_count(node):
    node["value"] = sum(node["files"]) + sum(
        dfs_count(n) for n in node["subdirs"].values() if n
    )
    return node["value"]


def dfs_flatten(node):
    children = [c for n in node["subdirs"].values() for c in dfs_flatten(n)]
    return [node, *children]


dfs_count(root)
all_nodes = dfs_flatten(root)

part_1 = sum(n["value"] for n in all_nodes if n["value"] <= 1e5)

needed = 30_000_000
total = 70_000_000
used = root["value"]
gap = needed - (total - used)
part_2 = min(n["value"] for n in all_nodes if n["value"] >= gap)

print(part_1)
print(part_2)
