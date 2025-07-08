import constants as const
import llm.tools.app as tool_app
from google import genai
from google.genai import types

# Initialize the Google GenAI client
client = genai.Client()

model_mapping = {
    'flash': const.gemini_model_flash,
    'pro': const.gemini_model_pro,
}

tools_mapping = {
    'chat': [tool_app.grounding_tool],
    'neo4j': [tool_app.execute_neo4j_query],
}

with open('llm/system-prompt.txt', 'r') as file:
    system_instruction = file.read().strip()


def llm(user_input, model='flash', tools='chat', schema: str = None):
    """Generates a response from the Gemini model using the provided user input.
    Args:
        user_input (str): The input text from the user.
    Returns:
        str: The generated response from the model.
    """
    config = types.GenerateContentConfig(
        tools=tools_mapping[tools],
        system_instruction=f'{system_instruction}\n\n{schema}' if schema else '',
    )

    chat = client.chats.create(
        model=model_mapping[model], 
        config=config,
        
    )
    response = chat.send_message(user_input)
    return response.text


def llm_with_conver(user_input, tools='chat', model='flash'):
    """Generates a response from the Gemini model using the provided user input and conversation history.
    Args:
        user_input (str): The input text from the user.
        conversation (list): The conversation history.
    Returns:
        str: The generated response from the model.
    """
    config = types.GenerateContentConfig(
        tools=tools_mapping[tools],
        system_instruction=system_instruction,
    )

    for chunk in client.models.generate_content_stream(
        model=model_mapping[model],
        contents=user_input,
        config=config,
    ):
        if chunk.text:
            yield chunk.text
