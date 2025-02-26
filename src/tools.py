from typing import List
from langchain.agents import Tool
from langchain.tools import BaseTool
import requests
import json

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for information"

    def _run(self, query: str) -> str:
        # Implement your web search logic here
        return f"Search results for: {query}"

    async def _arun(self, query: str) -> str:
        return self._run(query)

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Perform mathematical calculations"

    def _run(self, expression: str) -> str:
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, expression: str) -> str:
        return self._run(expression)

class DataAnalysisTool(BaseTool):
    name = "data_analysis"
    description = "Analyze data and provide insights"

    def _run(self, data: str) -> str:
        try:
            # Parse the input data as JSON
            json_data = json.loads(data)
            # Implement your data analysis logic here
            return "Data analysis results"
        except Exception as e:
            return f"Error analyzing data: {str(e)}"

    async def _arun(self, data: str) -> str:
        return self._run(data)

def get_default_tools() -> List[Tool]:
    """
    Get the default set of tools available to the agent
    """
    return [
        Tool(
            name="web_search",
            func=WebSearchTool()._run,
            description="Search the web for information"
        ),
        Tool(
            name="calculator",
            func=CalculatorTool()._run,
            description="Perform mathematical calculations"
        ),
        Tool(
            name="data_analysis",
            func=DataAnalysisTool()._run,
            description="Analyze data and provide insights"
        )
    ]
