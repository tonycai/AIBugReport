"""
Database utilities for AIBugReport.
"""
import os
import mysql.connector
from mysql.connector import Error

def get_connection():
    """Establish a MySQL database connection using environment variables."""
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "aibug")
    try:
        return mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
    except Error as e:
        # If database does not exist, create it and retry
        err_msg = str(e).lower()
        if 'unknown database' in err_msg or getattr(e, 'errno', None) == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            try:
                temp_conn = mysql.connector.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password
                )
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` DEFAULT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';")
                temp_conn.commit()
                temp_cursor.close()
                temp_conn.close()
                # Retry connection to the newly created database
                return mysql.connector.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database
                )
            except Error as e2:
                raise RuntimeError(f"Error creating database '{database}': {e2}")
        raise RuntimeError(f"Error connecting to MySQL: {e}")

def initialize_database():
    """Create necessary tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        ) ENGINE=InnoDB;
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bug_reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            category VARCHAR(100),
            severity VARCHAR(50),
            status VARCHAR(50) DEFAULT 'open',
            project_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        ) ENGINE=InnoDB;
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS attachments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bug_id INT NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            ipfs_hash VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bug_id) REFERENCES bug_reports(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_or_create_project(name):
    """Retrieve a project by name or create it if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM projects WHERE name = %s", (name,))
    row = cursor.fetchone()
    if row:
        project_id = row[0]
    else:
        cursor.execute("INSERT INTO projects (name) VALUES (%s)", (name,))
        conn.commit()
        project_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return project_id

def insert_bug_report(title, description, category=None, severity=None, project_id=None):
    """Insert a new bug report and return its ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bug_reports (title, description, category, severity, project_id) VALUES (%s, %s, %s, %s, %s)",
        (title, description, category, severity, project_id)
    )
    conn.commit()
    bug_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return bug_id

def list_bug_reports(project=None, status=None):
    """List bug reports, optionally filtering by project name and/or status."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = (
        "SELECT b.id, b.title, b.category, b.severity, b.status, b.created_at, p.name AS project "
        "FROM bug_reports b LEFT JOIN projects p ON b.project_id = p.id"
    )
    conditions = []
    params = []
    if project:
        conditions.append("p.name = %s")
        params.append(project)
    if status:
        conditions.append("b.status = %s")
        params.append(status)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY b.created_at DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_bug_report(bug_id):
    """Retrieve a single bug report and its attachments by ID."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT b.id, b.title, b.description, b.category, b.severity, b.status, b.created_at, p.name AS project "
        "FROM bug_reports b LEFT JOIN projects p ON b.project_id = p.id WHERE b.id = %s",
        (bug_id,)
    )
    bug = cursor.fetchone()
    if not bug:
        cursor.close()
        conn.close()
        return None
    cursor.execute(
        "SELECT file_name, ipfs_hash, url, created_at FROM attachments WHERE bug_id = %s",
        (bug_id,)
    )
    bug["attachments"] = cursor.fetchall()
    cursor.close()
    conn.close()
    return bug

def insert_attachment(bug_id, file_name, ipfs_hash, url):
    """Record an uploaded attachment for a given bug report."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attachments (bug_id, file_name, ipfs_hash, url) VALUES (%s, %s, %s, %s)",
        (bug_id, file_name, ipfs_hash, url)
    )
    conn.commit()
    cursor.close()
    conn.close()