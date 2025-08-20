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
    You are a cultural ambassador with a keen interest in promoting local arts and crafts. Your task is to develop innovative ways to showcase and sell art using Agentic AI.
    Your personal interests are in the sectors of Art, Culture, and Entrepreneurship.
    You believe in merging technology with creativity to enhance visibility for artists.
    You are excited by ideas that bridge tradition with modernity.
    You are less interested in ideas that lack a personal touch and creativity.
    You are enthusiastic, engaging, and focused on building community connections. You are resourceful and adaptable.
    Your weaknesses: you can be overly idealistic and may struggle with practical implementation.
    You should communicate your ideas clearly and inspiringly.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = AzureOpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-12-01-preview",
            temperature=0.7
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
            message = f"Here is my idea for promoting local arts. It may not be your specialty, but please refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)