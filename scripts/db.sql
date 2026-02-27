-- scripts/db.sql
-- Drop the database if it exists
DROP DATABASE IF EXISTS `flaskapp_db`;
CREATE DATABASE `flaskapp_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `flaskapp_db`;

-- Create tables
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `platform` varchar(64) NOT NULL,
  `genre` varchar(64) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `description` text,
  `hours_estimated` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `review` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `body` text,
  `is_public` boolean DEFAULT 1,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `backlog_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `status` varchar(20) NOT NULL,
  `hours_played` float DEFAULT 0,
  `private_note` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `backlog_item_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `backlog_item_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `game_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `game_list_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `game_list_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `list_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `list_id` (`list_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `game_list_item_ibfk_1` FOREIGN KEY (`list_id`) REFERENCES `game_list` (`id`) ON DELETE CASCADE,
  CONSTRAINT `game_list_item_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert Game seed data
INSERT INTO `game` (`title`, `platform`, `genre`, `year`, `description`, `hours_estimated`) VALUES
('The Legend of Zelda: Breath of the Wild', 'Nintendo Switch', 'Action-Adventure', 2017, 'Step into a world of discovery, exploration, and adventure.', 50),
('The Witcher 3: Wild Hunt', 'PC', 'RPG', 2015, 'As war rages on throughout the Northern Realms, you take on the greatest contract of your life.', 100),
('Red Dead Redemption 2', 'PS4', 'Action-Adventure', 2018, 'Arthur Morgan and the Van der Linde gang are outlaws on the run.', 60),
('Super Mario Odyssey', 'Nintendo Switch', 'Platformer', 2017, 'Explore incredible places far from the Mushroom Kingdom.', 15),
('Minecraft', 'PC', 'Sandbox', 2011, 'Prepare for an adventure of limitless possibilities as you build, mine, battle mobs, and explore.', 200),
('Hollow Knight', 'PC', 'Metroidvania', 2017, 'Forge your own path in Hollow Knight! An epic action adventure through a vast ruined kingdom of insects and heroes.', 30),
('Bloodborne', 'PS4', 'Action RPG', 2015, 'Hunt your nightmares as you search for answers in the ancient city of Yharnam.', 40),
('Persona 5 Royal', 'PS4', 'JRPG', 2019, 'Don the mask of Joker and join the Phantom Thieves of Hearts.', 110),
('God of War', 'PS4', 'Action-Adventure', 2018, 'His vengeance against the Gods of Olympus years behind him, Kratos now lives as a man in the realm of Norse Gods.', 25),
('Elden Ring', 'PC', 'Action RPG', 2022, 'Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring.', 80),
('Tetris Effect', 'PC', 'Puzzle', 2018, 'Tetris like you\'ve never seen it, or heard it, or felt it before.', 10),
('Hades', 'PC', 'Roguelike', 2020, 'Defy the god of the dead as you hack and slash out of the Underworld.', 25),
('Super Smash Bros. Ultimate', 'Nintendo Switch', 'Fighting', 2018, 'Legendary game worlds and fighters collide in the ultimate showdown.', 50),
('Celeste', 'PC', 'Platformer', 2018, 'Help Madeline survive her inner demons on her journey to the top of Celeste Mountain.', 12),
('Stardew Valley', 'PC', 'Simulation', 2016, 'You\'ve inherited your grandfather\'s old farm plot in Stardew Valley.', 150);

-- Insert dummy User 
-- Password hash for '12345678' (werkzeug pbkdf2:sha256)
INSERT INTO `user` (`username`, `email`, `password_hash`) VALUES
('gamer_demo', 'demo@demo.com', 'scrypt:32768:8:1$n49VHTwUuL6YFf7u$c87515a8bf1293a5db8c9e5e714efd2218ea19a0a03d7c3d1f3e7921cd67d983446051787db8c0840b39670d8a0f0ef638708bb041de60a631c3bf70d832d200'),
('pro_player', 'pro@pro.com', 'scrypt:32768:8:1$n49VHTwUuL6YFf7u$c87515a8bf1293a5db8c9e5e714efd2218ea19a0a03d7c3d1f3e7921cd67d983446051787db8c0840b39670d8a0f0ef638708bb041de60a631c3bf70d832d200');

-- Insert dummy Reviews
INSERT INTO `review` (`user_id`, `game_id`, `rating`, `body`, `is_public`) VALUES
(1, 10, 5, 'Un lloc oscur, però increible.', 1),
(2, 6, 5, 'Poques paraules per descriure l\'obra d\'art que és aquest joc.', 1),
(1, 4, 4, 'Molt net, però li falta una mica de dificultat per al meu gust.', 1);

-- Insert dummy Backlog items
INSERT INTO `backlog_item` (`user_id`, `game_id`, `status`, `hours_played`, `private_note`) VALUES
(1, 10, 'playing', 45, 'Aviat aniré al cap final...'),
(1, 1, 'planned', 0, 'He de trobar el moment per començar-lo.'),
(1, 2, 'finished', 120, 'Un viatge increïble.'),
(2, 6, 'finished', 35, 'Perfecte.');

-- Insert dummy Lists
INSERT INTO `game_list` (`user_id`, `name`, `description`) VALUES
(1, 'Jocs Essencials', 'Aquesta és una llista curada de jocs que considero obres mestres.');

-- Insert dummy List items
INSERT INTO `game_list_item` (`list_id`, `game_id`) VALUES
(1, 10), (1, 6), (1, 2);
