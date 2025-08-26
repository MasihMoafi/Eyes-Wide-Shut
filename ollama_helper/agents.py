import asyncio
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
 
set_tracing_disabled(True)
 
@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."
 
 
async def main(model: str, api_key: str):
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(model="ollama/gpt-oss:120b", api_key=api_key),
        tools=[get_weather],
    )
 
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)
 
if __name__ == "__main__":
    asyncio.run(main())
