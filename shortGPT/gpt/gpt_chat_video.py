from shortGPT.gpt import gpt_utils
from app.logger import logger
import json
def generateScript(prompt: str) -> str:
    """
    Generates a video script based on the provided prompt.

    Args:
        prompt (str): The prompt to generate the script from.

    Returns:
        str: The generated script, or None if there was an error.
    """
    chat_prompt = prompt

    system_message = (
        "You are an AI that generates high-quality video scripts based on the provided prompt. "
        "Your response should include only the main script content. Ensure that the script is structured logically and flows well, "
        "without including any narration or direction. Focus solely on the content itself, making it engaging and informative for the audience. "
        "Please avoid any newline characters, extra whitespace, or special characters at the beginning or end of the script. "
        "Ensure the entire script is a single continuous text without breaks, unnecessary punctuation, or non-alphanumeric characters. "
        "Use clear and concise language to maintain clarity and coherence throughout."
    )

    json_schema = {
        "name": "video_script_simple_schema",
        "schema": {
            "type": "object",
            "properties": {
                "script": {
                    "description": "The main script content for the video.",
                    "type": "string"
                }
            },
            "required": ["script"],
            "additionalProperties": False
        }
    }

    response = gpt_utils.gpt4o_completion(chat_prompt, system_message, json_schema)

    # Check for errors in the response
    if "error" in response:
        logger.error(f"Error generating script: {response['message']}")
        return None  # or handle the error as needed

    # Return the script, trimmed of any surrounding whitespace
    return response.get("script", "").strip()  # Ensures that we return a string even if not found

def correctScript(script, correction):
    out = {'script': ''}
    chat, system = gpt_utils.load_local_yaml_prompt('prompt_templates/chat_video_edit_script.yaml')
    chat = chat.replace("<<ORIGINAL_SCRIPT>>", script).replace("<<CORRECTIONS>>", correction)

    while not ('script' in out and out['script']):
        try:
            result = gpt_utils.gpt3Turbo_completion(chat_prompt=chat, system=system, temp=1)
            out = json.loads(result)
        except Exception as e:
            print("Difficulty parsing the output in gpt_chat_video.generateScript")
    return out['script']