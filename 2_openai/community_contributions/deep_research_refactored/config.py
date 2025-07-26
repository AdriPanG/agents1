"""
Configuration settings for the Deep Research Agent System
"""
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class AgentConfig:
    """Configuration for agent settings"""
    model_name: str = "gpt-4o-mini"
    search_context_size: str = "low"
    max_search_results: int = 3
    report_min_words: int = 1000
    report_max_words: int = 5000


@dataclass
class FileConfig:
    """Configuration for file paths and settings"""
    email_output_file: str = "sent_emails_deep_research.txt"
    log_file: str = "deep_research.log"
    reports_dir: str = "reports"


@dataclass
class SystemConfig:
    """System-wide configuration"""
    timeout_seconds: int = 300
    max_retries: int = 3
    enable_logging: bool = True
    log_level: str = "INFO"


class Config:
    """Main configuration class"""
    
    def __init__(self):
        self.agent = AgentConfig(
            model_name=os.getenv("AGENT_MODEL", "gpt-4o-mini"),
            search_context_size=os.getenv("SEARCH_CONTEXT_SIZE", "low"),
            max_search_results=int(os.getenv("MAX_SEARCH_RESULTS", "3")),
            report_min_words=int(os.getenv("REPORT_MIN_WORDS", "1000")),
            report_max_words=int(os.getenv("REPORT_MAX_WORDS", "5000"))
        )
        
        self.file = FileConfig(
            email_output_file=os.getenv("EMAIL_OUTPUT_FILE", "sent_emails_deep_research.txt"),
            log_file=os.getenv("LOG_FILE", "deep_research.log"),
            reports_dir=os.getenv("REPORTS_DIR", "reports")
        )
        
        self.system = SystemConfig(
            timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "300")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            enable_logging=os.getenv("ENABLE_LOGGING", "true").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )
    
    def create_directories(self):
        """Create necessary directories"""
        os.makedirs(self.file.reports_dir, exist_ok=True) 