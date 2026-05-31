# Demonstrates different LLM methods and functions
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import ChatMessage, TextBlock, ImageBlock
import asyncio


# handle = OpenAI().stream_complete("William Shakespeare is ")

# for token in handle:
#     print(token.delta, end="", flush=True)

llm = OpenAI(model="gpt-4o-mini")

messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="Tell me an actually funny joke(not about scarecrows.)"),
]

# response = llm.complete("Who is Laurie Voss?")
# print(response)

# chat_response = llm.chat(messages)
# print(chat_response)

# stream_response = llm.stream_chat(messages)

# for token in stream_response:
#     print(token.delta, end="", flush=True)


# IMGmessages = [
#     ChatMessage(
#         role="user",
#         blocks=[
#             ImageBlock(path="obama (high res).png"),
#             TextBlock(text="Which president is in the image?"),
#         ],
#     )
# ]
# resp = llm.chat(IMGmessages)
# print(resp.message.content)


def generate_song(name: str, artist: str) -> dict:
    """Generates a song with provided name and artist."""
    return {"name": name, "artist": artist}

tool = FunctionTool.from_defaults(fn=generate_song)

response = llm.predict_and_call(
    [tool],
    "Pick a random song for me",
)
print(str(response))

async def main(): 
    
    astream_response = await llm.astream_chat(messages)

    async for token in astream_response:
        print(token.delta, end="", flush=True)

# asyncio.run(main()) 
