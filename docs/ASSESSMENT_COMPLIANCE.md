# VIT Assessment Sheet Compliance Guide

This document establishes 100% compliance with every criterion specified in the official VIT Project Assessment Sheet:  
**`OOP_CP_PBL_PCL_Assessment Sheet_Revised(2).xlsx`**

---

## 1. Mid-Semester Exam (MSE — Scaled to 30 Marks)

| Column & Criterion | Max Marks | Project Evidence in DevCollab Pro |
|---|:---:|---|
| **Problem Definition, Related Work & Complexity** | **10** | • Documents research gaps in existing online judges (AOJ) and LLM-as-a-judge platforms.<br>• Synthesizes 5 peer-reviewed papers highlighting lack of static code analysis, opaque binary scoring, and invisible team member effort. |
| **Proposed Solution, Technical Approach & Feasibility** | **12** | • 3-Pillar architecture (`CodeVault`, `CodeSentry`, `AlgoPro`) built on FastAPI and MySQL.<br>• 11-step end-to-end evaluation pipeline with transparent 7-dimensional scoring. |
| **Cost, Resources, Environmental Relevance & Sustainability** | **8** | • 100% open-source technologies (zero licensing fees).<br>• Delta-storage saves >60% database storage footprint (Green IT).<br>• Algorithmic efficiency analysis prevents CPU cycle waste in cloud clusters. |
| **Teamwork & Project Management** | **10** | • Feature-wise matrix (Kunal, Shantanu, Jagdish, Nagesh) ensuring cross-domain mastery.<br>• Git branching workflow (`main`, `develop`, feature branches, peer PR reviews). |
| **Communication & Presentation** | **10** | • 13-slide PowerPoint presentation (`DOC-20260924-WA0007.pptx`).<br>• Structured UML diagrams, flowcharts, and live interactive UI demo. |
| **MSE TOTAL** | **50 / 30** | **Target Grade: 30 / 30** |

---

## 2. End-Semester Exam (ESE — Scaled to 70 Marks)

| Column & Criterion | Max Marks | Project Evidence in DevCollab Pro |
|---|:---:|---|
| **Technical Complexity, Implementation & Innovation** | **30** | • 5 GoF Design Patterns (Strategy, Visitor, Factory, Observer, Singleton).<br>• Max-Heap leaderboard, Myers Diff delta compression, AVL tree rotation recording, Dijkstra shortest path.<br>• 9-table 3NF schema, 5 reporting views, and automated pytest test suites. |
| **Cost Effectiveness & Resource Utilization** | **15** | • Delta storage reduces database disk space by >60% compared to full snapshots.<br>• Asynchronous submission queue prevents expensive cloud VM over-provisioning. |
| **Environmental Relevance, Sustainability & Impact** | **15** | • Energy-efficient software design through empirical Big-O profiling.<br>• Significant reduction in server disk I/O and carbon footprint. |
| **Teamwork & Project Management** | **15** | • Balanced commit history, merged GitHub Pull Requests, and collaboration metrics. |
| **Reporting & Demonstration** | **25** | • Live interactive web dashboard demonstrating AST inspection, Big-O fitting, and live heap rankings.<br>• Comprehensive documentation and engineering methodology. |
| **ESE TOTAL** | **100 / 70** | **Target Grade: 70 / 70** |

---

## 3. Mandatory Compliance Fields

### Technology Readiness Level (TRL)
* **Assessed Level:** **TRL 4 / TRL 5**
* **Justification:** Component and system validation in a laboratory/simulated environment. `CodeVault`, `CodeSentry`, and `AlgoPro` operate seamlessly together in an integrated pipeline processing real source code and outputting verified scores.

### UN Sustainable Development Goals (SDGs)
* **SDG (Y/N):** **Y**
* **Target SDGs:**
  1. **SDG 4 (Quality Education — Target 4.4):** Imparts educational insights (cyclomatic complexity, Big-O profiling, explainable grading) back to students instead of opaque pass/fail errors.
  2. **SDG 9 (Industry, Innovation, and Infrastructure — Target 9.5):** Enhances software engineering assessment tooling and automated developer review pipelines.
  3. **SDG 8 (Decent Work and Economic Growth — Target 8.2):** Promotes meritocratic, fair, and unbiased assessment of developer skills and individual team contributions.
  4. **SDG 12 (Responsible Consumption & Production):** Fosters Green IT and sustainable cloud storage through algorithmic efficiency and delta compression.
