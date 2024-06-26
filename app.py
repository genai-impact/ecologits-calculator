import gradio as gr

from ecologits.tracers.utils import compute_llm_impacts, _avg
from ecologits.impacts.llm import compute_llm_impacts as compute_llm_impacts_expert
from ecologits.impacts.llm import IF_ELECTRICITY_MIX_GWP, IF_ELECTRICITY_MIX_ADPE, IF_ELECTRICITY_MIX_PE
from ecologits.model_repository import models

from src.assets import custom_css
from src.electricity_mix import COUNTRY_CODES, find_electricity_mix
from src.content import (
    HERO_TEXT,
    ABOUT_TEXT,
    CITATION_LABEL,
    CITATION_TEXT,
    LICENCE_TEXT, METHODOLOGY_TEXT
)
from src.constants import (
    PROVIDERS,
    OPENAI_MODELS,
    ANTHROPIC_MODELS,
    COHERE_MODELS,
    META_MODELS,
    MISTRALAI_MODELS,
    PROMPTS,
    CLOSED_SOURCE_MODELS,
    MODELS,
)
from src.utils import (
    format_impacts,
    format_energy_eq_physical_activity,
    PhysicalActivity,
    format_energy_eq_electric_vehicle,
    format_gwp_eq_streaming, format_energy_eq_electricity_production, EnergyProduction,
    format_gwp_eq_airplane_paris_nyc, format_energy_eq_electricity_consumption_ireland
)

CUSTOM = "Custom"


def model_list(provider: str) -> gr.Dropdown:
    if provider == "openai":
        return gr.Dropdown(
            OPENAI_MODELS,
            label="Model",
            value=OPENAI_MODELS[0][1],
            filterable=True,
        )
    elif provider == "anthropic":
        return gr.Dropdown(
            ANTHROPIC_MODELS,
            label="Model",
            value=ANTHROPIC_MODELS[0][1],
            filterable=True,
        )
    elif provider == "cohere":
        return gr.Dropdown(
            COHERE_MODELS,
            label="Model",
            value=COHERE_MODELS[0][1],
            filterable=True,
        )
    elif provider == "huggingface_hub/meta":
        return gr.Dropdown(
            META_MODELS,
            label="Model",
            value=META_MODELS[0][1],
            filterable=True,
        )
    elif provider == "mistralai":
        return gr.Dropdown(
            MISTRALAI_MODELS,
            label="Model",
            value=MISTRALAI_MODELS[0][1],
            filterable=True,
        )


def custom():
    return CUSTOM


def model_active_params_fn(model_name: str, n_param: float):
    if model_name == CUSTOM:
        return n_param
    provider, model_name = model_name.split('/', 1)
    model = models.find_model(provider=provider, model_name=model_name)
    return model.active_parameters or _avg(model.active_parameters_range)


def model_total_params_fn(model_name: str, n_param: float):
    if model_name == CUSTOM:
        return n_param
    provider, model_name = model_name.split('/', 1)
    model = models.find_model(provider=provider, model_name=model_name)
    return model.total_parameters or _avg(model.total_parameters_range)


def mix_fn(country_code: str, mix_adpe: float, mix_pe: float, mix_gwp: float):
    if country_code == CUSTOM:
        return mix_adpe, mix_pe, mix_gwp
    return find_electricity_mix(country_code)


with gr.Blocks(css=custom_css) as demo:
    gr.Markdown(HERO_TEXT)

    with gr.Tab("🧮 Calculator"):
        with gr.Row():
            gr.Markdown("# Estimate the environmental impacts of LLM inference")
        with gr.Row():
            input_provider = gr.Dropdown(
                PROVIDERS,
                label="Provider",
                value=PROVIDERS[0][1],
                filterable=True,
            )

            input_model = gr.Dropdown(
                OPENAI_MODELS,
                label="Model",
                value=OPENAI_MODELS[0][1],
                filterable=True,
            )
            input_provider.change(model_list, input_provider, input_model)

            input_prompt = gr.Dropdown(
                PROMPTS,
                label="Example prompt",
                value=400,
            )


        @gr.render(inputs=[input_provider, input_model, input_prompt])
        def render_simple(provider, model, prompt):
            if provider.startswith("huggingface_hub"):
                provider = provider.split("/")[0]
            if models.find_model(provider, model) is not None:
                impacts = compute_llm_impacts(
                    provider=provider,
                    model_name=model,
                    output_token_count=prompt,
                    request_latency=100000
                )
                impacts = format_impacts(impacts)

                # Inference impacts
                with gr.Blocks():
                    if f"{provider}/{model}" in CLOSED_SOURCE_MODELS:
                        with gr.Row():
                            gr.Markdown("""<p> ⚠️ You have selected a closed-source model. Please be aware that 
                            some providers do not fully disclose information about such models. Consequently, our 
                            estimates have a lower precision for closed-source models. For further details, refer to 
                            our FAQ in the About section.
                            </p>""", elem_classes="warning-box")

                    with gr.Row():
                        gr.Markdown("""
                        ## Environmental impacts
                        
                        To understand how the environmental impacts are computed go to the 📖 Methodology tab. 
                        """)
                    with gr.Row():
                        with gr.Column(scale=1, min_width=220):
                            gr.Markdown(f"""
                            <h2 align="center">⚡️ Energy</h2>
                            $$ \Large {impacts.energy.magnitude:.3g} \ \large {impacts.energy.units} $$
                            <p align="center"><i>Evaluates the electricity consumption<i></p><br>
                            """)
                        with gr.Column(scale=1, min_width=220):
                            gr.Markdown(f"""
                            <h2 align="center">🌍️ GHG Emissions</h2>
                            $$ \Large {impacts.gwp.magnitude:.3g} \ \large {impacts.gwp.units} $$
                            <p align="center"><i>Evaluates the effect on global warming<i></p><br>
                            """)
                        with gr.Column(scale=1, min_width=220):
                            gr.Markdown(f"""
                            <h2 align="center">🪨 Abiotic Resources</h2>
                            $$ \Large {impacts.adpe.magnitude:.3g} \ \large {impacts.adpe.units} $$
                            <p align="center"><i>Evaluates the use of metals and minerals<i></p><br>
                            """)
                        with gr.Column(scale=1, min_width=220):
                            gr.Markdown(f"""
                            <h2 align="center">⛽️ Primary Energy</h2>
                            $$ \Large {impacts.pe.magnitude:.3g} \ \large {impacts.pe.units} $$
                            <p align="center"><i>Evaluates the use of energy resources<i></p><br>
                            """)

                # Impacts equivalents
                with gr.Blocks():
                    with gr.Row():
                        gr.Markdown("""
                        ---
                        ## That's equivalent to...
                        
                        Making this request to the LLM is equivalent to the following actions.
                        """)
                    with gr.Row():
                        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy)
                        if physical_activity == PhysicalActivity.WALKING:
                            physical_activity = "🚶 " + physical_activity.capitalize()
                        if physical_activity == PhysicalActivity.RUNNING:
                            physical_activity = "🏃 " + physical_activity.capitalize()
                        with gr.Column(scale=1, min_width=300):
                            gr.Markdown(f"""
                            <h2 align="center">{physical_activity} $$ \Large {distance.magnitude:.3g}\ {distance.units} $$ </h2>
                            <p align="center"><i>Based on energy consumption<i></p><br>
                            """, latex_delimiters=[{"left": "$$", "right": "$$", "display": False}])

                        ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
                        with gr.Column(scale=1, min_width=300):
                            gr.Markdown(f"""
                            <h2 align="center">🔋 Electric Vehicle $$ \Large {ev_eq.magnitude:.3g}\ {ev_eq.units} $$ </h2>
                            <p align="center"><i>Based on energy consumption<i></p><br>
                            """, latex_delimiters=[{"left": "$$", "right": "$$", "display": False}])

                        streaming_eq = format_gwp_eq_streaming(impacts.gwp)
                        with gr.Column(scale=1, min_width=300):
                            gr.Markdown(f"""
                            <h2 align="center">⏯️ Streaming $$ \Large {streaming_eq.magnitude:.3g}\ {streaming_eq.units} $$ </h2>
                            <p align="center"><i>Based on GHG emissions<i></p><br>
                            """, latex_delimiters=[{"left": "$$", "right": "$$", "display": False}])

                # Bigger scale impacts equivalent
                with gr.Blocks():
                    with gr.Row():
                        gr.Markdown("""
                        ## What if 1% of the planet does this request everyday for 1 year?
                        
                        If this use case is largely deployed around the world the equivalent impacts would be. (The 
                        impacts of this request x 1% of 8 billion people x 365 days in a year.)
                        """)
                    with gr.Row():
                        electricity_production, count = format_energy_eq_electricity_production(impacts.energy)
                        if electricity_production == EnergyProduction.NUCLEAR:
                            emoji = "☢️"
                            name = "Nuclear power plants"
                        if electricity_production == EnergyProduction.WIND:
                            emoji = "💨️ "
                            name = "Wind turbines"
                        with gr.Column(scale=1, min_width=300):
                            gr.Markdown(f"""
                            <h2 align="center">{emoji} $$ \Large {count:.0f} $$ {name} <span style="font-size: 12px">(yearly)</span></h2>
                            <p align="center"><i>Based on electricity consumption<i></p><br>
                            """, latex_delimiters=[{"left": "$$", "right": "$$", "display": False}])

                        ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
                        with gr.Column(scale=1, min_width=300):
                            gr.Markdown(f"""
                            <h2 align="center">🇮🇪 $$ \Large {ireland_count:.2g} $$ x Ireland <span style="font-size: 12px">(yearly ⚡️ cons.)</span></h2>
                            <p align="center"><i>Based on electricity consumption<i></p><br>
                            """, latex_delimiters=[{"left": "$$", "right": "$$", "display": False}])

                        paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
                        with gr.Column(scale=1, min_width=300):
                            gr.Markdown(f"""
                            <h2 align="center">✈️ $$ \Large {paris_nyc_airplane:,.0f} $$ Paris ↔ NYC </h2>
                            <p align="center"><i>Based on GHG emissions<i></p><br>
                            """, latex_delimiters=[{"left": "$$", "right": "$$", "display": False}])

    with gr.Tab("🤓 Expert Mode"):
        with gr.Row():
            gr.Markdown("# 🤓 Expert mode")
        model = gr.Dropdown(
            MODELS + [CUSTOM],
            label="Model name",
            value="openai/gpt-3.5-turbo",
            filterable=True,
            interactive=True
        )
        input_model_active_params = gr.Number(
            label="Number of billions of active parameters",
            value=45.0,
            interactive=True
        )
        input_model_total_params = gr.Number(
            label="Number of billions of total parameters",
            value=45.0,
            interactive=True
        )

        model.change(fn=model_active_params_fn,
                     inputs=[model, input_model_active_params],
                     outputs=[input_model_active_params])
        model.change(fn=model_total_params_fn,
                     inputs=[model, input_model_total_params],
                     outputs=[input_model_total_params])
        input_model_active_params.input(fn=custom, outputs=[model])
        input_model_total_params.input(fn=custom, outputs=[model])

        input_tokens = gr.Number(
            label="Output tokens",
            value=100
        )

        mix = gr.Dropdown(
            COUNTRY_CODES + [CUSTOM],
            label="Location",
            value="WOR",
            filterable=True,
            interactive=True
        )
        input_mix_gwp = gr.Number(
            label="Electricity mix - GHG emissions [kgCO2eq / kWh]",
            value=IF_ELECTRICITY_MIX_GWP,
            interactive=True
        )
        input_mix_adpe = gr.Number(
            label="Electricity mix - Abiotic resources [kgSbeq / kWh]",
            value=IF_ELECTRICITY_MIX_ADPE,
            interactive=True
        )
        input_mix_pe = gr.Number(
            label="Electricity mix - Primary energy [MJ / kWh]",
            value=IF_ELECTRICITY_MIX_PE,
            interactive=True
        )

        mix.change(fn=mix_fn,
                   inputs=[mix, input_mix_adpe, input_mix_pe, input_mix_gwp],
                   outputs=[input_mix_adpe, input_mix_pe, input_mix_gwp])
        input_mix_gwp.input(fn=custom, outputs=mix)
        input_mix_adpe.input(fn=custom, outputs=mix)
        input_mix_pe.input(fn=custom, outputs=mix)


        @gr.render(inputs=[
            input_model_active_params,
            input_model_total_params,
            input_tokens,
            input_mix_gwp,
            input_mix_adpe,
            input_mix_pe
        ])
        def render_expert(
                model_active_params,
                model_total_params,
                tokens,
                mix_gwp,
                mix_adpe,
                mix_pe
        ):
            impacts = compute_llm_impacts_expert(
                model_active_parameter_count=model_active_params,
                model_total_parameter_count=model_total_params,
                output_token_count=tokens,
                request_latency=100000,
                if_electricity_mix_gwp=mix_gwp,
                if_electricity_mix_adpe=mix_adpe,
                if_electricity_mix_pe=mix_pe
            )
            impacts = format_impacts(impacts)

            with gr.Blocks():
                with gr.Row():
                    gr.Markdown("## Environmental impacts")
                with gr.Row():
                    with gr.Column(scale=1, min_width=220):
                        gr.Markdown(f"""
                        <h2 align="center">⚡️ Energy</h2>
                        $$ \Large {impacts.energy.magnitude:.3g} \ \large {impacts.energy.units} $$
                        <p align="center"><i>Evaluates the electricity consumption<i></p><br>
                        """)
                    with gr.Column(scale=1, min_width=220):
                        gr.Markdown(f"""
                        <h2 align="center">🌍️ GHG Emissions</h2>
                        $$ \Large {impacts.gwp.magnitude:.3g} \ \large {impacts.gwp.units} $$
                        <p align="center"><i>Evaluates the effect on global warming<i></p><br>
                        """)
                    with gr.Column(scale=1, min_width=220):
                        gr.Markdown(f"""
                        <h2 align="center">🪨 Abiotic Resources</h2>
                        $$ \Large {impacts.adpe.magnitude:.3g} \ \large {impacts.adpe.units} $$
                        <p align="center"><i>Evaluates the use of metals and minerals<i></p><br>
                        """)
                    with gr.Column(scale=1, min_width=220):
                        gr.Markdown(f"""
                        <h2 align="center">⛽️ Primary Energy</h2>
                        $$ \Large {impacts.pe.magnitude:.3g} \ \large {impacts.pe.units} $$
                        <p align="center"><i>Evaluates the use of energy resources<i></p><br>
                        """)

    with gr.Tab("📖 Methodology"):
        gr.Markdown(METHODOLOGY_TEXT,
                    elem_classes="descriptive-text",
                    latex_delimiters=[
                        {"left": "$$", "right": "$$", "display": True},
                        {"left": "$", "right": "$", "display": False}
                    ])

    with gr.Tab("ℹ️ About"):
        gr.Markdown(ABOUT_TEXT, elem_classes="descriptive-text",)

    with gr.Accordion("📚 Citation", open=False):
        gr.Textbox(
            value=CITATION_TEXT,
            label=CITATION_LABEL,
            interactive=False,
            show_copy_button=True,
            lines=len(CITATION_TEXT.split('\n')),
        )

    # License
    gr.Markdown(LICENCE_TEXT)

if __name__ == '__main__':
    demo.launch()
