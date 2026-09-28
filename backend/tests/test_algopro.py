import pytest
from app.algopro.big_o_fitter import EmpiricalBigOFitter
from app.algopro.data_structures.avl_tree import AVLTree
from app.algopro.data_structures.dijkstra import GraphDijkstra
from app.algopro.data_structures.priority_queue import MaxHeapPriorityQueue

def test_empirical_big_o_fitting():
    n_vals = [10, 20, 30, 40, 50]
    times_linear = [0.01, 0.02, 0.03, 0.04, 0.05]
    res = EmpiricalBigOFitter.fit(n_vals, times_linear)
    assert res["verdict"] in ["O(n)", "O(1)"]
    assert res["best_r_squared"] > 0.8

def test_avl_tree_balance_and_rotations():
    avl = AVLTree()
    # Inserting in ascending order forces Left-Left (LL) right rotations
    for val in [10, 20, 30, 40, 50]:
        avl.insert(val)
    assert len(avl.rotation_log) > 0
    assert avl.inorder_traversal() == [10, 20, 30, 40, 50]
    assert abs(avl.get_balance(avl.root)) <= 1

def test_dijkstra_shortest_path():
    g = GraphDijkstra()
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)
    g.add_edge("A", "C", 5)
    res = g.shortest_path("A", "C")
    assert res["distance"] == 3
    assert res["path"] == ["A", "B", "C"]

def test_max_heap_leaderboard():
    pq = MaxHeapPriorityQueue()
    pq.insert_or_update("T1", "Team Alpha", 70.0)
    pq.insert_or_update("T2", "Team Beta", 95.0)
    pq.insert_or_update("T3", "Team Gamma", 85.0)

    top2 = pq.get_top_k(2)
    assert len(top2) == 2
    assert top2[0]["team_id"] == "T2"
    assert top2[0]["rank"] == 1
    assert top2[1]["team_id"] == "T3"
    assert top2[1]["rank"] == 2
