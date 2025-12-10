from langchain_ollama import ChatOllama

from src.agent.agent_state import UserIntent, ExecutionPlan

MODEL_NAME = "qwen2.5:32b"

llm = ChatOllama(model=MODEL_NAME, temperature=0)

llm_user_intention = ChatOllama(model=MODEL_NAME, temperature=0).with_structured_output(UserIntent)

llm_planner = ChatOllama(model=MODEL_NAME, temperature=0).with_structured_output(ExecutionPlan)