--
-- Mock data for AIBugReport
-- Using database: aibugrepot_db
--

USE `aibugrepot_db`;

-- Insert sample projects
INSERT INTO `projects` (`name`) VALUES
  ('WebApp'),
  ('API Service'),
  ('MobileApp');

-- Insert sample bug reports
INSERT INTO `bug_reports` (`title`, `description`, `category`, `severity`, `status`, `project_id`) VALUES
  ('Login button not responding',
   'When clicking the login button on the web interface, nothing happens.',
   'UI', 'Medium', 'open', 1),
  ('API returns 500 on GET /users',
   'A 500 Internal Server Error is returned when fetching list of users.',
   'Backend', 'High', 'open', 2),
  ('App crashes on startup',
   'Mobile app crashes immediately on Android devices running API level < 21.',
   'Stability', 'Critical', 'open', 3);

-- Insert sample attachments
INSERT INTO `attachments` (`bug_id`, `file_name`, `ipfs_hash`, `url`) VALUES
  (1, 'screenshot_login.png', 'QmHashExample1', 'https://gateway.pinata.cloud/ipfs/QmHashExample1'),
  (2, 'error_log.txt',       'QmHashExample2', 'https://gateway.pinata.cloud/ipfs/QmHashExample2'),
  (3, 'crash_report.log',    'QmHashExample3', 'https://gateway.pinata.cloud/ipfs/QmHashExample3');