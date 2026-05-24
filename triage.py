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

# Exit detection agent
exit_agent = Agent(
    name="exit_agent",
    instructions=(
        "Determine whether the user wants to end the conversation.\n"
        "Respond ONLY with YES or NO.\n"
        "YES = user wants to quit.\n"
        "NO = user wants to continue."
    ),
)

async def main():
    # Stores conversation history
    conversation = []

    while True:
        user_input = input("You: ")

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
        print(f"\nAssistant: {assistant_response}\n")

         # Ask AI if user wants to quit
        exit_result = await Runner.run(
            exit_agent,
            input=user_input,
        )

        decision = exit_result.final_output.strip().upper()

        if decision == "YES":
            break

        # Save assistant response to memory
        conversation.append(
            {
                "role": "assistant",
                "content": assistant_response,
            }
        )


if __name__ == "__main__":
    asyncio.run(main())