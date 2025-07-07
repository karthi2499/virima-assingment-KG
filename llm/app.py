from google import genai
from google.genai import types


# Initialize the Google GenAI client
client = genai.Client()


# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)