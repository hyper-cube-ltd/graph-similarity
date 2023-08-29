import networkx as nx


def calc_similarity(G1, G2, limit=600):
    opt_v = None
    for v in nx.optimize_edit_paths(
        G1,
        G2,
        node_del_cost=node_del_cost,
        node_ins_cost=node_ins_cost,
        node_subst_cost=node_subst_cost,
        edge_del_cost=edge_del_cost,
        edge_ins_cost=edge_ins_cost,
        edge_subst_cost=edge_subst_cost,
        timeout=limit,
    ):
        opt_v = v

    node_edit_path, edge_edit_path, costG1G2 = opt_v

    G0 = nx.Graph()

    opt_v = None
    for v in nx.optimize_edit_paths(
        G0,
        G1,
        node_del_cost=node_del_cost,
        node_ins_cost=node_ins_cost,
        node_subst_cost=node_subst_cost,
        edge_del_cost=edge_del_cost,
        edge_ins_cost=edge_ins_cost,
        edge_subst_cost=edge_subst_cost,
        timeout=limit,
    ):
        opt_v = v

    _, _, costG0G1 = opt_v

    opt_v = None
    for v in nx.optimize_edit_paths(
        G0,
        G2,
        node_del_cost=node_del_cost,
        node_ins_cost=node_ins_cost,
        node_subst_cost=node_subst_cost,
        edge_del_cost=edge_del_cost,
        edge_ins_cost=edge_ins_cost,
        edge_subst_cost=edge_subst_cost,
        timeout=limit,
    ):
        opt_v = v

    _, _, costG0G2 = opt_v

    similarity = 1 - (costG1G2 / (costG0G1 + costG0G2))

    return similarity, node_edit_path, edge_edit_path


# arguments
# arguments for nodes
def node_subst_cost(node1, node2):
    if node1 == node2:
        return 0
    elif node1["label"] == node2["label"]:
        return abs(node1["weight"] - node2["weight"])
    return abs(node1["weight"]) + abs(node2["weight"])


def node_del_cost(node):
    return node["weight"]


def node_ins_cost(node):
    return node["weight"]


# arguments for edges
def edge_subst_cost(edge1, edge2):
    if edge1 == edge2["node"]:
        return 0
    elif edge1["node"] == edge2["node"]:
        return abs(edge1["weight"] - edge2["weight"])
    return abs(edge1["weight"]) + abs(edge2["weight"])


def edge_del_cost(edge):
    return edge["weight"]


def edge_ins_cost(edge):
    return edge["weight"]
