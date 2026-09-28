# DevCollab Pro — System Architecture

**DevCollab Pro** is an automated, multi-dimensional hackathon project evaluation platform that moves beyond simplistic binary pass/fail grading into transparent, explainable software assessment.

```
+-----------------------------------------------------------------------------------+
|                                 DEVELOPER / TEAM                                  |
|                 Submits Complete Project (ZIP / Git Repository)                   |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                        FASTAPI REST BACKEND & WORKER QUEUE                        |
|        - Non-blocking Submission Queue (DSA Queue Dispatcher)                     |
|        - Validates project file structure, language runtimes, & dependencies      |
+--------+---------------------------------+--------------------------------+-------+
         |                                 |                                |
         v                                 v                                v
+----------------------+         +----------------------+         +-----------------+
|      CODEVAULT       |         |      CODESENTRY      |         |     ALGOPRO     |
|    (DBMS Pillar)     |         |     (OOP Pillar)     |         |  (DSA Pillar)   |
+----------------------+         +----------------------+         +-----------------+
| - Myers Diff Engine  |         | - AST Syntax Traversal|        | - Runtime & Mem |
| - Delta Compression  |         | - 5 GoF Patterns:    |         |   Execution     |
|   (>60% space saved) |         |   * Strategy         |         | - Empirical     |
| - 3-Way Merge Branch |         |   * Visitor          |         |   Big-O Curve   |
|   Reconciliation     |         |   * Factory          |         |   Fitting       |
| - 3NF 9-Table Schema |         |   * Observer         |         | - Self-Balance  |
| - 5 Analytical Views |         |   * Singleton        |         |   AVL Tree      |
|                      |         | - Vulnerability Scan |         | - Dijkstra      |
+----------+-----------+         +----------+-----------+         +--------+--------+
           |                                |                              |
           +--------------------------------+------------------------------+
                                            |
                                            v
+-----------------------------------------------------------------------------------+
|                       COMPOSITE SCORING & LEADERBOARD ENGINE                      |
|                                                                                   |
|   Formula:                                                                        |
|   Score = 0.25(Quality) + 0.20(Perf) + 0.15(Repo) + 0.15(Innovation)             |
|         + 0.10(Collab)  + 0.10(Docs) + 0.05(Security)                             |
|                                                                                   |
|   - Max-Heap PriorityQueue: O(log n) Updates & O(k) Top-k Retrieval               |
|   - Git Collaboration Graph: Per-member fairness & commit contribution analysis  |
+-------------------------------------------+---------------------------------------+
                                            |
                                            v
+-----------------------------------------------------------------------------------+
|                     MODERN REACT / HTML5 INTERACTIVE DASHBOARD                    |
|   - Live CodeSentry AST Visualizer & Security Inspector                           |
|   - AlgoPro Big-O Curve Visualizer & Performance Benchmarker                      |
|   - CodeVault Delta Storage Compression Analyzer                                  |
|   - Animated Real-time Top-k Standings Table                                      |
+-----------------------------------------------------------------------------------+
```

---

## The Three Core Pillars

### 1. CodeVault (DBMS Pillar)
* **Delta Storage:** Instead of duplicating full source files for every commit, CodeVault computes granular JSON-based delta operations using the Myers Diff algorithm. This reduces relational database disk consumption by over **60%**, serving as an explicit **Green IT & Sustainable Computing** initiative.
* **Three-Way Merge:** Compares incoming branch edits against a common ancestor baseline, reconciling non-conflicting lines and outputting standard Git conflict demarcations (`<<<<<<< OURS`, `=======`, `>>>>>>> THEIRS`).
* **Normalized 3NF Relational Database:** Comprises 9 primary entities (`Users`, `Teams`, `TeamMembers`, `Contests`, `Problems`, `Submissions`, `EvaluationScores`, `LeaderboardEntries`, `GitRepositories`) and 5 analytical reporting views.

### 2. CodeSentry (OOP Pillar)
* **Abstract Syntax Tree (AST) Parsing:** Generates a syntax tree of submitted code, traversing nodes to collect metrics and check for security vulnerabilities.
* **Five Classic GoF Design Patterns:**
  1. *Strategy Pattern:* Encapsulates interchangeable analysis rules (`ComplexityStrategy`, `SecurityVulnerabilityStrategy`, `CodeSmellStrategy`).
  2. *Visitor Pattern:* Navigates AST nodes (`ASTMetricsVisitor`, `FunctionComplexityVisitor`) to track function lengths, branching factor, and dangerous calls (`eval`, raw SQL concatenation).
  3. *Factory Pattern:* Dynamically instantiates language analyzers via `AnalyzerFactory`.
  4. *Observer Pattern:* Publishes real-time telemetry events during analysis via `AnalysisSubject` and `AnalysisObserver`.
  5. *Singleton Pattern:* Thread-safe `ConfigurationManager` providing consistent rule thresholds across all execution workers.

### 3. AlgoPro (DSA Pillar)
* **Empirical Big-O Curve Fitter:** Measures execution wall-clock time on scaled input sizes ($n \in [50, 150, 300, 600, 1200]$) and performs least-squares regression across $O(1), O(\log n), O(n), O(n \log n), O(n^2), O(2^n)$ to determine real-world computational complexity.
* **Self-Balancing AVL Tree:** Demonstrates tree height-balancing and records Left-Left (LL), Right-Right (RR), Left-Right (LR), and Right-Left (RL) rotations.
* **Dijkstra Shortest Path:** Adjacency-list graph algorithm with min-heap priority queue for optimal service pathways.
* **Max-Heap PriorityQueue:** Custom binary heap ordering team scores in $O(\log n)$ update time, eliminating expensive $O(n \log n)$ total array sorting.
