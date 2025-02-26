from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.schema import AgentAction, AgentFinish

class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]
    
    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += f"\nAction: {action}\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

class VortexAgent:
    def __init__(self, tools: List[Tool], llm: Optional[Any] = None):
        self.tools = tools
        self.llm = llm or OpenAI(temperature=0)
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.agent_executor = self._create_agent_executor()

    def _create_agent_executor(self) -> AgentExecutor:
        template = """You are an AI assistant that helps users accomplish tasks.
You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Previous conversation history:
{chat_history}

Question: {input}
{agent_scratchpad}"""

        prompt = CustomPromptTemplate(
            template=template,
            tools=self.tools,
            input_variables=["input", "intermediate_steps", "chat_history"]
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        
        tool_names = [tool.name for tool in self.tools]
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=self._output_parser,
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )

        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )

    def _output_parser(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )

        action_match = re.search(r"Action: (.*?)[\n]", llm_output, re.DOTALL)
        action_input_match = re.search(r"Action Input: (.*)", llm_output, re.DOTALL)
        
        if not action_match or not action_input_match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        
        action = action_match.group(1).strip()
        action_input = action_input_match.group(1).strip()
        
        return AgentAction(tool=action, tool_input=action_input, log=llm_output)

    async def run(self, input_text: str) -> Dict[str, Any]:
        try:
            response = await self.agent_executor.arun(input=input_text)
            return {"status": "success", "response": response}
        except Exception as e:
            return {"status": "error", "error": str(e)}
