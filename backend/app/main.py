"""
DevCollab Pro - FastAPI Backend Application
Unified REST API serving:
- CodeSentry (OOP AST Static Analyzer & 5 Design Patterns)
- AlgoPro (DSA Execution Profiler, Empirical Big-O & AVL Tree)
- CodeVault (DBMS Delta Storage VCS & 3-Way Merge)
- Scoring Engine & Real-time Max-Heap Leaderboard
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

from .codesentry.analyzer_service import CodeSentryAnalyzer
from .codesentry.patterns.singleton import ConfigurationManager
from .algopro.profiler_service import ProfilerService
from .algopro.data_structures.priority_queue import MaxHeapPriorityQueue
from .algopro.data_structures.avl_tree import AVLTree
from .algopro.data_structures.dijkstra import GraphDijkstra
from .codevault.delta_engine import DeltaEngine
from .codevault.three_way_merge import ThreeWayMerge
from .codevault.repository_service import RepositoryService
from .scoring.scoring_engine import MultiCriteriaScoringEngine
from .scoring.contribution_tracker import ContributionTracker

app = FastAPI(
    title="DevCollab Pro API",
    description="Automated Hackathon Software Project Evaluation Platform - VIT Pune Group SY06",
    version="1.0.0"
)

# Enable CORS for frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory services
repo_service = RepositoryService()
leaderboard_heap = MaxHeapPriorityQueue()
scoring_engine = MultiCriteriaScoringEngine()

# Seed default mock teams on startup
leaderboard_heap.insert_or_update("T-01", "Group SY06 (DevCollab Pro)", 92.4, {
    "quality": 94.0, "performance": 91.5, "repo": 95.0, "innovation": 90.0, "collab": 92.5
})
leaderboard_heap.insert_or_update("T-02", "NeuralHackers", 86.8, {
    "quality": 88.0, "performance": 85.0, "repo": 84.0, "innovation": 92.0, "collab": 85.0
})
leaderboard_heap.insert_or_update("T-03", "AlgoKnights", 83.2, {
    "quality": 81.0, "performance": 96.0, "repo": 78.0, "innovation": 80.0, "collab": 81.0
})
leaderboard_heap.insert_or_update("T-04", "ByteBuilders", 77.5, {
    "quality": 75.0, "performance": 79.0, "repo": 80.0, "innovation": 76.0, "collab": 78.0
})

# Pydantic Schemas
class CodeAnalyzeRequest(BaseModel):
    code: str
    filename: Optional[str] = "solution.py"

class AlgorithmProfileRequest(BaseModel):
    algorithm_name: str

class DeltaRequest(BaseModel):
    base_content: str
    target_content: str

class MergeRequest(BaseModel):
    base_text: str
    ours_text: str
    theirs_text: str

class ScoreCalculationRequest(BaseModel):
    team_id: str
    team_name: str
    metrics: Dict[str, float]

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "DevCollab Pro",
        "version": "1.0.0",
        "institution": "Vishwakarma Institute of Technology, Pune",
        "group": "SY06",
        "modules": ["CodeVault (DBMS)", "CodeSentry (OOP)", "AlgoPro (DSA)", "Scoring Engine"]
    }

# 1. CodeSentry API
@app.post("/api/analyze")
def analyze_code(req: CodeAnalyzeRequest):
    analyzer = CodeSentryAnalyzer()
    res = analyzer.run_full_analysis(req.code, filename=req.filename or "code.py")
    return res

# 2. AlgoPro API
@app.post("/api/profile")
def profile_algorithm(req: AlgorithmProfileRequest):
    return ProfilerService.profile_algorithm(req.algorithm_name)

@app.get("/api/dsa/avl-demo")
def demo_avl_tree():
    avl = AVLTree()
    keys = [10, 20, 30, 40, 50, 25]
    for k in keys:
        avl.insert(k)
    return {
        "keys_inserted": keys,
        "inorder_traversal": avl.inorder_traversal(),
        "rotations_recorded": avl.rotation_log,
        "is_balanced": abs(avl.get_balance(avl.root)) <= 1
    }

@app.get("/api/dsa/dijkstra-demo")
def demo_dijkstra():
    g = GraphDijkstra()
    edges = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10), ("D", "E", 2)]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g.shortest_path("A", "E")

# 3. CodeVault API
@app.post("/api/vcs/delta")
def compute_delta(req: DeltaRequest):
    return DeltaEngine.generate_delta(req.base_content, req.target_content)

@app.post("/api/vcs/merge")
def three_way_merge(req: MergeRequest):
    return ThreeWayMerge.merge(req.base_text, req.ours_text, req.theirs_text)

# 4. Scoring & Leaderboard API
@app.get("/api/leaderboard")
def get_leaderboard(k: int = 10):
    return {
        "ranking_algorithm": "Max-Heap PriorityQueue (O(k log n))",
        "standings": leaderboard_heap.get_top_k(k=k)
    }

@app.post("/api/scoring/submit")
def calculate_and_rank(req: ScoreCalculationRequest):
    result = scoring_engine.calculate_score(req.metrics)
    final_score = result["final_score"]
    leaderboard_heap.insert_or_update(req.team_id, req.team_name, final_score, result["breakdown"])
    new_rank = leaderboard_heap.get_team_rank(req.team_id)
    return {
        "team_id": req.team_id,
        "team_name": req.team_name,
        "rank": new_rank,
        "scoring_details": result
    }

# 5. Git Collaboration & Team Fairness API
@app.get("/api/analytics/collaboration")
def get_collaboration_stats():
    records = [
        {"author": "Nagesh", "commits": 12, "lines_added": 480, "lines_removed": 60, "prs_reviewed": 5},
        {"author": "Kunal", "commits": 14, "lines_added": 520, "lines_removed": 80, "prs_reviewed": 6},
        {"author": "Shantanu", "commits": 10, "lines_added": 390, "lines_removed": 45, "prs_reviewed": 4},
        {"author": "Jagdish", "commits": 11, "lines_added": 410, "lines_removed": 50, "prs_reviewed": 4}
    ]
    return ContributionTracker.analyze_team_contributions(records)

# 6. Green IT & Sustainability Stats
@app.get("/api/analytics/green-it")
def get_green_it_stats():
    return {
        "delta_storage_savings_percentage": 64.8,
        "raw_storage_mb": 420.5,
        "delta_storage_mb": 148.0,
        "disk_space_saved_mb": 272.5,
        "energy_reduction_kwh_est": 18.4,
        "carbon_saved_kg_co2": 8.7,
        "sdg_alignment": ["SDG 12: Responsible Consumption", "SDG 9: Industry & Innovation"]
    }
