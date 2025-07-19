from agents import Agent, Runner, trace, gen_trace_id, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from search_agent import search_agent
from planner_agent import planner_agent
from writer_agent import writer_agent
from email_agent import email_agent
from dotenv import load_dotenv
import os

# Convert agents to tools
planner_tool = planner_agent.as_tool(tool_name="planner_agent", tool_description="Create search strategy")
search_tool = search_agent.as_tool(tool_name="search_agent", tool_description="Execute web searches and summarises results")
writer_tool = writer_agent.as_tool(tool_name="writer_agent", tool_description="Generate research report")
email_tool = email_agent.as_tool(tool_name="email_agent", tool_description="Email final report")

# Research Manager Model

load_dotenv(override=True)
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
anthropic_client = AsyncOpenAI(base_url=ANTHROPIC_BASE_URL, api_key=anthropic_api_key)
claude_model = OpenAIChatCompletionsModel(model="claude-3-5-sonnet-20240620", openai_client=anthropic_client)


# Research Manager Agent
INSTRUCTIONS = (
    """You are a research reviewer responsible for co-ordinating the research process and producing high-quality research reports for organisations.

    You have access to these tools:
    - planner_tool: Create search strategy
    - search_tool: Execute web searches and summarises results
    - writer_tool: Generate research report
    - email_tool: Send final report

    Your workflow:
    1. Use the available tools to create a research report.
    2. Ensure that you provide the company, industry, and user query to the planner tool, search tool, and writer tool.
    3. Review quality at each step.
    4. Re-engage with tools if quality is insufficient (max 3 iterations). Be intelligent about when to re-run specific tools vs continuing forward. Always ensure high quality before finalising.
    5. Send the full final report in markdown format to the email tool.

    CRITICAL OUTPUT REQUIREMENTS:
    - Your FINAL response must contain ONLY the complete markdown report
    - Do NOT include any commentary, summaries, explanations, or process descriptions
    - Do NOT mention the steps you followed or tools you used
    - Do NOT add phrases like "Here is the report" or "I have completed the research"
    - The response should start directly with the markdown content (e.g., "# Research Report Title")
    - End your response immediately after the final markdown content

    INTERNAL PROCESS (do not include in final output):
    - Conduct all tool interactions and quality reviews silently
    - Only return the final markdown report to the user interface
    - Ensure the report is comprehensive and standalone
    """
)

research_manager_agent = Agent(
    name="Research Manager",
    instructions=INSTRUCTIONS,
    model=claude_model,
    tools=[planner_tool, search_tool, writer_tool, email_tool]
)

async def run_research(company: str, industry: str, query: str):
    trace_id = gen_trace_id()
    with trace("Research trace", trace_id=trace_id):
        print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
        
        yield "Research underway..."
        
        result = await Runner.run(
            research_manager_agent, 
            f"Research: Company: {company} | Industry: {industry} | Query: {query}"
        )
    yield result.final_output