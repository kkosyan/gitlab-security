# gitlab-security

Project provides an opportunity to automate check up and control on GitLab members access to projects. The project
includes two use-cases:
1. Extract-projects-members use-case upload all projects with access members into xlsx file for analysis
2. Project-members-comparison use-case compares expected and factual members to projects access
The project includes docker compose dev file for service testing.

To get started locally, you'll need:
1. Update databases credentials with settings/settings.toml and settings/.secrets.toml files
2. Install dependencies with pyproject.toml file
3. Run service with command`python cli.py extract-projects-members` to upload projects and members report
4. Run service with command`python cli.py project-members-comparison --file-name {expected_report_file_name}` to 
   start comparison between factual and expected reports
