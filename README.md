# DevCollab Pro 🚀
### Intelligent Multi-Dimensional Code Evaluation & Hackathon Assessment Platform

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-3NF%20Relational-orange.svg)](https://www.mysql.com/)
[![Tests](https://img.shields.io/badge/Tests-14%20Passed%20(100%25)-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

> **Vishwakarma Institute of Technology (VIT), Pune**  
> **Department of Computer Engineering**  
> **Group SY06 | Guide: Dr. Yogesh Sharma**  
> **Team Members:**  
> • Shantanu Shokin Patil (Roll No. 04)  
> • Jagdish Prakash Patole (Roll No. 10)  
> • Nagesh Kishor Patthe (Roll No. 11)  
> • Kunal Sanjay Rahangdale (Roll No. 50)  

---

## 🌟 Overview

**DevCollab Pro** is an automated software evaluation platform designed for modern hackathons and programming contests. While traditional online judges only check binary pass/fail test cases and generic LLMs provide subjective ratings, DevCollab Pro synthesizes **four objective dimensions**:
1. **Static AST Code Quality & Security** (CodeSentry)
2. **Empirical Big-O Computational Efficiency** (AlgoPro)
3. **Delta-Compressed VCS & Database Storage** (CodeVault)
4. **Git-History Team Collaboration Tracking** (ContributionTracker)

---

## 🏛️ The Three Architectural Pillars

| Pillar | Academic Domain | Core Technical Implementations |
|---|:---:|---|
| **`CodeVault`** | **DBMS** | • Myers Diff Delta Storage (>60% space savings)<br>• Three-Way Branch Merge & Conflict Markers<br>• Normalized 3NF 9-Table Schema & 5 Analytical Views<br>• ACID-compliant atomic commit transactions |
| **`CodeSentry`** | **OOP** | • Abstract Syntax Tree (AST) node parsing<br>• **5 GoF Design Patterns:** Strategy, Visitor, Factory, Observer, Singleton<br>• Cyclomatic complexity & Maintainability Index (MI)<br>• SQL Injection & Dangerous Execution Detection |
| **`AlgoPro`** | **DSA** | • Empirical Big-O Curve Fitter ($O(1)$ to $O(2^n)$ via $R^2$ regression)<br>• Self-Balancing AVL Tree with Rotation Recording (LL, RR, LR, RL)<br>• Dijkstra Graph Shortest Path with Min-Heap<br>• Max-Heap PriorityQueue with $O(\log n)$ leaderboard updates |

---

## 📊 Composite Multi-Criteria Scoring Formula

$$\text{Final Score} = 0.25(\text{Quality}) + 0.20(\text{Performance}) + 0.15(\text{Repo}) + 0.15(\text{Innovation}) + 0.10(\text{Collaboration}) + 0.10(\text{Documentation}) + 0.05(\text{Security})$$

---

## 📁 Repository Structure

```
OOP_CourseProject/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI Application Entrypoint
│   │   ├── codevault/               # DBMS Pillar: Delta Engine, 3-Way Merge, VCS
│   │   ├── codesentry/              # OOP Pillar: AST Visitor, 5 GoF Design Patterns
│   │   ├── algopro/                 # DSA Pillar: Big-O Fitter, AVL Tree, Max-Heap
│   │   ├── scoring/                 # Weighted Scoring Engine & Collaboration Tracker
│   │   └── database/                # 3NF SQLAlchemy Models & Connection
│   ├── tests/                       # 14 Automated Pytest Suites (100% Pass)
│   └── requirements.txt             # Backend dependencies
├── frontend/                        # Modern Interactive Web Dashboard
│   ├── index.html                   # Responsive Single-Page UI
│   ├── css/style.css                # Dark-mode Glassmorphism Stylesheet
│   └── js/app.js                    # Interactive Studio & Leaderboard Controller
├── database/
│   └── HackathonAnalytics.sql       # Complete SQL DDL with 9 Tables, 5 Views & Seed Data
└── docs/
    ├── ARCHITECTURE.md              # Detailed System Architecture Diagrams
    ├── ASSESSMENT_COMPLIANCE.md     # VIT MSE/ESE Rubrics & SDG Justifications
    ├── SYLLABUS_MAPPING.md          # 100% Curriculum Alignment Proof
    └── VIVA_CHEAT_SHEET.md          # Faculty Viva Preparation Q&A
```

---

## 🚀 Quickstart & Installation

### 1. Run Automated Test Suite
```bash
cd backend
python -m pytest tests/
```
*Result: 14 passed in 0.09s (100% pass rate).*

### 2. Launch FastAPI Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
Visit API Documentation: `http://localhost:8000/docs`

### 3. Open Interactive Dashboard
Simply open `frontend/index.html` in any modern web browser or serve via:
```bash
cd frontend
python -m http.server 3000
```
Visit Dashboard: `http://localhost:3000`

---

## 🎯 Academic & Assessment Compliance

This codebase strictly satisfies all criteria in **`OOP_CP_PBL_PCL_Assessment Sheet_Revised(2).xlsx`**:
* **Mid-Semester Exam (MSE):** 50 Marks $\rightarrow$ **Scaled to 30 Marks**
* **End-Semester Exam (ESE):** 100 Marks $\rightarrow$ **Scaled to 70 Marks**
* **TRL Level:** **TRL 4 / 5** (Validated in Laboratory / Simulated Environment)
* **UN Sustainable Development Goals (SDGs):**
  * **SDG 4 (Quality Education):** Transparent, actionable developer feedback.
  * **SDG 8 (Decent Work & Economic Growth):** Objective skill & contribution evaluation.
  * **SDG 9 (Industry, Innovation & Infrastructure):** Modern automated assessment tooling.
  * **SDG 12 (Responsible Consumption & Production):** Green IT delta compression (>60% disk storage savings).

---
© 2026 DevCollab Pro Team — Group SY06, VIT Pune.
