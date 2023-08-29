# import itertools
# import random
# import string

import networkx as nx
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from ged import calc_similarity


def create_graph(nodes, edges):
    G = nx.Graph()
    for node in nodes:
        node["color"] = "blue"
        G.add_node(node["label"], **node)
    for edge in edges:
        edge[2]["color"] = "b"
    G.add_edges_from(edges)
    return G


def generate_edit_nodes(edit_node_path):
    edit_nodes = {"insert": [], "delete": [], "subst": []}
    for pre, post in edit_node_path:
        if pre == post:
            continue
        elif pre is None:
            edit_nodes["insert"].append(post)
        elif post is None:
            edit_nodes["delete"].append(pre)
        else:
            edit_nodes["subst"].append((pre, post))
    return edit_nodes


def generate_edit_edges(edit_edge_path):
    edit_edges = {"insert": [], "delete": [], "subst": []}
    for pre, post in edit_edge_path:
        if pre == post:
            continue
        elif pre is None:
            edit_edges["insert"].append(post)
        elif post is None:
            edit_edges["delete"].append(pre)
        else:
            edit_edges["subst"].append((pre, post))
    return edit_edges


def plot_edit_graph(G1, G2, node_edit_path, edge_edit_path):
    edit_nodes = generate_edit_nodes(node_edit_path)
    edit_edges = generate_edit_edges(edge_edit_path)

    G = nx.Graph()
    insert_nodes = edit_nodes["insert"]
    delete_nodes = edit_nodes["delete"]
    subst_nodes = edit_nodes["subst"]
    insert_edges = edit_edges["insert"]
    delete_edges = edit_edges["delete"]
    subst_edges = edit_edges["subst"]

    if len(insert_nodes) > 0:
        node = insert_nodes[0]
        if node in G1.nodes:
            G = G2
        else:
            G = G1
    elif len(delete_nodes) > 0:
        node = delete_nodes[0]
        if node in G1.nodes:
            G = G1
        else:
            G = G2
    elif len(subst_nodes) > 0:
        pre_node = subst_nodes[0][0]
        if pre_node in G1.nodes:
            G = G1
        else:
            G = G2
    elif len(insert_edges) > 0:
        edge = insert_edges[0]
        if edge in G1.edges:
            G = G2
        else:
            G = G1
    elif len(delete_edges) > 0:
        edge = delete_edges[0]
        if edge in G1.edges:
            G = G1
        else:
            G = G2
    elif len(subst_edges) > 0:
        pre_edge = subst_edges[0][0]
        if pre_edge in G1.edges:
            G = G1
        else:
            G = G2

    for node in insert_nodes:
        G.add_node(node, **{"color": "red"})

    for node in delete_nodes:
        G.nodes[node]["color"] = "red"

    for pre_node, post_node in subst_nodes:
        G.nodes[pre_node]["color"] = "red"
        G.add_node(post_node, **{"color": "red"})

    for edge in insert_edges:
        G.add_edge(edge[0], edge[1], **{"color": "red"})

    for edge in delete_edges:
        G.edges[edge]["color"] = "red"

    for pre_edge, post_edge in subst_edges:
        G.edges[edge]["color"] = "red"
        G.add_edge(post_edge[0], post_edge[1], **{"color": "red"})

    node_colors = [node[1]["color"] for node in G.nodes(data=True)]
    edge_colors = nx.get_edge_attributes(G, "color").values()

    fig, ax = plt.subplots(figsize=(15, 8))

    red_patch = mpatches.Patch(color="red", label="edit")
    blue_patch = mpatches.Patch(color="blue", label="not edit")
    plt.legend(handles=[red_patch, blue_patch])

    pos = nx.spring_layout(G, k=3)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)
    plt.show()


def plot_diff(
    node_edit_path,
    edge_edit_path,
):
    edit_nodes = generate_edit_nodes(node_edit_path)
    edit_edges = generate_edit_edges(edge_edit_path)

    G = nx.Graph()
    insert_nodes = edit_nodes["insert"]
    delete_nodes = edit_nodes["delete"]
    subst_nodes = edit_nodes["subst"]
    insert_edges = edit_edges["insert"]
    delete_edges = edit_edges["delete"]
    subst_edges = edit_edges["subst"]

    for node in insert_nodes:
        G.add_node(node, **{"color": "red"})

    for node in delete_nodes:
        G.add_node(node, **{"color": "red"})

    for pre_node, post_node in subst_nodes:
        G.add_node(pre_node, **{"color": "red"})
        G.add_node(post_node, **{"color": "red"})

    for edge in insert_edges:
        if edge[0] not in G.nodes:
            G.add_node(edge[0], **{"color": "blue"})
        if edge[1] not in G.nodes:
            G.add_node(edge[1], **{"color": "blue"})
        G.add_edge(edge[0], edge[1], **{"color": "red"})

    for edge in delete_edges:
        if edge[0] not in G.nodes:
            G.add_node(edge[0], **{"color": "blue"})
        if edge[1] not in G.nodes:
            G.add_node(edge[1], **{"color": "blue"})
        G.add_edge(edge[0], edge[1], **{"color": "red"})

    for pre_edge, post_edge in subst_edges:
        if pre_edge[0] not in G.nodes:
            G.add_node(pre_edge[0], **{"color": "blue"})
        if pre_edge[1] not in G.nodes:
            G.add_node(pre_edge[1], **{"color": "blue"})
        if post_edge[0] not in G.nodes:
            G.add_edge(post_edge[0], **{"color": "blue"})
        if post_edge[1] not in G.nodes:
            G.add_edge(post_edge[1], **{"color": "blue"})

        G.add_edge(pre_edge[0], pre_edge[1], **{"color": "red"})
        G.add_edge(post_edge[0], post_edge[1], **{"color": "red"})

    node_colors = [node[1]["color"] for node in G.nodes(data=True)]
    edge_colors = nx.get_edge_attributes(G, "color").values()

    fig, ax = plt.subplots(figsize=(15, 8))

    red_patch = mpatches.Patch(color="red", label="edit")
    blue_patch = mpatches.Patch(color="blue", label="not edit")
    plt.legend(handles=[red_patch, blue_patch])

    pos = nx.spring_layout(G, k=3)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)
    plt.show()


if __name__ == "__main__":
    # random graph

    # max_node_cost = 1000
    # max_edge_cost = 1000
    # labels = list(string.ascii_uppercase)

    # g1_nodes = random.sample(labels, random.randint(2, len(labels)))
    # g1_edges = [edge for edge in itertools.combinations(g1_nodes, 2)]
    # G1_nodes = [{"label": node, "weight": random.randint(1, max_node_cost)} for node in g1_nodes]
    # G1_edges = [
    #     (
    #         edge[0],
    #         edge[1],
    #         {"node": edge, "weight": random.randint(1, 100)},
    #     )
    #     for edge in random.sample(g1_edges, random.randint(1, len(g1_edges)))
    # ]
    # G1 = create_graph(G1_nodes, G1_edges)

    # g2_nodes = random.sample(labels, random.randint(2, len(labels)))
    # g2_edges = [edge for edge in itertools.combinations(g2_nodes, 2)]
    # G2_nodes = [{"label": node, "weight": random.randint(1, 100)} for node in g2_nodes]
    # G2_edges = [
    #     (
    #         edge[0],
    #         edge[1],
    #         {"node": edge, "weight": random.randint(1, 100)},
    #     )
    #     for edge in random.sample(g2_edges, random.randint(1, len(g2_edges)))
    # ]
    # G2 = create_graph(G2_nodes, G2_edges)

    G1_nodes = [
        {"label": "A", "weight": 1, "color": "blue"},
        {"label": "B", "weight": 1, "color": "blue"},
        {"label": "C", "weight": 5, "color": "blue"},
        {"label": "D", "weight": 1, "color": "blue"},
    ]
    G1_edges = [
        ("A", "B", {"node": ("A", "B"), "weight": 8, "color": "blue"}),
        ("A", "C", {"node": ("A", "C"), "weight": 12, "color": "blue"}),
        ("B", "C", {"node": ("B", "C"), "weight": 10, "color": "blue"}),
        ("C", "D", {"node": ("C", "D"), "weight": 15, "color": "blue"}),
    ]
    G1 = create_graph(G1_nodes, G1_edges)

    G2_nodes = [
        {"label": "A", "weight": 1, "color": "blue"},
        {"label": "B", "weight": 3, "color": "blue"},
        {"label": "C", "weight": 1, "color": "blue"},
    ]
    G2_edges = [
        ("A", "B", {"node": ("A", "B"), "weight": 15, "color": "blue"}),
        ("B", "C", {"node": ("B", "C"), "weight": 10, "color": "blue"}),
    ]
    G2 = create_graph(G2_nodes, G2_edges)

    limit = 600
    similarity, node_edit_path, edge_edit_path = calc_similarity(G1, G2, limit)
    print(similarity)

    plot_diff(node_edit_path, edge_edit_path)
    plot_edit_graph(G1, G2, node_edit_path, edge_edit_path)
