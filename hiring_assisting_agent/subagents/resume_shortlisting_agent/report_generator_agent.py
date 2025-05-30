from google.adk.agents import Agent

report_generator_agent = Agent(
    model='gemini-2.0-flash-001',
    name='report_generator_agent',
    description='Generates a shortlisting report based on skill matching score.',
    instruction="""
        You are the final agent in the resume shortlisting pipeline. Your job is to generate a shortlisting report.

        Input:
        {score_and_report}

        Use a cutoff score of 70.

        Instructions:
            1. Compare the candidate's score to the provided cutoff.
            2. If the score is greater than or equal to the cutoff:
                - Mark the candidate as "shortlisted".
            3. Otherwise:
                - Mark the candidate as "not shortlisted".
            4. Generate a final report in JSON format as shown below.
            Output Format:
                {
                "candidate_status": "shortlisted" or "not shortlisted",
                "score": <candidate_score>,
                "cutoff": <cutoff_value>,
                "decision_reason": "Brief summary justifying the decision based on matched and missing skills, reasoning, and how the score aligns with the cutoff."
                }

        
        Only output the JSON.
    """
)