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
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "o1",
    "o1-mini",
    "o3-mini",
    "gpt-4.1-nano",
    "gpt-4.1-mini",
    "gpt-4.1",
    "o4-mini",
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-5",
]

main_models_anthropic = [
    "claude-3-5-haiku-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-7-sonnet-latest",
    "claude-opus-4-0",
    "claude-opus-4-1",
    "claude-sonnet-4-0",
    "claude-sonnet-4-5",
    "claude-haiku-4-5"
]

main_models_cohere = [
    "command-a-03-2025",
    "command-r",
    "command-r-08-2024",
    "command-r-plus-08-2024",
    "command-r7b-12-2024"
]

main_models_google = [
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemma-3-1b-it",
    "gemma-3-4b-it",
    "gemma-3-12b-it",
    "gemma-3-27b-it"
]

main_models_mistral = [
    "codestral-latest",
    "devstral-medium-latest",
    "devstral-small-latest",
    "magistral-medium-latest",
    "magistral-small-latest",
    "ministral-3b-latest",
    "ministral-8b-latest",
    "mistral-large-latest",
    "mistral-medium-latest",
    "mistral-small-latest",
    "mistral-tiny-latest",
    "open-mistral-7b",
    "open-mistral-nemo",
    "open-mixtral-8x22b",
    "open-mixtral-8x7b"
]

MAIN_MODELS = (
    main_models_openai
    + main_models_anthropic
    + main_models_cohere
    + main_models_mistral
    + main_models_google
)
