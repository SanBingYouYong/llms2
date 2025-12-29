import openai
import yaml
from dotenv import load_dotenv
import os

from .utils import encode_image

class LLMS:
    def __init__(self, config_file: str='llms.yml'):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file {config_file} not found.")

        with open(config_file, "r") as f:
            self.profiles = yaml.safe_load(f).get("profiles")
        if not self.profiles:
            raise ValueError("No profiles found in configuration file.")
        self._check_profiles()
        self.clients = {}
    
    def _check_profiles(self):
        '''
        Ensure all profiles have required fields, and that environment variables are set.
        '''
        load_dotenv()
        required_fields = ["model", "url", "api_key_env"]
        for profile_name, profile_data in self.profiles.items():
            for field in required_fields:
                if field not in profile_data:
                    raise ValueError(f"Profile '{profile_name}' is missing required field '{field}'.")
            # check that api_key_env is set in environment
            api_key_env = profile_data["api_key_env"]
            if not os.getenv(api_key_env):
                raise ValueError(f"Environment variable '{api_key_env}' for profile '{profile_name}' is not set.")

    def _get_client(self, profile: str):
        '''
        Profile exists, get or initialize the client for the profile.
        '''
        if profile in self.clients:
            return self.clients[profile]

        profile_data = self.profiles[profile]
        client = openai.OpenAI(
            api_key=os.getenv(profile_data["api_key_env"]),
            base_url=profile_data["url"]
        )
        self.clients[profile] = client
        return client
    
    def save_messages(self, profile: str, messages: list[dict], filepath: str):
        '''
        Saves messages to a YAML file including the profile info.
        '''
        to_be_saved = {
            "profile": profile,
            "messages": messages
        }
        with open(filepath, "w") as f:
            yaml.dump(to_be_saved, f)

    def load_messages(self, filepath: str) -> list[dict]:
        '''
        Loads messages from a YAML file ignoring the profile info.
        '''
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
        return data["messages"]

    def prepare_messages(self, prompt: str, image_paths: list[str]=None,
                         system_msg: str=None, history_msgs: list[dict]=None) -> list[dict]:
        '''
        Prepares messages for a chat completion request.
        - prompt: Latest user message.
        - image_paths: List of image file paths to be included in the user message.
        - system_msg: Optional system message to include at the start, typically used to initialize the assistant's behavior. Will always be inserted at the start of the messages.
        - history_msgs: Optional list of previous messages to include in the conversation history. Should not contain a system message if system_msg is provided.
        '''
        messages = []
        if system_msg:
            if history_msgs:
                # Check if there's already a system message in history
                for msg in history_msgs:
                    if msg["role"] == "system":
                        raise ValueError("System message already exists in history messages.")
            messages.append({"role": "system", "content": system_msg})
        if history_msgs:
            messages.extend(history_msgs)
        user_content = prompt
        if image_paths:
            user_content = [
                {"type": "text", "text": prompt}
            ]
            for image_path in image_paths:
                encoded_image = encode_image(image_path)
                user_content.append(
                    {"type": "image_url", 
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                )
        messages.append({"role": "user", "content": user_content})
        return messages
        
    def query(self, profile: str, messages: list[dict]) -> str:
        '''
        Makes a query using the specified LLM profile, and returns the response message string.
        '''
        if profile not in self.profiles:
            raise ValueError(f"Profile '{profile}' not found in configuration.")

        profile_data = self.profiles[profile]
        client = self._get_client(profile)

        response = client.chat.completions.create(
            model=profile_data["model"],
            messages=messages,
            **profile_data.get("request_params", {})
        )
        return response.choices[0].message.content
