from typing import Optional
import gradio as gr
from pint import UnitRegistry

from ecologits.tracers.utils import compute_llm_impacts, _avg
from ecologits.impacts.llm import compute_llm_impacts as compute_llm_impacts_expert
from ecologits.impacts.llm import IF_ELECTRICITY_MIX_GWP, IF_ELECTRICITY_MIX_ADPE, IF_ELECTRICITY_MIX_PE
from ecologits.model_repository import models

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
    ("Write a Tweet", 50),
    ("Write an email", 170),
    ("Write an article summary", 250),
    ("Small conversation with a chatbot", 400),
    ("Write a report of 5 pages", 5000),
]
PROMPTS = [(s + f" ({v} output tokens)", v) for (s, v) in PROMPTS]


def format_indicator(name: str, value: str, unit: str) -> str:
    return f"""
    ## {name}
    $$ \LARGE {value} \ \large {unit} $$
    """


def form_output(impacts):
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


def form(
    model_name: str,
    prompt_generated_tokens: int
):
    provider, model_name = model_name.split('/', 1)
    impacts = compute_llm_impacts(
        provider=provider,
        model_name=model_name,
        output_token_count=prompt_generated_tokens,
        request_latency=100000
    )
    return form_output(impacts)


def form_expert(
    model_name: str,
    prompt_generated_tokens: int,
    mix_gwp: float,
    mix_adpe: float,
    mix_pe: float
):
    provider, model_name = model_name.split('/', 1)
    model = models.find_model(provider=provider, model_name=model_name)
    model_active_params = model.active_parameters or _avg(model.active_parameters_range)    # TODO: handle ranges
    model_total_params = model.total_parameters or _avg(model.total_parameters_range)
    impacts = compute_llm_impacts_expert(
        model_active_parameter_count=model_active_params,
        model_total_parameter_count=model_total_params,
        output_token_count=prompt_generated_tokens,
        request_latency=100000, 
        if_electricity_mix_gwp=mix_gwp,
        if_electricity_mix_adpe=mix_adpe,
        if_electricity_mix_pe=mix_pe
    )
    return form_output(impacts)


with gr.Blocks() as demo:

### TITLE

    gr.Markdown("""
    # 🌱 EcoLogits Calculator
    
    **EcoLogits** is a python library that tracks the **energy consumption** and **environmental footprint** of using 
    **generative AI** models through APIs.

    Read the documentation: 
    [ecologits.ai](https://ecologits.ai) | ⭐️ us on GitHub: [genai-impact/ecologits](https://github.com/genai-impact/ecologits) 
    """)

### SIMPLE CALCULATOR

    gr.Markdown(""" 
    ## 😊 Calculator
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
            label="Example prompt",
            value=50
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

    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=form, inputs=[model, prompt], outputs=[energy, gwp, adpe, pe])

### EXPERT CALCULATOR

    gr.Markdown(""" 
    ## 🤓 Expert mode
    """)
    model = gr.Dropdown(
        MODELS,
        label="Model name",
        value="openai/gpt-3.5-turbo",
        filterable=True,
    )
    tokens = gr.Number(
        label="Output tokens", 
        value=100
    )
    mix_gwp = gr.Number(
        label="Electricity mix - GHG emissions [kgCO2eq / kWh]",
        value=IF_ELECTRICITY_MIX_GWP
    )
    mix_adpe = gr.Number(
        label="Electricity mix - Abiotic resources [kgSbeq / kWh]",
        value=IF_ELECTRICITY_MIX_ADPE
    )
    mix_pe = gr.Number(
        label="Electricity mix - Primary energy [MJ / kWh]",
        value=IF_ELECTRICITY_MIX_PE
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

    submit_btn = gr.Button("Submit")
    submit_btn.click(
        fn=form_expert, 
        inputs=[model, tokens, mix_gwp, mix_adpe, mix_pe], 
        outputs=[energy, gwp, adpe, pe]
    )

### INFORMATION ABOUT INDICATORS

    gr.Markdown("""
    ## 📊 More about the indicators

    - ⚡️ **Energy**: Final energy consumption, 
    - 🌍 **GHG Emissions**: Potential impact on global warming (commonly known as GHG/carbon emissions), 
    - 🪨 **Abiotic Resources**: Impact on the depletion of non-living resources such as minerals or metals, 
    - ⛽️ **Primary Energy**: Total energy consumed from primary sources.
    """)

if __name__ == '__main__':
    demo.launch()
