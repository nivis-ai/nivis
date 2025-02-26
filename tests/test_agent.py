import pytest
from src.agent import VortexAgent
from src.tools import get_default_tools

@pytest.fixture
def agent():
    return VortexAgent(tools=get_default_tools())

@pytest.mark.asyncio
async def test_agent_basic_query(agent):
    result = await agent.run("What is 2 + 2?")
    assert result["status"] == "success"
    assert "4" in result["response"]

@pytest.mark.asyncio
async def test_agent_web_search(agent):
    result = await agent.run("Search for information about Python programming")
    assert result["status"] == "success"
    assert "Python" in result["response"]

@pytest.mark.asyncio
async def test_agent_error_handling(agent):
    result = await agent.run("1/0")  # Should trigger an error
    assert result["status"] == "error"
    assert "error" in result
