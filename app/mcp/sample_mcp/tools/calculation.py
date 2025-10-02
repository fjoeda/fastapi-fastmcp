from fastmcp import FastMCP


def register_tools(mcp: FastMCP):
    @mcp.tool(name="add", description="Add two numbers")
    def add(a: int, b: int) -> int:
        """
        Adds two numbers.
        """
        return a + b

    @mcp.tool(name="multiply", description="Multiply two numbers")
    def multiply(a: int, b: int) -> int:
        """
        Multiplies two numbers.
        """
        return a * b