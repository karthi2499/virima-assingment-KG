from google.genai import types
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters



t = types.GenerateContentConfig(
    tools=[
        types.Tool(function_declarations=[])
    ],
    system_instruction="You are a helpful assistant.",
)