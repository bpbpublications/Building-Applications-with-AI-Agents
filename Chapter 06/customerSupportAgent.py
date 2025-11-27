
###--------Customer support agent using CrewAI.-------------


###Environment setup - Install the CrewAI library before running this code if you haven't already:
import pip
pip install crewai


###Configure environment and LLM
import os
from typing import Dict
from crewai import LLM
from crewai import Agent, Task, Crew, Process
import os

###Configure the large language model
from crewai import LLM

os.environ["OPENAI_API_KEY"] = "your-openai-key"
llm = LLM(model="openai/gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

###Define specialized tools

from typing import Dict
from crewai.tools import BaseTool

# Simulated tool to fetch order status
class OrderStatusTool(BaseTool):
    name: str = "Order Status Checker"
    description: str = "Retrieves the shipping status given an order ID."

    def _run(self, order_id: str) -> str:
        # Replace with real API call in production
        return f"Order {order_id} is shipped and expected to arrive tomorrow."

order_status_tool = OrderStatusTool()

# Simulated tool to answer FAQs
class FAQTool(BaseTool):
    name: str = "FAQ Answerer"
    description: str = "Answers frequently asked questions on products, returns, policies, etc."
    faqs : Dict[str, str]= {
        "return policy": "Returns accepted within 30 days for unused items.",
        "shipping time": "Standard shipping takes 3-5 business days.",
        "warranty": "1-year warranty on all electronic items."}
    def _run(self, question: str) -> str:
        # Simple matching; in production use better NLP or search
        for key, answer in self.faqs.items():
            if key in question.lower():
                return answer
        answer="I am not sure. Let me escalate this to a human support specialist."
        return answer

faq_tool = FAQTool()

# Simulated tool to escalate to human support
class HumanEscalationTool(BaseTool):
    name: str = "Human Escalation"
    description: str = "Escalates unresolved or sensitive queries to a human agent."
    def _run(self, query: str) -> str:
        # In practice, trigger a ticketing system, send email, etc.
        return f"Your query has been forwarded to a human support agent for review: '{query}'."

escalation_tool = HumanEscalationTool()

###Define agents and their roles

from crewai import Agent

# Agent for routine queries
auto_support_agent = Agent(
    role="Automated Customer Support Agent",
    goal="Resolve routine customer queries promptly and escalate complex or sensitive cases.",
    backstory="You handle simple order status and FAQ queries, escalating anything unclear or complex.",
    llm=llm,
    tools=[order_status_tool, faq_tool, escalation_tool],
    verbose=True
)

# Agent to simulate a Human Support Specialist
human_support_agent = Agent(
    role="Human Support Agent",
    goal="Review escalated queries and provide the best resolution.",
    backstory="An expert trained to handle complex, ambiguous, or sensitive customer concerns.",
    llm=llm,
    tools=[],  # Optionally give access to all tools
    verbose=True
)


###Assign tasks to agents

from crewai import Task

# Routine support task: handles most queries autonomously
routine_task = Task(
    description="Handle customer queries regarding order status or FAQs. Escalate if the query is complex or unclear.",
    expected_output="Clear response to the customer, or escalation to a human agent if necessary.",
    agent=auto_support_agent
)

# Escalation task: only runs if needed
escalation_task = Task(
    description="If the routine support agent escalates, review the query and provide a human-crafted response.",
    expected_output="Resolution or follow-up for the customer.",
    agent=human_support_agent
)

###Crew orchestration


from crewai import Crew, Process

crew = Crew(
    agents=[auto_support_agent, human_support_agent],
    tasks=[routine_task, escalation_task],
    process=Process.sequential,  # Tasks run in order, escalation only if necessary
    verbose=True
)


###Running and observing the agent

# Execute the workflow
customer_query = "Can you tell me status of my order id #12345?"
result = crew.kickoff(inputs={"customer_query": customer_query})
print(result)



