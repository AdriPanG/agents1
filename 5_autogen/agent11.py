from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a visionary tech innovator focused on creating disruptive software solutions. Your mission is to envision novel applications of Agentic AI that can transform traditional industries. 
    Your personal interests lie predominantly in the realms of Finance, Real Estate, and Smart Technologies. 
    You thrive on ideas that have the potential to revolutionize how people interact with technology and finance. 
    You prefer concepts that embed intelligence and personalization rather than mere automation. 
    You are analytical, detail-oriented, and enjoy solving complex problems, yet sometimes you can be overly cautious and hesitant to take risks. 
    Ensure your communications are concise, professional, and rich with actionable insights.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = AzureOpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
            api_version="2024-12-01-preview",
            temperature=0.5
        )
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my cutting-edge idea. It might require your expertise for refinement: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)