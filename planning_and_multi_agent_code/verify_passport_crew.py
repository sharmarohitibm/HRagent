import os
from dotenv import load_dotenv
from crewai import LLM, Task, Agent, Crew, Process
from typing import List

from crewai_tools import NL2SQLTool
from crewai import Agent, Crew, Task, Process
from crewai import LLM
import os

load_dotenv()
# psycopg2 was installed to run this example with PostgreSQL
# nl2sql = NL2SQLTool(db_uri="sqlite:///sales.db")
api_key=os.environ["WATSONX_API_KEY"]
db_url=os.environ["DB_URI"]
nl2sql = NL2SQLTool(db_uri= db_url)
load_dotenv()

# === LLM Setup ===
# Initialize LLM
llm = LLM(
    api_key=os.environ["WATSONX_API_KEY"],
    model="watsonx/meta-llama/llama-3-3-70b-instruct",
    params={
        "decoding_method": "sample",
        "max_new_tokens": 15000,
        "temperature": 0,
        "repetition_penalty": 1.05
    }
)

# === Function to Generate Blog Post ===
def get_passport_details(question: str) -> str:
    # === Define Agents ===
    db_agent= Agent(
        role="Database Analyst",
        goal="""Generates the report based on user question and information in database. Always write the colum name as table_name."column_name" in sql query. Formulate the respose in table structure.""",
        backstory="""You are an expert data analyst creating reports from database.""",
        llm=llm,
        allow_delegation=False,
        tools=[nl2sql]
    )

    # === Define Tasks ===
    extraction_task = Task(
        description=f"""{question}.""",
        expected_output="""Response from database after running the query.""",
        agent=db_agent
    )


    # === Assemble the Crew ===
    crew = Crew(
        agents=[db_agent],
        tasks=[extraction_task],
        verbose=False
    )

    # === Run the Crew ===
    result = crew.kickoff()
    return result