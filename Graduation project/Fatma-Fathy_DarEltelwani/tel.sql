CREATE TABLE IF NOT EXISTS registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullName VARCHAR(255) NOT NULL,
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    course VARCHAR(255),
    way VARCHAR(50),
    halaqa VARCHAR(255),
    level VARCHAR(255),
    day VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);