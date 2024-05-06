---
title: EcoLogits Calculator
emoji: 🌱
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: 4.26.0
app_file: app.py
pinned: true
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


To do:

- [ ] Add a tab with basic documentation
    - [ ] Definition of each indicator
    - [ ] Basic explanation of the methodology
        - Why it depends on the number of tokens? (What is a token?)
        - What is taken into account? (usage, manufacturing for inference != training)
        - What hypotheses have we made?
    - [ ] Explain how to reduce the impacts? What are good strategies?
- [ ] Add more indicators like (km by car, kg of concrete, ...) we can use [impactco2.fr](https://impactco2.fr/).
- [ ] Call to actions: 
    - Follow us on LinkedIn
    - Share the results of a simulation (e.g. export an image generated with plotly for instance?)
- [ ] Add an advanced/expert tab
    - Expose more inputs like the electricity mix
