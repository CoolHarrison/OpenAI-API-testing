from dotenv import load_dotenv

load_dotenv()

from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import AgentWorkflow, FunctionAgent, AgentStream
from llama_index.core.workflow import Context, InputRequiredEvent, HumanResponseEvent,JsonPickleSerializer, JsonSerializer
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from llama_index.tools.tavily_research import TavilyToolSpec
import os
import asyncio


def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

async def set_name(ctx: Context, name: str) -> str:
    async with ctx.store.edit_state() as ctx_state:
        ctx_state["state"]["name"] = name

    return name
#Function that
async def dangerous_task(ctx: Context) -> str:
    """A dangerous task that requires human confirmation."""

    # emit a waiter event (InputRequiredEvent here) 
    # and wait until we see a HumanResponseEvent 
    state = await ctx.store.get("state")
    name = state.get("name", "unset")

    if name != "Harrison":
        return "Access denied: Incorrect user name."

    question = "Are you sure you want to proceed? "

    response = await ctx.wait_for_event(
        HumanResponseEvent,
        waiter_id=question,
        waiter_event=InputRequiredEvent(
            prefix=question,
            user_name=name,
        ),
    )
    return "Dangerous task completed successfully."


llm = OpenAI(model="gpt-4o-mini")

finance_tools = YahooFinanceToolSpec().to_tool_list()
finance_tools.extend([multiply, add])

tavily_tool = TavilyToolSpec(api_key=os.getenv("TAVILY_API_KEY"))

workflow1 = FunctionAgent(
    name="Agent",
    description="Useful for performing financial operations.",
    llm=OpenAI(model="gpt-4o-mini"),
    tools=finance_tools,
    system_prompt="You are a helpful assistant.",
)

workflow2 = AgentWorkflow.from_tools_or_functions( #Uses set_name function as a tool in the workflow
    [set_name],
    llm=llm,
    system_prompt="You are a helpful assistant that can set a name.",
    initial_state={"name": "Harrison"},
)

workflow3 = FunctionAgent(
    tools=tavily_tool.to_tool_list(),
    llm=llm,
    system_prompt="You're a helpful assistant that can search the web for information.",
)

workflow4 = FunctionAgent(
    tools=[dangerous_task, set_name],
    llm=llm,
    system_prompt="You are a helpful assistant that can perform dangerous tasks.",
    initial_state={"name": "unset"},
)
                      
workflow = workflow4


async def main(): 
    ctx = Context(workflow)
    # (Workflow2)
    # response = await workflow.run("My name is Sir. Billionson", ctx=ctx)
    # ctx_dict = ctx.to_dict(serializer=JsonSerializer())
    # restored_ctx = Context.from_dict(
    #     workflow, ctx_dict, serializer=JsonSerializer()
    # )
    # print("Name as stored in state: ", restored_ctx.state["name"])

    # (Workflow3)
    # while True:
    #     user_input = input("\nYou: ")
    #     response = workflow.run(user_input, ctx=ctx)
    #     async for event in response.stream_events():
    #         if isinstance(event, AgentStream):
    #             print(event.delta, end="", flush=True)      

    # (Workflow4)
    while True:
        user_input = input("\nYou: ")
        handler = workflow.run(user_input, ctx=ctx)
        async for event in handler.stream_events():
            if isinstance(event, InputRequiredEvent):
                # capture keyboard input
                response = input(event.prefix)
                # send our response back
                handler.ctx.send_event(
                    HumanResponseEvent(
                        response=response,
                        user_name=event.user_name,
                    )
                )

        response = await handler
        print(str(response).strip)        

asyncio.run(main()) 