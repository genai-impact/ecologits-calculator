HERO_TEXT = """
<div align="center" class="hero">
  <a href="https://ecologits.ai/">
    <img style="max-height: 200px" alt="EcoLogits" src="https://raw.githubusercontent.com/genai-impact/ecologits-calculator/main/assets/logo.png">
  </a>
</div>
<div align="center">
  <p style="max-width: 850px; text-align: left">
    <b><a href="https://ecologits.ai/" target="_blank">EcoLogits</a></b> is an <b>open source</b> tool for estimating the <b>energy consumption</b> and <b>environmental footprint</b> when using <b>generative AI models</b>. It is developed by the <b><a href="https://genai-impact.org/">GenAI Impact</a></b> non-profit.
    <br><br>
    This page is the official calculator made for everyone to explore the impact evaluation methodology and raise awareness on sustainable AI.
  </p>

</div>
<br>
"""

HOW_TO_TEXT = """
Chose a provider, a model and an example of usage (prompts). 

1. The calculator will provide you estimates of environmental impacts of this example. To learn more about how these impacts are computed check the Methodology tab.

2. You can then check for equivalences of these impacts.

3. The calculator will extrapolate your example to simulate how impacts can scale rapidly if only one percent of the world population make the same prompt everyday for one year.


"""

WARNING_CLOSED_SOURCE = """
The model architecture has not been publicly released, expect lower precision of estimations.
"""

WARNING_MULTI_MODAL = """
The model architecture is multimodal, expect lower precision of estimations.
"""

WARNING_BOTH = """
The model architecture has not been publicly released and is multimodal, expect lower precision of estimations.
"""

TOKEN_ESTIMATOR_TEXT = """
A token is the basic unit of text that a language model processes. Think of it as a piece of text that the model breaks down for analysis and generation. Tokens can be:

1. Whole words
2. Parts of words
3. Punctuation marks
4. Spaces or other whitespace characters

For example, the sentence "I love EcoLogits!" might be tokenized like this:

- "I" (1 token)
- "love" (1 token)
- "EcoLogits" (1 token)
- "!" (1 token)

Different tokenization methods exist : some models split tokens at spaces wile others use more complex algorithms that break words into subwords.

Tokens are crucial because:

- They determine the model's input and output capacity
- They impact processing speed and memory usage
- Most LLMs have a maximum token limit (e.g., 4,000 or 8,000 tokens)
- Longer texts require more tokens, which can increase computational complexity
- At EcoLogits, they are at the core of our impact assessment methodology !

When you're writing or interacting with an LLM, being aware of token count can help you manage input length and complexity more effectively.
"""

ABOUT_TEXT = r"""
### 🎯 Our goal

**The main goal of the EcoLogits Calculator is to raise awareness on the environmental impacts of LLM inference.**

The rapid evolution of generative AI is reshaping numerous industries and aspects of our daily lives. While these advancements offer some benefits, they also **pose substantial environmental challenges that cannot be overlooked**. Plus the issue of AI's environmental footprint has been mainly discussed at training stage but rarely at the inference stage. That is an issue because **inference impacts for large langauge models (LLMs) can largely overcome the training impacts when deployed at large scales**.

At **[GenAI Impact](https://genai-impact.org/) we are dedicated to understanding and mitigating the environmental impacts of generative AI** through rigorous research, innovative tools, and community engagement. Especially, in early 2024 we have launched an new open-source tool called [EcoLogits](https://github.com/genai-impact/ecologits) that tracks the energy consumption and environmental footprint of using generative AI models through APIs.


### 🙋 FAQ 

**How we assess the impacts of closed-source models?**

Environmental impacts are calculated based on model architecture and parameter count. For closed-source models, we lack transparency from providers, so we estimate parameter counts using available information. For GPT models, we based our estimates on leaked GPT-4 architecture and scaled parameters count for GPT-4-Turbo and GPT-4o based on pricing differences. For other proprietary models like Anthropic's Claude, we assume similar impacts for models released around the same time with similar performance on public benchmarks. Please note that these estimates are based on assumptions and may not be exact. Our methods are open-source and transparent so you can always see the hypotheses we use.

**Which generative AI models or providers are supported?**

To see the full list of **generative AI providers** currently supported by EcoLogits, see the following [documentation page](https://ecologits.ai/providers/). As of today we only support LLMs but we plan to add support for embeddings, image generation, multi-modal models and more. If you are interested don't hesitate to [join us](https://genai-impact.org/contact/) and accelerate our work!

**How to reduce AI environmental impacts?**

* Look at **indirect impacts** of your project. Does the finality of your project is impacting negatively the environment?
* **Be frugal** and question your usage or need of AI
    * Do you really need AI to solve your problem?
    * Do you really need GenAI to solve your problem? (you can read this [paper](https://aclanthology.org/2023.emnlp-industry.39.pdf))
    * Use small and specialized models to solve your problem.
    * Evaluate before, during and after the development of your project the environmental impacts with tools like 🌱 [EcoLogits](https://github.com/genai-impact/ecologits) or [CodeCarbon](https://github.com/mlco2/codecarbon) (see [more tools](https://github.com/samuelrince/awesome-green-ai))
    * Restrict the use case and limit the usage of your tool or feature to the desired purpose.
* Do NOT buy new GPUs / hardware
    * Hardware manufacturing for data centers is around 50% of the impact.
* Use cloud instances that are located in low emissions / high energy efficiency data centers (see [electricitymaps.com](https://app.electricitymaps.com/map))
* Optimize your models for production
    * Quantize your models.
    * Use inference optimization tricks.
    * Prefer fine-tuning of small and existing models over generalist models.
    
**What is the difference between **EcoLogits** and [CodeCarbon](https://github.com/mlco2/codecarbon)?**

EcoLogits is focused on estimating the environmental impacts of generative AI (only LLMs for now) used **through API providers (such as OpenAI, Anthropic, Cloud APIs...)** whereas  CodeCarbon is more general tool to measure energy consumption and estimate GHG emissions measurement. If you deploy LLMs locally we encourage you to use CodeCarbon to get real numbers of your energy consumption.


### 🤗 Contributing 

We are eager to get feedback from the community, don't hesitate to engage the discussion with us on this [GitHub thread](https://github.com/genai-impact/ecologits/discussions/45) or message us on [LinkedIn](https://www.linkedin.com/company/genai-impact/).

We also welcome any open-source contributions on 🌱 **[EcoLogits](https://github.com/genai-impact/ecologits)** or on 🧮 **EcoLogits Calculator**.


### ⚖️ License

<p xmlns:cc="http://creativecommons.org/ns#" >
  This work is licensed under 
  <a href="https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">
    CC BY-SA 4.0
  </a>
</p>

### 🙌 Acknowledgement

We thank [Data For Good](https://dataforgood.fr/) and [Boavizta](https://boavizta.org/en) for supporting the development of this project. Their contributions of tools, best practices, and expertise in environmental impact assessment have been invaluable. 


### 🤝 Contact

For general question on the project, please use the [GitHub thread](https://github.com/genai-impact/ecologits/discussions/45). 
Otherwise use our contact form on [genai-impact.org/contact](https://genai-impact.org/contact/).
"""

SUPPORT_TEXT = r"""
### How to support us

At GenAI Impact, our projects are powered by the passion and dedication of our team. 
Since its first release in June 2024, this calculator has been **developed and maintained entirely on a volunteer basis by our members**.
We aim to keep this tool available as a free and open-source resource for the common good. We need your support to reach this goal, this is how you can help.

#### If you have 1 second

3 easy ways to help this project:
- Give a ❤️ like to this space
- Give a ⭐ to the EcoLogits repository on [GitHub](https://github.com/genai-impact/ecologits)
- Follow us on [LinkedIn](https://fr.linkedin.com/company/genai-impact)

#### If you have 5 minutes

Share your feedback, ask questions, help other members of the community !

Engage the discussion with us:
- Start a new discussion on this space or on this 
[GitHub thread](https://github.com/genai-impact/ecologits/discussions/45) 
- Use the contact form on [GenAI Impact website](https://genai-impact.org/contact/)
- message us on [LinkedIn](https://www.linkedin.com/company/genai-impact/).

#### If you have more to give

###### As an individual

We welcome any open source contribution ! You can :
- Contribute on **[EcoLogits](https://github.com/genai-impact/ecologits)** or on 
**EcoLogits Calculator**.
- Become a an active member of [GenAI Impact ](https://genai-impact.org/contact/) non profit. Get involved in our broader mission !


###### As an organization

If EcoLogits Calculator brings value to your organization, customers or communities you can help finance this project.
- Become a **sponsor**
- Become a **benefactor member** if you are a public sector or non-profit organization or a university.

Contact us on [GenAI Impact](https://genai-impact.org/contact/)
"""

METHODOLOGY_TEXT = r"""
### 📖 Methodology

We have developed a methodology to **estimate the energy consumption and environmental impacts for an LLM inference** based on request parameters and hypotheses on the data center location, the hardware used, the model architecture and more.

In this section we will only cover the principles of the methodology related to the 🧮 **EcoLogits Calculator**. If you wish to learn more on the environmental impacts modeling of an LLM request checkout the 🌱 [EcoLogits documentation page](https://ecologits.ai/methodology/).

#### Modeling impacts of an LLM request

The environmental impacts of an LLM inference are split into the **usage impacts** $I_{request}^u$ to account for electricity consumption and the **embodied impacts** $I_{request}^e$ that relates to resource extraction, hardware manufacturing and transportation. In general terms it can be expressed as follow:

$$ I_{request} = I_{request}^u  + I_{request}^e $$

$$ I_{request} = E_{request}*F_{em}+\frac{\Delta T}{\Delta L}*I_{server}^e $$

With,

* $E_{request}$ the estimated energy consumption of the server and its cooling system.
* $F_{em}$ the electricity mix that depends on the country and time.
* $\frac{\Delta T}{\Delta L}$ the hardware usage ratio i.e. the computation time over the lifetime of the hardware.
* $I_{server}^e$ the embodied impacts of the server.

Additionally, to ⚡️ **direct energy consumption** the environmental impacts are expressed in **three dimensions (multi-criteria impacts)** that are:

* 🌍 **Global Warming Potential** (GWP): Potential impact on global warming in kgCO2eq (commonly known as GHG/carbon emissions).
* 🪨 **Abiotic Depletion Potential for Elements** (ADPe): Impact on the depletion of non-living resources such as minerals or metals in kgSbeq.
* ⛽️ **Primary Energy** (PE): Total energy consumed from primary sources in MJ.
* ⛽️ **Water Consumption Footprint** (WCF): Water consumed by data centers and electricity generation power plants.

#### Principles, Data and Hypotheses

We use a **bottom-up methodology** to model impacts, meaning that we will estimate the impacts of low-level physical components to then estimate the impacts at software level (in that case an LLM inference). We also rely on **Life Cycle Approach (LCA) proxies and approach** to model both usage and embodied phases with multi-criteria impacts. If you are interested in this approach we recommend you to read the following [Boavizta](https://boavizta.org/) resources.

* [Digital & environment: How to evaluate server manufacturing footprint, beyond greenhouse gas emissions?](https://boavizta.org/en/blog/empreinte-de-la-fabrication-d-un-serveur) 
* [Boavizta API automated evaluation of environmental impacts of ICT services and equipments](https://boavizta.org/en/blog/boavizta-api-automated-evaluation-of-ict-impacts-on-the-environment)
* [Boavizta API documentation](https://doc.api.boavizta.org/)

We leverage **open data to estimate the environmental impacts**, here is an exhaustive list of our data providers.

* [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) to estimate GPU energy consumption and latency based on the model architecture and number of output tokens.
* [Boavizta API](https://github.com/Boavizta/boaviztapi) to estimate server embodied impacts and base energy consumption.
* [Our World in Data](https://ourworldindata.org/), [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/) and [World Resource Institute](https://www.wri.org/) for electricity mix impacts per country.

Finally here are the **main hypotheses** we have made to compute the impacts.

* ⚠️ **We *"guesstimate"* the model architecture of proprietary LLMs when not disclosed by the provider.** 
* Production setup: quantized models running on data center grade servers and GPUs such as H100.
* Electricity mixes are yearly averages.
* Ignore the following impacts: unused cloud resources, data center building, network and end-user devices... (for now)

### Equivalents

We have integrated impact equivalents to help people better understand the impacts and have reference points for standard use cases and everyday activities.

#### Request impacts

These equivalents are computed based on the request impacts only.

##### 🚶‍♂️‍➡️ Walking or 🏃‍♂️‍➡️ running distance

We compare the ⚡️ direct energy consumption with the energy consumption of someone 🚶‍♂️‍➡️ walking or 🏃‍♂️‍➡️ running. From [runningtools.com](https://www.runningtools.com/energyusage.htm) we consider the following energy values per physical activity (for someone weighing 70kg):

* 🚶‍♂️‍➡️ walking: $ 196\ kJ/km $ (speed of $ 3\ km/h $)
* 🏃‍♂️‍➡️ running: $ 294\ kJ/km $ (speed of $ 10\ km/h $)

We divide the request energy consumption by these values to compute the distance traveled. 

##### 🔋 Electric Vehicle distance

We compare the ⚡️ direct energy consumption with the energy consumer by a EV car. From [selectra.info](https://selectra.info/energie/actualites/insolite/consommation-vehicules-electriques-france-2040) or [tesla.com](https://www.tesla.com/fr_fr/support/power-consumption) we consider an average value of energy consumed per kilometer of: $ 0.17\ kWh/km $.

We divide the request energy consumption by this value to compute the distance driven by an EV. 

##### ⏯️ Streaming time

We compare the 🌍 GHG emissions of the request and of streaming a video. From [impactco2.fr](https://impactco2.fr/outils/comparateur?value=1&comparisons=streamingvideo), we consider that $ 1\ kgCO2eq $ is equivalent to $ 15.6\ h $ of streaming.

We multiply that value by the GHG emissions of the request to get an equivalent in hours of video streaming.

#### Scaled impacts

These equivalents are computed based on the request impacts scaled to a worldwide adoption use case. We imply that the same request is done 1% of the planet everyday for 1 year, and then compute impact equivalents.

$$
I_{scaled} = I_{request} * [1 \% \ \text{of}\ 8B\ \text{people on earth}] * 365\ \text{days}
$$

##### Number of 💨 wind turbines or ☢️ nuclear plants

We compare the ⚡️ direct energy consumption (scaled) by the energy production of wind turbines and nuclear power plants. From [ecologie.gouv.fr](https://www.ecologie.gouv.fr/eolien-terrestre) we consider that a $ 2\ MW $ wind turbine produces $ 4.2\ GWh $ a year. And from [edf.fr](https://www.edf.fr/groupe-edf/espaces-dedies/jeunes-enseignants/pour-les-jeunes/lenergie-de-a-a-z/produire-de-lelectricite/le-nucleaire-en-chiffres) we learn that a $ 900\ MW $ nuclear power plant produces $ 6\ TWh $ a year.

We divide the scaled energy consumption by these values to get the number of wind turbines or nuclear power plants needed.

##### Multiplier of 🇮🇪 Ireland electricity consumption

We compare the ⚡️ direct energy consumption (scaled) by the electricity consumption of Ireland per year. From [wikipedia.org](https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption) we consider the Ireland electricity consumption to be $ 33\ TWh $ a year for a population of 5M.

We divide the scaled energy consumption by this value to get the equivalent number of "Ireland countries".

##### Number of ✈️ Paris ↔ New York City flights

We compare the 🌍 GHG emissions (scaled) of the request and of a return flight Paris ↔ New York City. From [impactco2.fr](https://impactco2.fr/outils/comparateur?value=1&comparisons=&equivalent=avion-pny) we consider that a return flight Paris → New York City → Paris for one passenger emits $ 1,770\ kgCO2eq $ and we consider an overall average load of 100 passengers per flight.

We divide the scaled GHG emissions by this value to get the equivalent number of return flights.

##### If you are motivated to help us test and enhance this methodology [contact us](https://genai-impact.org/contact/)! 💪
"""

CITATION_LABEL = "BibTeX citation for EcoLogits Calculator and the EcoLogits library:"
CITATION_TEXT = """@misc{ecologits_calculator,
  author={Samuel Rincé, Adrien Banse, Valentin Defour, Caroline Jean-Pierre},
  title={EcoLogits Calculator},
  year={2025},
  howpublished= {\\url{https://huggingface.co/spaces/genai-impact/ecologits-calculator}},
}
@article{ecologits_paper,
  author = {Rincé, Samuel and Banse, Adrien},
  doi = {10.21105/joss.07471},
  journal = {Journal of Open Source Software},
  month = jul,
  number = {111},
  pages = {7471},
  title = {{EcoLogits: Evaluating the Environmental Impacts of Generative AI}},
  url = {https://joss.theoj.org/papers/10.21105/joss.07471},
  volume = {10},
  year = {2025}
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
