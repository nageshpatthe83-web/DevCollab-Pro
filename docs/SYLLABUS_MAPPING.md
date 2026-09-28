# VIT Academic Syllabus Mapping

DevCollab Pro is designed to strictly align 100% with the second-year engineering curriculum across **DBMS**, **OOP**, and **DSA**.

---

## 1. DBMS Syllabus Mapping
* **Relational Data Modeling:** 9 entities modeled in Third Normal Form (3NF) eliminating update, deletion, and insertion anomalies.
* **Keys & Referential Integrity:** Primary keys, foreign key constraints (`ON DELETE CASCADE` / `RESTRICT`), and composite keys.
* **Indexing:** B-Tree indexing on frequently queried columns (`user_id`, `contest_id`, `team_id`, `submitted_at`).
* **Analytical Reporting Views:**
  1. `vw_team_performance_summary`
  2. `vw_leaderboard_standings`
  3. `vw_code_quality_audit`
  4. `vw_submission_bottlenecks`
  5. `vw_student_contribution_breakdown`
* **ACID Transactions:** Atomic commits and transactional rollbacks during repository operations.

---

## 2. OOP Syllabus Mapping
* **Encapsulation:** Clear separation of internal state and public interfaces across dataclasses and services.
* **Inheritance & Polymorphism:** Strategy and Visitor hierarchies allowing extensible, pluggable evaluation behavior.
* **Abstraction:** Abstract Base Classes (`AnalysisStrategy`, `BaseLanguageAnalyzer`, `AnalysisObserver`) defining strict contracts.
* **5 GoF Design Patterns:**
  * **Strategy Pattern:** `ComplexityStrategy`, `SecurityVulnerabilityStrategy`, `CodeSmellStrategy`.
  * **Visitor Pattern:** `ASTMetricsVisitor` and `FunctionComplexityVisitor`.
  * **Factory Pattern:** `AnalyzerFactory` for language-specific analysis.
  * **Observer Pattern:** `AnalysisSubject` and `MetricsCollectorObserver`.
  * **Singleton Pattern:** Thread-safe `ConfigurationManager`.

---

## 3. DSA Syllabus Mapping
* **Priority Queue / Max-Heap:** $O(\log n)$ insertion and $O(k)$ top-$k$ leaderboard retrieval.
* **Self-Balancing AVL Tree:** Rotations (LL, RR, LR, RL) guaranteeing $O(\log n)$ balance factor.
* **Graph Algorithms:** Dijkstra's shortest path with adjacency list and min-heap.
* **Queues & Worker Scheduling:** FIFO dispatch queue managing simultaneous submissions.
* **Empirical Complexity Analysis:** Regression-based Big-O curve fitting.
