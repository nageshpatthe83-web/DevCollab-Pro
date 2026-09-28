# Viva Defense Cheat Sheet (Questions & Answers)

This guide prepares all 4 team members of **Group SY06** to ace the faculty viva defense.

---

### General Questions for Everyone

**Q1: Why did you choose DevCollab Pro instead of a normal web app or simple LeetCode clone?**  
*Answer:* A normal LeetCode clone only tests binary correctness (input vs output). DevCollab Pro provides **multi-dimensional, explainable evaluation**: it analyzes AST code quality, empirical Big-O execution efficiency, Git collaboration fairness, and compresses storage using delta algorithms—covering DBMS, OOP, and DSA within our syllabus.

**Q2: How does your platform support Green IT and sustainability?**  
*Answer:* Two ways: (1) `CodeVault` uses Myers Diff delta compression, storing only incremental modifications to save >60% database storage footprint. (2) `AlgoPro` profiles code on scaled inputs, flagging inefficient $O(n^2)$ or $O(2^n)$ loops before they consume wasteful CPU energy at cloud scale.

---

### Questions for Nagesh (Roll No. 11)
*Focus: Leaderboard, Max-Heap, Analytics & Reporting*

**Q: Why use a Max-Heap for the leaderboard instead of sorting an array?**  
*Answer:* Sorting an array on every new submission takes $O(n \log n)$ time. With a Max-Heap, inserting or updating a team's score takes only $O(\log n)$ time, and retrieving the top $k$ teams takes $O(k \log n)$ time. This prevents server bottlenecks during peak hackathon submissions.

**Q: Explain how your composite scoring formula works.**  
*Answer:* The scoring engine uses a weighted linear combination:
$$\text{Score} = 0.25(\text{Quality}) + 0.20(\text{Perf}) + 0.15(\text{Repo}) + 0.15(\text{Innovation}) + 0.10(\text{Collab}) + 0.10(\text{Docs}) + 0.05(\text{Security})$$
Every dimension is scaled from 0 to 100, providing an explainable breakdown to students and judges.

---

### Questions for Kunal (Roll No. 50)
*Focus: System Architecture & 5 GoF Design Patterns*

**Q: Name the 5 design patterns implemented in CodeSentry and explain one.**  
*Answer:* Strategy, Visitor, Factory, Observer, and Singleton. In the **Strategy Pattern**, each evaluation rule (Complexity, Security, Code Smells) implements a common `AnalysisStrategy` interface. This allows us to add new inspection rules without modifying the analyzer pipeline (Open/Closed Principle).

---

### Questions for Shantanu (Roll No. 04)
*Focus: Contests, Submission Queue, & DSA Queue*

**Q: How does the submission queue handle high traffic?**  
*Answer:* Submissions are enqueued into a thread-safe FIFO Queue. Background worker processes pull submissions concurrently according to available CPU cores, preventing server crashes during submission deadlines.

---

### Questions for Jagdish (Roll No. 10)
*Focus: CodeVault, Delta Compression & Three-Way Merge*

**Q: How does delta storage work, and what is a three-way merge?**  
*Answer:* Delta storage uses Myers Diff to store only the lines added, deleted, or changed between commits rather than full file duplicates. A three-way merge compares the target branch and source branch against their common ancestor to detect overlapping line modifications and flag merge conflicts cleanly.
