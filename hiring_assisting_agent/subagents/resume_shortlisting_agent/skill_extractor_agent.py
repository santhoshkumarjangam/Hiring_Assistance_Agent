from google.adk.agents import Agent

skill_extractor_agent = Agent(
    model='gemini-2.0-flash-001',
    name='skill_extractor_agent',
    description='Extracts skills from the parsed resume.',
    instruction="""
        You are a skill extractor agent.

        The parsed resume is given below:
        {parsed_resume_text}

        Your responsibilities:

        PART 1: basic_information
        Basic structured data extracted from the resume:
        - `personal_info`: full name, location, email
        - `summary`: 2-3 sentence professional summary (from an actual section or inferred from the top)
        - `skills`: categorized skill list
        - `education`: list of degrees with institution and graduation year
        - `experience`: list of jobs (latest first) with job title, company, location, dates, and key bullet points
        - `certifications`: list of certifications with issuer and optional date
        ---

        PART 2: advanced_insights
        Use contextual understanding of the resume to identify the following insights:
        - learning_and_growth
        - exposure_to_multiple_domains
        - workplace_stability
        - leadership_and_decision_making
        - alignment_with_latest_technologies
        - debugging_or_reverse_engineering
        - problem_solving_skills
        - business_and_product_insight
        - innovation_or_ownership
        - initiative_and_continuous_learning
        - collaboration_and_communication

        Each insight should be a 2-3 sentence paragraph supported by evidence from the resume.
        ---

        output a neatly formatted json with the following sections:
            - basic_information
            - advanced_insights
        """,
        output_key="extracted_skills"
)