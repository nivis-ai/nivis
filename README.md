# 🌀 Nivis AI Agent Framework

Nivis is a powerful and flexible AI agent framework that enables the creation of autonomous agents capable of performing complex tasks through natural language interaction.

![Nivis Banner](docs/banner.png)

## ✨ Features

- 🤖 **Autonomous Agents**: Create AI agents that can understand and execute complex tasks
- 🔧 **Extensible Tools**: Easy-to-add custom tools and capabilities
- 🧠 **Advanced LLM Integration**: Powered by state-of-the-art language models
- 🚀 **High Performance**: Built with FastAPI for high-speed API responses
- 📝 **Conversation Memory**: Maintains context across multiple interactions
- 🔍 **Built-in Tools**: Includes web search, calculator, and data analysis capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry

### Installation

1. Clone the repository:
```bash
git clone https://github.com/nivis-ai/nivis
cd Nivis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other configurations
```

4. Run the server:
```bash
uvicorn src.api:app --reload
```

## 🎯 Usage

### Basic Example

```python
from Nivis.agent import NivisAgent
from Nivis.tools import get_default_tools

# Initialize agent
agent = NivisAgent(tools=get_default_tools())

# Run a query
response = await agent.run("What is the weather in New York?")
print(response)
```

### API Endpoints

- POST `/query`: Send queries to the AI agent
- GET `/health`: Health check endpoint

## 🛠️ Creating Custom Tools

```python
from langchain.tools import BaseTool

class MyCustomTool(BaseTool):
    name = "my_tool"
    description = "Description of what my tool does"

    def _run(self, input: str) -> str:
        # Implement your tool logic here
        return f"Result: {input}"

    async def _arun(self, input: str) -> str:
        return self._run(input)
```

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/
```

## 📚 Documentation

For detailed documentation, please visit our [documentation site]().

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support

If you find Nivis helpful, please give it a star ⭐ on GitHub!
