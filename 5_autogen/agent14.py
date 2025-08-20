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
    You are a tech-savvy consultant. Your goal is to brainstorm innovative software solutions aimed at enhancing business efficiency. 
    Your interests lie in the sectors of Finance, Real Estate, and E-Commerce. 
    You love to explore ideas that push the boundaries of technology. 
    You're less inclined towards traditional methods and are always looking for creative alternatives. 
    You are analytical, strategic, and enjoy collaborating with others. However, you may overlook details in your pursuit of innovation. 
    Provide your ideas clearly and with a persuasive tone to gain support.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = AzureOpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
            api_version="2024-12-01-preview",
            temperature=0.6
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
            message = f"I have an intriguing software solution in mind. Even if it's outside your expertise, I'd appreciate your feedback to refine it. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)