PROVIDERS = [
    ("OpenAI", "openai"),
    ("Anthropic", "anthropic"),
    ("Cohere", "cohere"),
    ("Meta", "huggingface_hub/meta"),
    ("Mistral AI", "mistralai"),
]

OPENAI_MODELS = [
    ("GPT-3.5-Turbo", "gpt-3.5-turbo"),
    ("GPT-4", "gpt-4"),
]

ANTHROPIC_MODELS = [
    ("Claude 3 Opus", "claude-3-opus-20240229"),
    ("Claude 3 Sonnet", "claude-3-sonnet-20240229"),
    ("Claude 3 Haiku", "claude-3-haiku-20240307"),
    ("Claude 2.1", "claude-2.1"),
    ("Claude 2.0", "claude-2.0"),
    ("Claude Instant 1.2", "claude-instant-1.2"),
]

COHERE_MODELS = [
    ("Command Light", "command-light"),
    ("Command", "command"),
    ("Command R", "command-r"),
    ("Command R+", "command-r-plus"),
]

META_MODELS = [
    ("Llama 3 8B", "meta-llama/Meta-Llama-3-8B"),
    ("Llama 3 70B", "meta-llama/Meta-Llama-3-70B"),
    ("Llama 2 7B", "meta-llama/Llama-2-7b-hf"),
    ("Llama 2 13B", "meta-llama/Llama-2-13b-hf"),
    ("Llama 2 70B", "meta-llama/Llama-2-70b-hf"),
]

MISTRALAI_MODELS = [
    ("Mistral 7B", "open-mistral-7b"),
    ("Mixtral 8x7B", "open-mixtral-8x7b"),
    ("Mixtral 8x22B", "open-mixtral-8x22b"),
    ("Tiny", "mistral-tiny-2312"),
    ("Small", "mistral-small-2402"),
    ("Medium", "mistral-medium-2312"),
    ("Large", "mistral-large-2402"),
]

PROMPTS = [
    ("Write a Tweet", 50),
    ("Write an email", 170),
    ("Write an article summary", 250),
    ("Small conversation with a chatbot", 400),
    ("Write a report of 5 pages", 5000),
]
PROMPTS = [(s + f" ({v} output tokens)", v) for (s, v) in PROMPTS]

MODELS = [
    ("OpenAI / GPT-3.5-Turbo", "openai/gpt-3.5-turbo"),
    ("OpenAI / GPT-4", "openai/gpt-4"),
    ("Anthropic / Claude 3 Opus", "anthropic/claude-3-opus-20240229"),
    ("Anthropic / Claude 3 Sonnet", "anthropic/claude-3-sonnet-20240229"),
    ("Anthropic / Claude 3 Haiku", "anthropic/claude-3-haiku-20240307"),
    ("Anthropic / Claude 2.1", "anthropic/claude-2.1"),
    ("Anthropic / Claude 2.0", "anthropic/claude-2.0"),
    ("Anthropic / Claude Instant 1.2", "anthropic/claude-instant-1.2"),
    ("Mistral AI / Mistral 7B", "mistralai/open-mistral-7b"),
    ("Mistral AI / Mixtral 8x7B", "mistralai/open-mixtral-8x7b"),
    ("Mistral AI / Mixtral 8x22B", "mistralai/open-mixtral-8x22b"),
    ("Mistral AI / Tiny", "mistralai/mistral-tiny-2312"),
    ("Mistral AI / Small", "mistralai/mistral-small-2402"),
    ("Mistral AI / Medium", "mistralai/mistral-medium-2312"),
    ("Mistral AI / Large", "mistralai/mistral-large-2402"),
    ("Meta / Llama 3 8B", "huggingface_hub/meta-llama/Meta-Llama-3-8B"),
    ("Meta / Llama 3 70B", "huggingface_hub/meta-llama/Meta-Llama-3-70B"),
    ("Meta / Llama 2 7B", "huggingface_hub/meta-llama/Llama-2-7b-hf"),
    ("Meta / Llama 2 13B", "huggingface_hub/meta-llama/Llama-2-13b-hf"),
    ("Meta / Llama 2 70B", "huggingface_hub/meta-llama/Llama-2-70b-hf"),
    ("Cohere / Command Light", "cohere/command-light"),
    ("Cohere / Command", "cohere/command"),
    ("Cohere / Command R", "cohere/command-r"),
    ("Cohere / Command R+", "cohere/command-r-plus"),
]
