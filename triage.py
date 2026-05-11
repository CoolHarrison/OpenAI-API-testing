from agents import Agent, Runner
import asyncio

# Create specialized agents
spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English.",
)

# Create routing/triage agent
triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)


async def main():
    print("Chat started! Type 'quit' to exit.\n")

    # Stores conversation history
    conversation = []

    while True:
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        # Add user message to conversation history
        conversation.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # Run the agent system
        result = await Runner.run(
            triage_agent,
            input=conversation,
        )

        # Get AI response
        assistant_response = result.final_output

        # Print response
        print(f"Assistant: {assistant_response}\n")

        # Save assistant response to memory
        conversation.append(
            {
                "role": "assistant",
                "content": assistant_response,
            }
        )


if __name__ == "__main__":
    asyncio.run(main())