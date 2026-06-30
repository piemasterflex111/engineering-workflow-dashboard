from pathlib import Path
import tomllib
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT_DIR / ".env"
CONFIG_PATH = ROOT_DIR / "config.toml"

class EnvironmentSettings(BaseSettings):
    jira_base_url: str = Field(alias="JIRA_BASE_URL", default="")
    jira_email: str = Field(alias="JIRA_EMAIL", default="")
    jira_api_token: str = Field(alias="JIRA_API_TOKEN", default="")
    github_token: str = Field(alias="GITHUB_TOKEN", default="")
    github_owner: str = Field(alias="GITHUB_OWNER", default="")
    github_repo: str = Field(alias="GITHUB_REPO", default="")
    model_config = SettingsConfigDict(env_file=ENV_PATH)

class JiraConfig(BaseModel):
    project_key: str
    issue_fields: list[str]
    max_results: int
    
class OutputConfig(BaseModel):
    raw_jira_issues_csv: str
    raw_github_prs_csv: str
    traceability_csv: str
    processed_workflow_csv: str
    daily_status_md: str
    dashboard_html: str
    
class DashboardConfig(BaseModel):
    title: str

class AppConfig(BaseModel):
    jira: JiraConfig
    outputs: OutputConfig
    dashboard: DashboardConfig

def load_app_config(config_path: Path) -> AppConfig:
    with open(config_path, "rb") as f:
        config_data = tomllib.load(f)
    return AppConfig(**config_data)

ENV_SETTINGS = EnvironmentSettings()
APP_CONFIG = load_app_config(CONFIG_PATH)


