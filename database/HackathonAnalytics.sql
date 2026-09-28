-- =====================================================================
-- DevCollab Pro: Hackathon Analytics Relational Database Schema
-- 3NF Normalized Schema (9 Tables) + 5 Analytical Reporting Views
-- Vishwakarma Institute of Technology, Pune - Group SY06
-- =====================================================================

DROP DATABASE IF EXISTS DevCollabProDB;
CREATE DATABASE DevCollabProDB;
USE DevCollabProDB;

-- 1. Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('STUDENT', 'JUDGE', 'ORGANIZER') DEFAULT 'STUDENT',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Teams Table
CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    leader_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (leader_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- 3. Team Members Table (Associative Entity in 3NF)
CREATE TABLE team_members (
    membership_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    user_id INT NOT NULL,
    roll_number VARCHAR(20) NOT NULL,
    role_description VARCHAR(100),
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
    UNIQUE KEY uq_team_user (team_id, user_id)
);

-- 4. Contests Table
CREATE TABLE contests (
    contest_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    organizer_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- 5. Problems Table
CREATE TABLE problems (
    problem_id INT AUTO_INCREMENT PRIMARY KEY,
    contest_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    time_limit_ms INT DEFAULT 2000,
    FOREIGN KEY (contest_id) REFERENCES contests(contest_id) ON DELETE CASCADE
);

-- 6. Submissions Table
CREATE TABLE submissions (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    contest_id INT NOT NULL,
    team_id INT NOT NULL,
    language VARCHAR(20) DEFAULT 'python',
    code_content MEDIUMTEXT NOT NULL,
    status ENUM('PENDING', 'QUEUED', 'EVALUATED', 'ERROR') DEFAULT 'PENDING',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contest_id) REFERENCES contests(contest_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);

-- 7. Evaluation Scores Table (1-to-1 with Submissions)
CREATE TABLE evaluation_scores (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    submission_id INT NOT NULL UNIQUE,
    correctness_score DECIMAL(5,2) DEFAULT 0.00,
    code_quality_score DECIMAL(5,2) DEFAULT 0.00,
    performance_score DECIMAL(5,2) DEFAULT 0.00,
    security_score DECIMAL(5,2) DEFAULT 0.00,
    innovation_score DECIMAL(5,2) DEFAULT 0.00,
    collaboration_score DECIMAL(5,2) DEFAULT 0.00,
    final_composite_score DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id) ON DELETE CASCADE
);

-- 8. Leaderboard Entries Table
CREATE TABLE leaderboard_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    contest_id INT NOT NULL,
    team_id INT NOT NULL,
    `rank` INT NOT NULL,
    total_score DECIMAL(5,2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (contest_id) REFERENCES contests(contest_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);

-- 9. Git Repositories Table (CodeVault metadata)
CREATE TABLE git_repositories (
    repo_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT NOT NULL,
    repo_name VARCHAR(100) NOT NULL,
    total_commits INT DEFAULT 0,
    storage_saved_pct DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);

-- =====================================================================
-- 5 Analytical Reporting Views
-- =====================================================================

-- View 1: Team Performance Summary View
CREATE VIEW vw_team_performance_summary AS
SELECT 
    t.team_id,
    t.team_name,
    COUNT(s.submission_id) AS total_submissions,
    ROUND(AVG(es.final_composite_score), 2) AS avg_score,
    MAX(es.final_composite_score) AS best_score
FROM teams t
LEFT JOIN submissions s ON t.team_id = s.team_id
LEFT JOIN evaluation_scores es ON s.submission_id = es.submission_id
GROUP BY t.team_id, t.team_name;

-- View 2: Live Leaderboard Standings View
CREATE VIEW vw_leaderboard_standings AS
SELECT 
    le.`rank`,
    t.team_name,
    c.title AS contest_name,
    le.total_score,
    le.last_updated
FROM leaderboard_entries le
JOIN teams t ON le.team_id = t.team_id
JOIN contests c ON le.contest_id = c.contest_id
ORDER BY le.`rank` ASC;

-- View 3: Code Quality & Security Audit View
CREATE VIEW vw_code_quality_audit AS
SELECT 
    s.submission_id,
    t.team_name,
    es.code_quality_score,
    es.security_score,
    es.performance_score
FROM submissions s
JOIN teams t ON s.team_id = t.team_id
JOIN evaluation_scores es ON s.submission_id = es.submission_id
WHERE es.security_score < 70 OR es.code_quality_score < 70;

-- View 4: Submission Throughput & Bottleneck View
CREATE VIEW vw_submission_bottlenecks AS
SELECT 
    DATE(submitted_at) AS submission_date,
    HOUR(submitted_at) AS submission_hour,
    COUNT(submission_id) AS submissions_count,
    SUM(CASE WHEN status = 'ERROR' THEN 1 ELSE 0 END) AS error_count
FROM submissions
GROUP BY DATE(submitted_at), HOUR(submitted_at);

-- View 5: Student Member Contribution View
CREATE VIEW vw_student_contribution_breakdown AS
SELECT 
    t.team_name,
    u.full_name AS student_name,
    tm.roll_number,
    tm.role_description,
    gr.total_commits,
    gr.storage_saved_pct
FROM team_members tm
JOIN teams t ON tm.team_id = t.team_id
JOIN users u ON tm.user_id = u.user_id
LEFT JOIN git_repositories gr ON t.team_id = gr.team_id;

-- =====================================================================
-- Seed Data: VIT Pune Group SY06
-- =====================================================================
INSERT INTO users (username, email, full_name, role) VALUES
('kunal_r', 'kunal@vit.edu', 'Kunal Sanjay Rahangdale', 'STUDENT'),
('shantanu_p', 'shantanu@vit.edu', 'Shantanu Shokin Patil', 'STUDENT'),
('jagdish_p', 'jagdish@vit.edu', 'Jagdish Prakash Patole', 'STUDENT'),
('nagesh_p', 'nagesh@vit.edu', 'Nagesh Kishor Patthe', 'STUDENT'),
('dr_yogesh', 'yogesh.sharma@vit.edu', 'Dr. Yogesh Sharma', 'JUDGE');

INSERT INTO teams (team_name, leader_id) VALUES
('Group SY06 (DevCollab Pro)', 1);

INSERT INTO team_members (team_id, user_id, roll_number, role_description) VALUES
(1, 1, '50', 'Team Lead & Architecture'),
(1, 2, '04', 'Contest & Upload Modules'),
(1, 3, '10', 'Evaluation & Testing'),
(1, 4, '11', 'Leaderboard, Heap Ranking & Analytics');

INSERT INTO contests (title, organizer_id) VALUES
('VIT EDI National Hackathon 2026', 5);

INSERT INTO git_repositories (team_id, repo_name, total_commits, storage_saved_pct) VALUES
(1, 'DevCollab-Pro', 24, 64.8);
