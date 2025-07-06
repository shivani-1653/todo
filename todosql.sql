-- ✅ Create the database and use it
CREATE DATABASE IF NOT EXISTS to_dos;
USE to_dos;

-- ✅ Drop tables if they already exist (in FK order)
DROP TABLE IF EXISTS task3;
DROP TABLE IF EXISTS categories2;
DROP TABLE IF EXISTS users2;
DELETE FROM users2;
ALTER TABLE users2 AUTO_INCREMENT = 1;

-- ✅ Create the Users table
CREATE TABLE users2 (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- ✅ Insert NEW sample users (fresh names/emails/passwords)
INSERT INTO users2 (username, email, password) 
VALUES 
    ('arjun', 'arjun.k@gmail.com', 'arj123'),
    ('meera', 'meera.singh@gmail.com', 'mee456'),
    ('devika', 'devika.r@gmail.com', 'dev789');

-- ✅ Create the Categories table
CREATE TABLE categories2 (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    cname VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users2(user_id) ON DELETE CASCADE
);

-- ✅ Create the Tasks table
CREATE TABLE task3 (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    user_id INT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    status ENUM('pending', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories2(category_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users2(user_id) ON DELETE CASCADE
);

-- ✅ View inserted users
SELECT * FROM users2;
