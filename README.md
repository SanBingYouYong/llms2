# llms2

A Python package for managing multiple LLM profiles and API interactions.

## Installation

Install the package using pip:

```bash
pip install -e .
```
- or `pip install git+https://github.com/SanBingYouYong/llms2.git`

Or with uv:

```bash
uv pip install -e .
```
- or `uv add git+https://github.com/SanBingYouYong/llms2.git`

## Configuration

Create a `llms.yml` file with your LLM profiles:

```yaml
profiles:
  example_profile:
    url: https://api.example.com
    api_key_env: EXAMPLE_API_KEY
    model: model-name
    vision: false
    accepts_sys_msg: true
    request_params:
      temperature: 1
```

Set the corresponding environment variables in a `.env` file or export them:

```bash
export EXAMPLE_API_KEY=your_api_key_here
```

## Usage

```python
from llms2 import LLMS

# Initialize with configuration file (default: llms.yml)
llms = LLMS()

# Prepare messages
messages = llms.prepare_messages(
    prompt="Hello, how are you?",
    system_msg="You are a helpful assistant."
)

# Query an LLM profile
response = llms.query("deepseek-v3.2", messages)
print(response)

# Save conversation history
messages.append({"role": "assistant", "content": response})
llms.save_messages("deepseek-v3.2", messages, "conversation.yml")

# Load conversation history
loaded_messages = llms.load_messages("conversation.yml")
```

## Features

- Support for multiple LLM profiles with different configurations
- Vision model support for image inputs
- Conversation history management (save/load)
- System message support
- Configurable request parameters per profile

## Development Notes

- Streaming and visualization features: disregarded from llms
- Distributed chat history dump comparing to llms
