from dspy.modules import PromptCompression

# Initialize the Prompt Compression module
prompt_compressor = PromptCompression()

original_prompt = "Long description of a scenario that exceeds the token limit..."
compressed_prompt = prompt_compressor.compress(original_prompt)

# Use the compressed prompt with a language model
from dspy.modules import ChainOfThought
cot = ChainOfThought(signature="compressed_prompt -> answer")
answer = cot(compressed_prompt)
