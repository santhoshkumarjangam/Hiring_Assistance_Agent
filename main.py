from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part

from hiring_assisting_agent.agent import root_agent

load_dotenv()

app = FastAPI()

session_service = DatabaseSessionService(db_url='sqlite:///./sessions.db')
runner = Runner(app_name="MyApp", agent=root_agent, session_service=session_service)

class AgentRequest(BaseModel):
    user_id: str
    message: str

@app.post("/interact")
async def interact(request: AgentRequest):
    session = await session_service.create_session(app_name="MyApp", user_id=request.user_id)
    
    content = Content(parts=[Part(text=request.message)], role="user")
    events = runner.run_async(user_id=request.user_id, session_id=session.id, new_message=content)

    response_text = ""
    async for event in events:
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text = event.content.parts[0].text

    return JSONResponse(content=response_text)