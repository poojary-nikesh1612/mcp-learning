import asyncio

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["E:/Brave/mcp-project/servers/math_server.py"],
            },
            "weather": {
                "transport": "http",
                "url": "http://localhost:8000/mcp",
            },
        }
    )

    tools = await client.get_tools()
    print(tools)

    agent = create_agent(model, tools)

    res = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": "what is 32*2+4*5 and weather in mangalore"}
            ]
        }
    )
    print(res["messages"][-1].content[-1]["text"])


if __name__ == "__main__":
    asyncio.run(main())
