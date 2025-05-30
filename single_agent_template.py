class SingleAgent:
    def __init__(self, name, model, description, instruction):
        self.name = "_".join(name.split())
        self.model = model
        self.description = description
        self.instruction = instruction

    def create_ADK_agent(self):
        from google.adk.agents import Agent
        agent = Agent(
            name = self.name,
            model = self.model,
            description = self.description,
            instruction=(self.instruction)
        )
        return agent