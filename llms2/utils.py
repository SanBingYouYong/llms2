import base64

def encode_image(image_path: str) -> str:
    """
    Encodes an image file to a base64 string.

    Args:
        image_path: The path to the image file.

    Returns:
        The base64 encoded image string.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found at: {image_path}")

def decode_image(encoded_str: str, output_path: str):
    """
    Decodes a base64 string and saves it as an image file.

    Args:
        encoded_str: The base64 encoded image string.
        output_path: The path to save the decoded image file.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(encoded_str))

def extract_code_block(response: str, tag: str) -> str:
    """
    Extracts a markdown code block (first found) marked with the specified tag from an LLM response.

    Args:
        response (str): The LLM response containing a markdown code block.
        tag (str): The tag marking the code block (e.g., 'jsonl', 'python', 'json').

    Returns:
        str: The extracted content.

    Raises:
        ValueError: If no valid code block is found.
    """
    lines = response.splitlines()
    start, end = None, None

    # Find the start and end of the code block
    for i, line in enumerate(lines):
        if line.strip() == f"```{tag}":
            start = i + 1
        elif line.strip() == "```" and start is not None:
            end = i
            break

    if start is None or end is None:
        raise ValueError(f"No {tag} markdown code block found in the response:\n{response}")

    code_block = lines[start:end]
    return "\n".join(code_block)
