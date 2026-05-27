# Demonstrates different LLM methods and functions
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
import asyncio


handle = OpenAI().stream_complete("William Shakespeare is ")

# for token in handle:
#     print(token.delta, end="", flush=True)

llm = OpenAI(model="gpt-4o-mini")

response = llm.complete("Who is Laurie Voss?")
# print(response)

messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="Tell me an actually funny joke(not about scarecrows.)"),
]
chat_response = llm.chat(messages)
# print(chat_response)

stream_response = llm.stream_chat(messages)

# for token in stream_response:
#     print(token.delta, end="", flush=True)

async def main(): 
    astream_response = await llm.astream_chat(messages)

    async for token in astream_response:
        print(token.delta, end="", flush=True)

# asyncio.run(main()) 

IMGmessages = [
    ChatMessage(
        role="user",
        blocks=[
            ImageBlock(path="image.png"),
            TextBlock(text="Describe the image in a few sentences."),
        ],
    )
]
resp = llm.chat(IMGmessages)
print(resp.message.content)