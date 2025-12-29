"""
Example usage of the llms2 package.

This example demonstrates how to use the LLMS class to interact with LLM APIs.
"""

from llms2 import LLMS

# Initialize LLMS with a configuration file
# Default is 'llms.yml' in the current directory
llms = LLMS()

# Prepare a simple message
messages = llms.prepare_messages(
    prompt="Hello, how are you?",
    system_msg="When user asks how are you, say hello world."
)

# Query the LLM (requires API keys to be set in environment)
# response = llms.query("deepseek-v3.2", messages)
# print(response)

# Example with image (for vision models)
# messages = llms.prepare_messages(
#     prompt="What do you see in this image?",
#     image_paths=["test_img.png"]
# )
# response = llms.query("qwen3vl-plus", messages)
# print(response)

# Save and load conversation history
# messages.append({"role": "assistant", "content": response})
# llms.save_messages("deepseek-v3.2", messages, "conversation.yml")
# loaded_messages = llms.load_messages("conversation.yml")
# assert messages == loaded_messages, "! Loaded messages do not match saved messages."

print("Example script loaded successfully!")
print("Uncomment the lines above to test with real API calls.")
