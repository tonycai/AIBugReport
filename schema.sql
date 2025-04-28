--
-- Schema definition for AIBugReport
-- Database: aibugrepot_db
--

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `aibugrepot_db`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE `aibugrepot_db`;

-- -----------------------------------------------------
-- Table `projects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projects` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table `bug_reports`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bug_reports` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `category` VARCHAR(100),
  `severity` VARCHAR(50),
  `status` VARCHAR(50) NOT NULL DEFAULT 'open',
  `project_id` INT,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`project_id`) REFERENCES `projects`(`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Table `attachments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attachments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `bug_id` INT NOT NULL,
  `file_name` VARCHAR(255) NOT NULL,
  `ipfs_hash` VARCHAR(255) NOT NULL,
  `url` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`bug_id`) REFERENCES `bug_reports`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;