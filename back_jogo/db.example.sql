CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nickname VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE player_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    damage FLOAT DEFAULT 1.0,
    gold INT DEFAULT 0,
    gold_per_second INT DEFAULT 0,
    floor INT DEFAULT 1,
    dash_unlocked BOOLEAN DEFAULT FALSE,
    movespeed FLOAT DEFAULT 1.0,
    dps FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE achievements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  condition_text VARCHAR(255) NOT NULL,
  icon_path VARCHAR(255) NOT NULL,
  reward INT DEFAULT 0
);

CREATE TABLE user_achievements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  achievement_id INT NOT NULL,
  unlocked BOOLEAN DEFAULT FALSE,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (achievement_id) REFERENCES achievements(id),
  UNIQUE KEY (user_id, achievement_id)
);

INSERT INTO achievements (name, description, condition_text, icon_path, reward) VALUES
('First Steps', 'Get to the third floor', 'player.floor >= 3', 'assets/achievements/first_steps.png', 100),
('Rich', 'Get 1000 gold', 'player.gold >= 1000', 'assets/achievements/rich.png', 500),
('Hunter', 'Defeat 50 enemies', 'enemy_manager.enemies_defeated >= 50', 'assets/achievements/hunter.png', 1000);