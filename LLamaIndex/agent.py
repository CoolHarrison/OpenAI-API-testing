from dotenv import load_dotenv

load_dotenv()

from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context, JsonPickleSerializer, JsonSerializer
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
import asyncio


def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

llm = OpenAI(model="gpt-4o-mini")

finance_tools = YahooFinanceToolSpec().to_tool_list()
finance_tools.extend([multiply, add])

workflow = FunctionAgent(
    name="Agent",
    description="Useful for performing financial operations.",
    llm=OpenAI(model="gpt-4o-mini"),
    tools=finance_tools,
    system_prompt="You are a helpful assistant.",
)

async def main(): 
    ctx = Context(workflow)
    response = await workflow.run("My name is Sir. Billionson", ctx=ctx)
    
    ctx_dict = ctx.to_dict(serializer=JsonSerializer())
    restored_ctx = Context.from_dict(
        workflow, ctx_dict, serializer=JsonSerializer()
    )
    while True:
        user_input = input("You: ")
        response = await workflow.run(user_input, ctx=restored_ctx)
        print(response)
        

asyncio.run(main()) 