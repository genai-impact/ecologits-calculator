PROMPTS = [
    ("Write a Tweet", 50),
    ("Write an email", 170),
    ("Write an article summary", 250),
    ("Small conversation with a chatbot", 400),
    ("Write a report of 5 pages", 5000),
    ("Write the code for this app", 15000),
]
PROMPTS = [(s + f" ({v} output tokens)", v) for (s, v) in PROMPTS]

MODEL_REPOSITORY_URL = "https://raw.githubusercontent.com/genai-impact/ecologits/refs/heads/main/ecologits/data/models.json"

main_models_openai = [
    "chatgpt-4o-latest",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "o1",
    "o1-mini",
]

main_models_meta = [
    "meta-llama/Meta-Llama-3.1-8B",
    "meta-llama/Meta-Llama-3.1-70B",
    "meta-llama/Meta-Llama-3.1-405B",
    "meta-llama/Meta-Llama-3-8B",
    "meta-llama/Meta-Llama-3-70B",
    "meta-llama/Meta-Llama-3-70B",
    "meta-llama/Llama-2-7b",
    "meta-llama/Llama-2-13b",
    "meta-llama/Llama-2-70b",
    "meta-llama/CodeLlama-7b-hf",
    "meta-llama/CodeLlama-13b-hf",
    "meta-llama/CodeLlama-34b-hf",
    "meta-llama/CodeLlama-70b-hf",
]

main_models_msft = [
    "microsoft/phi-1",
    "microsoft/phi-1_5",
    "microsoft/Phi-3-mini-128k-instruct",
    "microsoft/Phi-3-small-128k-instruct",
    "microsoft/Phi-3-medium-128k-instruct",
]

main_models_anthropic = [
    "claude-2.0",
    "claude-2.1",
    "claude-3-5-haiku-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-7-sonnet-latest",
    "claude-3-haiku-20240307",
    "claude-3-opus-latest",
    "claude-3-sonnet-20240229",
]

main_models_cohere = [
    "c4ai-aya-expanse-8b",
    "c4ai-aya-expanse-32b",
    "command",
    "command-light",
    "command-r",
    "command-r-plus",
]

main_models_google = [
    "google/gemma-2-2b",
    "google/gemma-2-9b",
    "google/gemma-2-27b",
    "google/codegemma-2b",
    "google/codegemma-7b",
    "gemini-1.0-pro",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
]

main_models_databricks = [
    "databricks/dolly-v1-6b",
    "databricks/dolly-v2-12b",
    "databricks/dolly-v2-7b",
    "databricks/dolly-v2-3b",
    "databricks/dbrx-base",
]

main_models_mistral = [
    "mistralai/Mistral-7B-v0.3",
    "mistralai/Mixtral-8x7B-v0.1",
    "mistralai/Mixtral-8x22B-v0.1",
    "mistralai/Codestral-22B-v0.1",
    "mistralai/Mathstral-7B-v0.1",
    "ministral-3b-latest",
    "ministral-8b-latest",
    "mistral-tiny",
    "mistral-small",
    "mistral-medium",
    "mistral-large-latest",
]

MAIN_MODELS = (
    main_models_meta
    + main_models_openai
    + main_models_anthropic
    + main_models_cohere
    + main_models_msft
    + main_models_mistral
    + main_models_databricks
    + main_models_google
)
