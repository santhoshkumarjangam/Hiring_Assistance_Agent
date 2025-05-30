from google.adk.agents import Agent, SequentialAgent
from .parser_agent import parser_agent
from .skill_extractor_agent import skill_extractor_agent
from .skill_matcher_and_scorer_agent import skill_matcher_and_scorer_agent
from .report_generator_agent import report_generator_agent

def fetch_resume() -> dict :
    '''
    Extracts resume from DB and returns {raw_text}.
    '''
    import sqlite3
    import io
    import pdfplumber

    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, data FROM uploaded_files where id=2")
        resume = cursor.fetchone()

    resume_id, blob_data = resume

    with pdfplumber.open(io.BytesIO(blob_data)) as pdf:
            raw_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    
    return {"raw_text":raw_text}
    # return {"id": resume_id, "raw_text": raw_text}

def fetch_job_description() -> dict :
    '''
    Extracts Job Description from DB and returns {job_description}
    '''
    import sqlite3

    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT job_id, job_description FROM jobs  where job_id=2")
        JD = cursor.fetchone()

    job_description = JD[1]

    return {"job_description":job_description}

def fetch_resume_and_job_description() -> dict:
    '''
    Fetches resume and job description from the database
    returns a dictionary with keys raw_text and job_description
    '''

    raw_text = fetch_resume()
    job_description = fetch_job_description()

    return {**raw_text, **job_description}

sequential_pipeline = SequentialAgent(
    name='resume_shortlisting_flow',
    sub_agents=[
        parser_agent,
        skill_extractor_agent,
        skill_matcher_and_scorer_agent,
        report_generator_agent
    ]
)

resume_shortlisting_agent = Agent(
    name='resume_shortlisting_agent',
    model='gemini-2.0-flash-001',
    description='Handles end-to-end resume shortlisting',
    tools=[fetch_resume_and_job_description],
    sub_agents=[sequential_pipeline],
    instruction="""
    1. Use the `fetch_resume_and_job_description` tool to retrieve the resume and job description.
    2. Call the `sequential_pipeline` agent with the output.
    3. Wait for the flow to complete and return the final structured result.
    """
)