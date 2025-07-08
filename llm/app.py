from google import genai
import constants as const
from google.genai import types
from tools import tools as _tools

model_mapping = {
    'flash': const.gemini_model_flash,
    'pro': const.gemini_model_pro,
}


# Initialize the Google GenAI client
client = genai.Client()

with open('system-prompt.txt', 'r') as file:
    system_instruction = file.read().strip()

config = types.GenerateContentConfig(
    tools=_tools,
    system_instruction=system_instruction,
)


def llm(user_input, model='flash'):
    """Generates a response from the Gemini model using the provided user input.
    Args:
        user_input (str): The input text from the user.
    Returns:
        str: The generated response from the model.
    """
    response = client.models.generate_content(
        model=model_mapping[model], 
        contents=user_input,
        config=config,
    )
    return response.text

