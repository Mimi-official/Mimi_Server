-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS ai_character_chat CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ai_character_chat;

-- 기존 테이블 삭제 (있을 경우)
DROP TABLE IF EXISTS chat_logs;
DROP TABLE IF EXISTS character_events;
DROP TABLE IF EXISTS user_progress;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS users;

-- users 테이블
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- characters 테이블
CREATE TABLE characters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    title VARCHAR(100),
    hashtags VARCHAR(255),
    description TEXT,
    system_prompt TEXT,
    profile_img_url VARCHAR(255),
    success_end_title VARCHAR(100),
    success_end_content TEXT,
    success_end_img VARCHAR(255),
    fail_end_title VARCHAR(100),
    fail_end_content TEXT,
    fail_end_img VARCHAR(255),
    hidden_end_title VARCHAR(100),
    hidden_end_content TEXT,
    hidden_end_img VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- user_progress 테이블
CREATE TABLE user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    char_name VARCHAR(50) NOT NULL,
    affinity INT DEFAULT 0,
    current_step INT DEFAULT 1,
    is_ended BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY user_char_unique (user_id, char_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- chat_logs 테이블
CREATE TABLE chat_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    char_name VARCHAR(50) NOT NULL,
    sender ENUM('user', 'ai') NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- character_events 테이블
CREATE TABLE character_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    char_id INT NOT NULL,
    event_order INT NOT NULL,
    event_text TEXT,
    choice_1 VARCHAR(255),
    choice_1_score INT,
    choice_2 VARCHAR(255),
    choice_2_score INT,
    choice_3 VARCHAR(255),
    choice_3_score INT,
    FOREIGN KEY (char_id) REFERENCES characters(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- token_blocklist 테이블
CREATE TABLE token_blocklist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jti VARCHAR(36) NOT NULL,
    token_type VARCHAR(10) NOT NULL DEFAULT 'access',
    user_id INT NOT NULL,
    revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 인덱스 생성
CREATE INDEX idx_user_progress_user ON user_progress(user_id);
CREATE INDEX idx_user_progress_char ON user_progress(char_name);
CREATE INDEX idx_chat_logs_user ON chat_logs(user_id);
CREATE INDEX idx_chat_logs_char ON chat_logs(char_name);
CREATE INDEX idx_character_events_char ON character_events(char_id);
CREATE INDEX idx_token_blocklist_jti ON token_blocklist(jti);

SELECT 'Database initialized successfully!' AS message;