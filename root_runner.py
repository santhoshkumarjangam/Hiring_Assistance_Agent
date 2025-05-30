from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai.types import Content,Part
from hiring_assisting_agent.agent import root_agent
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def create_session(session_service, user_id):
    session = await session_service.create_session(app_name="MyApp", user_id=user_id)
    return session

async def run_agent(runner, session, user_id, user_input):
    
    content = Content(parts=[Part(text=user_input)], role="user")

    events = runner.run_async(user_id=user_id, session_id=session.id, new_message=content)

    async for event in events:
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                print("Agent Response:", final_response)


if __name__ == "__main__":

    user_id = input("please enter your user_id:")

    session_service = DatabaseSessionService(db_url='sqlite:///./sessions.db')
    session = asyncio.run(create_session(session_service, user_id))
    runner = Runner(app_name="MyApp", agent=root_agent, session_service=session_service)

    while True:
        user_input = input("User:")

        if user_input == "exit":
            break

        asyncio.run(run_agent(runner, session, user_id, user_input))