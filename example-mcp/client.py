from fastmcp import Client
from rich import print

client = Client("Example MCP Client")


async def call_tool(a: int, b: int):
    async with client:
        result = await client.call_tool("add", {"a": a, "b": b})
        print(result)
