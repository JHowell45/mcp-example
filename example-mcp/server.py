from fastmcp import FastMCP

mcp = FastMCP("Example MCP")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=9000, path="/mcp")
