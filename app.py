import gradio as gr
from ecologits.tracers.utils import compute_llm_impacts
from pint import UnitRegistry

u = UnitRegistry()
u.define('kWh = kilowatt_hour')
u.define('Wh = watt_hour')
u.define('gCO2eq = gram')
u.define('kgCO2eq = kilogram')
u.define('kgSbeq = kilogram')
u.define('MJ = megajoule')
u.define('kJ = kilojoule')
q = u.Quantity


MODELS = [
    ("OpenAI / GPT-3.5-Turbo", "openai/gpt-3.5-turbo"),
    ("OpenAI / GPT-4", "openai/gpt-4"),
    ("Anthropic / Claude 3 Opus", "anthropic/claude-3-opus-20240229"),
    ("Anthropic / Claude 3 Sonnet", "anthropic/claude-3-sonnet-20240229"),
    ("Anthropic / Claude 3 Haiku", "anthropic/claude-3-haiku-20240307"),
    ("Anthropic / Claude 2.1", "anthropic/claude-2.1"),
    ("Anthropic / Claude 2", "anthropic/claude-2"),
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


PROMPTS = [
    ("Write an email", 170),
    ("Write an article summary", 250),
    ("Write a Tweet", 50),
    ("Write a report of 5 pages", 5000),
    ("Small conversation with a chatbot", 400)
]


def format_indicator(name: str, value: str, unit: str) -> str:
    return f"""
    ## {name}
    $$ \LARGE {value} \ \large {unit} $$
    """


def form(
    model_name: str,
    prompt_generated_tokens: int,
):
    provider, model_name = model_name.split('/', 1)
    impacts = compute_llm_impacts(
        provider=provider,
        model_name=model_name,
        output_token_count=prompt_generated_tokens,
        request_latency=100000
    )
    energy_ = q(impacts.energy.value, impacts.energy.unit)
    if energy_ < q("1 kWh"):
        energy_ = energy_.to("Wh")
    gwp_ = q(impacts.gwp.value, impacts.gwp.unit)
    if gwp_ < q("1 kgCO2eq"):
        gwp_ = gwp_.to("1 gCO2eq")
    adpe_ = q(impacts.adpe.value, impacts.adpe.unit)
    pe_ = q(impacts.pe.value, impacts.pe.unit)
    if pe_ < q("1 MJ"):
        pe_ = pe_.to("kJ")
    return (
        format_indicator("⚡️ Energy", f"{energy_.magnitude:.3g}", energy_.units),
        format_indicator("🌍 GHG Emissions", f"{gwp_.magnitude:.3g}", gwp_.units),
        format_indicator("🪨 Abiotic Resources", f"{adpe_.magnitude:.3g}", adpe_.units),
        format_indicator("⛽️ Primary Energy", f"{pe_.magnitude:.3g}", pe_.units),
    )


with gr.Blocks() as demo:
    gr.Markdown("""
    # 🌱 EcoLogits Calculator
    
    **EcoLogits** is a python library that tracks the **energy consumption** and **environmental footprint** of using 
    **generative AI** models through APIs.

    ⭐️ us on GitHub: [genai-impact/ecologits](https://github.com/genai-impact/ecologits) | Read the documentation: 
    [ecologits.ai](https://ecologits.ai)
    """)

    with gr.Row():
        model = gr.Dropdown(
            MODELS,
            label="Model name",
            value="openai/gpt-3.5-turbo",
            filterable=True,
        )
        prompt = gr.Dropdown(
            PROMPTS,
            label="Prompt",
            value=170
        )

    with gr.Row():
        energy = gr.Markdown(
            label="energy",
            latex_delimiters=[{"left": "$$", "right": "$$", "display": False}]
        )
        gwp = gr.Markdown(
            label="gwp",
            latex_delimiters=[{"left": "$$", "right": "$$", "display": False}]
        )
        adpe = gr.Markdown(
            label="adpe",
            latex_delimiters=[{"left": "$$", "right": "$$", "display": False}]
        )
        pe = gr.Markdown(
            label="pe",
            latex_delimiters=[{"left": "$$", "right": "$$", "display": False}]
        )

    btn = gr.Button("Submit")
    btn.click(fn=form, inputs=[model, prompt], outputs=[energy, gwp, adpe, pe])


if __name__ == '__main__':
    demo.launch()
