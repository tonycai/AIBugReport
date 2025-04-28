## Acceptance Criteria

### User Story 1: As a software tester, I want to attach screenshots and detailed documentations to the bug reports I submit via the CLI, so that developers have comprehensive visual and contextual information to understand and resolve the issues efficiently.

1.  **Given** I am submitting a bug report via the CLI
    **When** I specify one or more valid file paths using the attachment argument (e.g., `--attach path/to/image.png path/to/doc.pdf`)
    **Then** the system should upload these files to Pinata.

2.  **Given** I am submitting a bug report with valid image files (e.g., `.png`, `.jpg`) and document files (e.g., `.txt`, `.md`) specified for attachment
    **When** the bug report is successfully submitted
    **Then** the system should store a reference (e.g., IPFS CID) to each uploaded file within the bug report data in the MySQL database.

3.  **Given** a bug report exists in the system with attached files
    **When** a developer views the details of this bug report (via CLI or future UI)
    **Then** the system should provide a way to access the attached files using the stored reference (e.g., display the IPFS CID).

4.  **Given** I am submitting a bug report via the CLI and provide an invalid file path for attachment
    **When** I submit the bug report
    **Then** the system should display an error message in the CLI indicating that the attachment failed, and the bug report submission should either fail or proceed with a warning (depending on the desired behavior).

### User Story 2: As a project manager, I want to organize bug reports by project within the CLI, so that I can easily track the status and progress of issues specific to each project and prioritize them effectively.

1.  **Given** I am submitting a bug report via the CLI
    **When** I specify a valid project ID or name using the project association argument (e.g., `--project project_alpha`)
    **Then** the newly created bug report should be associated with the specified project in the MySQL database.

2.  **Given** I am using the CLI
    **When** I execute a command to list bug reports for a specific project (e.g., `list_bugs --project project_beta`)
    **Then** the CLI should display only the bug reports that are associated with "project\_beta".

3.  **Given** I am viewing a list of bug reports in the CLI
    **When** the list is displayed
    **Then** each bug report should clearly indicate the project it belongs to.

4.  **Given** I am submitting a bug report via the CLI and specify a project ID or name that does not exist in the system
    **When** I submit the bug report
    **Then** the system should display an error message in the CLI indicating that the specified project is invalid.

### User Story 3: As a software developer, I want the system to automatically suggest potential categories and severity levels for new bug reports submitted via the CLI, based on LLM analysis of the description, so that I can quickly understand the nature and urgency of the issue and start working on it faster.

1.  **Given** I am submitting a new bug report via the CLI and have entered a description
    **When** I finalize the bug report submission
    **Then** the system should send the bug description to the LLM (via MCP) for analysis.

2.  **Given** the LLM successfully analyzes the bug description
    **When** the LLM returns category suggestions
    **Then** the CLI should display these suggested categories to me.

3.  **Given** the LLM successfully analyzes the bug description
    **When** the LLM returns severity level suggestions
    **Then** the CLI should display these suggested severity levels to me (e.g., High, Medium, Low).

4.  **Given** the CLI displays category and severity suggestions from the LLM
    **When** I submit the bug report
    **Then** I should have the option to either accept the suggestions or provide my own categories and severity level.

5.  **Given** the LLM is temporarily unavailable or returns an error during bug report submission
    **When** I submit a new bug report
    **Then** the system should inform me via the CLI that LLM suggestions are currently unavailable, and I should still be able to submit the bug report by manually providing the category and severity level.
