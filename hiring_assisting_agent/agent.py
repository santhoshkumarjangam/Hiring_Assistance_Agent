from google.adk.agents import Agent

from .subagents.resume_shortlisting_agent.agent import resume_shortlisting_agent

hiring_assistant_agent = Agent(
    model='gemini-2.0-flash-001',
    name='hiring_assistant_agent',
    description='An intelligent assistant to help with resume shortlisting and hiring tasks.',
    instruction=(
        """
        You are an intelligent hiring assistant responsible for automating the hiring process.
        First, understand what the user is asking without requesting clarification.
        Then, based on the request, delegate it to the most suitable sub-agent available.
        Use reasoning and understanding to pick the best one.
        If the user sends a greeting or unrelated message, respond politely without invoking a sub-agent.
        Once the intent is clear, delegate to the correct sub-agent.
        Sub-agents handle tasks completely—assume they return a full response.
        """
    ),
    sub_agents=[resume_shortlisting_agent]
)

root_agent = hiring_assistant_agent