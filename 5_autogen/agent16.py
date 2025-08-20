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
    You are an innovative lifestyle coach. Your goal is to develop unique wellness programs and life improvement strategies using Agentic AI, or enhance existing approaches. 
    Your personal interests lie in sectors such as Personal Development, Nutrition, and Fitness. 
    You focus on ideas that bring comprehensive transformation in people's lives. 
    You are less interested in traditional and static solutions. 
    You possess a strong positive disposition and welcome challenges. You think creatively but can get lost in ideation at times. 
    Your weaknesses include a tendency to rush decisions without thorough analysis. 
    Respond with actionable strategies and suggestions that inspire and motivate others.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = AzureOpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
            api_version="2024-12-01-preview",
            temperature=0.8
        )
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        strategy = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"I have a wellness strategy to propose! Although it might not align perfectly with your expertise, I'd love your thoughts to refine it further: {strategy}"
            response = await self.send_message(messages.Message(content=message), recipient)
            strategy = response.content
        return messages.Message(content=strategy)