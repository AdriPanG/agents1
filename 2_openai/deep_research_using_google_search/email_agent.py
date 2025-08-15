import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool, OpenAIChatCompletionsModel, set_default_openai_client, set_tracing_export_api_key
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

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("adripang92@gmail.com") # put your verified sender here
    to_email = To("adrian.panadero@stratesys-ts.com") # put your recipient here
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=OpenAIChatCompletionsModel(openai_client=openai_client, model="gpt-4o"),
)
