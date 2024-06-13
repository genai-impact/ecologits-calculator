
HERO_TEXT = """
<div align="center">
  <a href="https://ecologits.ai/">
    <img style="max-height: 80px" alt="EcoLogits" src="https://raw.githubusercontent.com/genai-impact/ecologits/main/docs/assets/logo_light.png">
  </a>
</div>

<h1 align="center">🧮 EcoLogits Calculator</h1>
<div align="center">
  <p style="max-width: 500px; text-align: center">
    <i><b>EcoLogits</b> is a python library that tracks the <b>energy consumption</b> and <b>environmental 
    footprint</b> of using <b>generative AI</b> models through APIs.</i>
  </p>
</div>
<br>

This tool is developed and maintained by [GenAI Impact](https://genai-impact.org/) non-profit. Learn more about 
🌱 EcoLogits by reading the documentation on [ecologits.ai](https://ecologits.ai).
 
🩷 Support us by giving a ⭐️ on our [GitHub repository](https://github.com/genai-impact/ecologits) and by following our [LinkedIn page](https://www.linkedin.com/company/genai-impact/).
"""

ABOUT_TEXT = r"""
## 🎯 Our goal

**The main goal of the EcoLogits Calculator is to raise awareness on the environmental impacts of LLM inference.**

The rapid evolution of generative AI is reshaping numerous industries and aspects of our daily lives. While these 
advancements offer some benefits, they also **pose substantial environmental challenges that cannot be overlooked**. 
Plus the issue of AI's environmental footprint as been mainly discussed at training stage but rarely at the inference 
stage. That is an issue because **inference impacts for LLMs can largely overcome the training impacts when deployed 
at large scales**.

At **[GenAI Impact](https://genai-impact.org/) we are dedicated to understanding and mitigating the environmental 
impacts of generative AI** through rigorous research, innovative tools, and community engagement. Especially, in early 
2024 we have launched an new open-source tool called [EcoLogits](https://github.com/genai-impact/ecologits) that tracks
the energy consumption and environmental footprint of using generative AI models through APIs.

## 🙋 FAQ 

**Which generative AI models or providers are supported?**

To see the full list of **generative AI providers** currently supported by EcoLogits, see the following 
[documentation page](https://ecologits.ai/providers/). As of today we only support LLMs but we plan to add support for 
embeddings, image generation, multi-modal models and more. If you are interested don't hesitate to 
[join us](https://genai-impact.org/contact/) and accelerate our work!

**How to reduce AI environmental impacts?**

* Look at **indirect impacts** of your project. Does the finality of your project is impacting negatively the 
environment?
* **Be frugal** and question your usage or need of AI
    * Do you really need AI to solve your problem?
    * Do you really need GenAI to solve your problem? (you can read this [paper](https://aclanthology.org/2023.emnlp-industry.39.pdf))
    * Use small and specialized models to solve your problem.
    * Evaluate before, during and after the development of your project the environmental impacts with tools like 
    🌱 [EcoLogits](https://github.com/genai-impact/ecologits) or [CodeCarbon](https://github.com/mlco2/codecarbon) 
    (see [more tools](https://github.com/samuelrince/awesome-green-ai))
    * Restrict the use case and limit the usage of your tool or feature to the desired purpose.
* Do NOT buy new GPUs / hardware
    * Hardware manufacturing for data centers is around 50% of the impact.
* Use cloud instances that are located in low emissions / high energy efficiency data centers 
(see [electricitymaps.com](https://app.electricitymaps.com/map))
* Optimize your models for production
    * Quantize your models.
    * Use inference optimization tricks.
    * Prefer fine-tuning of small and existing models over generalist models.

**What is the difference between **EcoLogits** and [CodeCarbon](https://github.com/mlco2/codecarbon)?**

EcoLogits is focused on estimating the environmental impacts of generative AI (only LLMs for now) used **through API 
providers (such as OpenAI, Anthropic, Cloud APIs...)** whereas  CodeCarbon is more general tool to measure energy 
consumption and estimate GHG emissions measurement. If you deploy LLMs locally we encourage you to use CodeCarbon to 
get real numbers of your energy consumption.

## 🤗 Contributing 

We are eager to get feedback from the community, don't hesitate to engage the discussion with us on this 
[GitHub thread](https://github.com/genai-impact/ecologits/discussions/45) or message us on 
[LinkedIn](https://www.linkedin.com/company/genai-impact/).

We also welcome any open-source contributions on 🌱 **[EcoLogits](https://github.com/genai-impact/ecologits)** or on 
🧮 **EcoLogits Calculator**.

## ⚖️ License

<p xmlns:cc="http://creativecommons.org/ns#" >
  This work is licensed under 
  <a href="https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">
    CC BY-SA 4.0
  </a>
  <img style="display:inline-block;height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">
  <img style="display:inline-block;height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">
  <img style="display:inline-block;height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="">
</p>

## 🙌 Acknowledgement

We thank [Data For Good](https://dataforgood.fr/) and [Boavizta](https://boavizta.org/en) for supporting the 
development of this project. Their contributions of tools, best practices, and expertise in environmental impact 
assessment have been invaluable.

We also extend our gratitude to the open-source contributions of 🤗 [Hugging Face](huggingface.com) on the LLM-Perf 
Leaderboard.

## 🤝 Contact

For general question on the project, please use the [GitHub thread](https://github.com/genai-impact/ecologits/discussions/45). 
Otherwise use our contact form on [genai-impact.org/contact](https://genai-impact.org/contact/).
"""


METHODOLOGY_TEXT = r"""
## 📖 Methodology

We have developed a methodology to **estimate the energy consumption and environmental impacts for an LLM inference** 
based on request parameters and hypotheses on the data center location, the hardware used, the model architecture and
more.

In this section we will only cover the principles of the methodology related to the 🧮 **EcoLogits Calculator**. If 
you wish to learn more on the environmental impacts modeling of an LLM request checkout the 
🌱 [EcoLogits documentation page](https://ecologits.ai/methodology/).

### Modeling impacts of an LLM request

The environmental impacts of an LLM inference are split into the **usage impacts** $I_{request}^u$ to account for 
electricity consumption and the **embodied impacts** $I_{request}^e$ that relates to resource extraction, hardware 
manufacturing and transportation. In general terms it can be expressed as follow:

$$ I_{request} = I_{request}^u  + I_{request}^e $$

$$ I_{request} = E_{request}*F_{em}+\frac{\Delta T}{\Delta L}*I_{server}^e $$

With,

* $E_{request}$ the estimated energy consumption of the server and its cooling system.
* $F_{em}$ the electricity mix that depends on the country and time.
* $\frac{\Delta T}{\Delta L}$ the hardware usage ratio i.e. the computation time over the lifetime of the hardware.
* $I_{server}^e$ the embodied impacts of the server.

Additionally, to ⚡️ **direct energy consumption** the environmental impacts are expressed in **three dimensions 
(multi-criteria impacts)** that are:

* 🌍 **Global Warming Potential** (GWP): Potential impact on global warming in kgCO2eq (commonly known as GHG/carbon 
emissions).
* 🪨 **Abiotic Depletion Potential for Elements** (ADPe): Impact on the depletion of non-living resources such as 
minerals or metals in kgSbeq.
* ⛽️ **Primary Energy** (PE): Total energy consumed from primary sources in MJ.

### Principles, Data and Hypotheses

We use a **bottom-up methodology** to model impacts, meaning that we will estimate the impacts of low-level physical 
components to then estimate the impacts at software level (in that case an LLM inference). We also rely on **Life 
Cycle Approach (LCA) proxies and approach** to model both usage and embodied phases with multi-criteria impacts. 
If you are interested in this approach we recommend you to read the following [Boavizta](https://boavizta.org/) 
resources.

* [Digital & environment: How to evaluate server manufacturing footprint, beyond greenhouse gas emissions?](https://boavizta.org/en/blog/empreinte-de-la-fabrication-d-un-serveur) 
* [Boavizta API automated evaluation of environmental impacts of ICT services and equipments](https://boavizta.org/en/blog/boavizta-api-automated-evaluation-of-ict-impacts-on-the-environment)
* [Boavizta API documentation](https://doc.api.boavizta.org/)

We leverage **open data to estimate the environmental impacts**, here is an exhaustive list of our data providers.

* [LLM-Perf Leaderboard](https://huggingface.co/spaces/optimum/llm-perf-leaderboard) to estimate GPU energy consumption 
and latency based on the model architecture and number of output tokens.
* [Boavizta API](https://github.com/Boavizta/boaviztapi) to estimate server embodied impacts and base energy 
consumption.
* [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/) for electricity mix impacts per country.

Finally here are the **main hypotheses** we have made to compute the impacts.

* ⚠️ **We *"guesstimate"* the model architecture of proprietary LLMs when not disclosed by the provider.** 
* Production setup: quantized models running on data center grade servers and GPUs such as A100.
* Electricity mix does not depend on time (help us enhance EcoLogits and work on this [issue](https://github.com/genai-impact/ecologits/issues/42))
* Ignore the following impacts: unused cloud resources, data center building, network and end-user devices... (for now)

## Equivalents

### 🚶‍♂️‍➡️ Walking or 🏃‍♂️‍➡️ running distance

🔴 TODO

### 🔋 Electric Vehicle distance

🔴 TODO

### ⏯️ Streaming time

🔴 TODO

### Number of 💨 wind turbines or ☢️ nuclear plants

🔴 TODO

### Multiplier of 🇮🇪 Ireland electricity consumption

🔴 TODO

### Number of ✈️ Paris ↔ New York City flights

🔴 TODO

**If you are motivated to help us test and enhance this methodology 
[contact us](https://genai-impact.org/contact/)!** 💪
"""

CITATION_LABEL = "BibTeX citation for EcoLogits Calculator and the EcoLogits library:"
CITATION_TEXT = r"""@misc{ecologits-calculator,
  author={Samuel Rincé, Adrien Banse and Valentin Defour},
  title={EcoLogits Calculator},
  year={2024},
  howpublished= {\url{https://huggingface.co/spaces/genai-impact/ecologits-calculator}},
}
@software{ecologits,
  author = {Samuel Rincé, Adrien Banse, Vinh Nguyen and Luc Berton},
  publisher = {GenAI Impact},
  title = {EcoLogits: track the energy consumption and environmental footprint of using generative AI models through APIs.},
}"""

LICENCE_TEXT = """<p xmlns:cc="http://creativecommons.org/ns#" >
  This work is licensed under 
  <a href="https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">
    CC BY-SA 4.0
  </a>
  <img style="display:inline-block;height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">
  <img style="display:inline-block;height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">
  <img style="display:inline-block;height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="">
</p>"""
