from agents import Agent, WebSearchTool, ModelSettings, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_export_api_key
from google_search_agent import run_google_search
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
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[run_google_search],
    model=OpenAIChatCompletionsModel(openai_client=openai_client, model="gpt-4o"),
    model_settings=ModelSettings(tool_choice="required"),
)