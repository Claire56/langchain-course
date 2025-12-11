import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

class Source(BaseModel):
    """Schema for Agent sources of information"""
    source: str = Field(description="The source of the information")

class AgentResponse(BaseModel):
    """Schema for Agent response with answer and sources of information"""
    response: str = Field(description="The response from the agent for the query")
    sources: list[Source] = Field(default_factory=list, description="The sources used to generate the response")

load_dotenv()

tools = [TavilySearch()]
# tavily_client = TavilyClient()
# @tool
# def search_tavily(query: str) -> str:
#     """Search the web for information
    
#     Args:
#         query: The query to search for
#     Returns:
#         The search results
#     """
#     print(f"Searching the web for {query}")
#     results = tavily_client.search(query, max_results=4)
#     # print(results)
#     return results
# tools = [search_tavily]

llm=ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Hello from langchain-course!")

    result = agent.invoke({"messages": [HumanMessage(content="I want you to search linkedin for 4 AI engineer roles in San Francisco with Easy Apply, and are remote, give me their title and a link to the job posting")]})
    print(result)


if __name__ == "__main__":
    main()
