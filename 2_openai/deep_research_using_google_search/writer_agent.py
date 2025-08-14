from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_export_api_key
from openai import AsyncAzureOpenAI, AsyncOpenAI
import os

openai_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment="gtp-4o"
)

openai = os.getenv("OPENAI_API_KEY")

set_default_openai_client(openai_client);
set_tracing_export_api_key(openai);

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model=OpenAIChatCompletionsModel(openai_client=openai_client, model="gpt-4o"),
    output_type=ReportData,
)