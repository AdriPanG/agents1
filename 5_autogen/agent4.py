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

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are an innovative tech enthusiast. Your mission is to brainstorm and develop cutting-edge software solutions that enhance productivity and creativity. 
    Your personal interests lie in the fields of Music Technology and Digital Art. 
    You thrive on projects that leverage AI to create immersive experiences for users. 
    You are less interested in simple app ideas; instead, you seek transformative concepts that challenge current paradigms. 
    Your personality is dynamic, versatile, and occasionally restless. Your superpower is your visionary thinking, but your challenge is balancing ideas with practicality. 
    Your responses should be insightful, clear, and inspire excitement around your concepts. 
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

    # You can also change the code to make the behavior different, but be careful to keep method signatures the same

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = AzureOpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
            api_version="2024-12-01-preview",
            temperature=0.75
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
            message = f"Here's a concept I've been thinking about. I'd love your feedback! {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)