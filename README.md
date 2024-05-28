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
    - [x] Definition of each indicator (check the use of tool tip in gradio ?)
    - [ ] Basic explanation of the methodology 
        - Why it depends on the number of tokens? (What is a token?)
        - What is taken into account? (usage, manufacturing for inference != training)
        - What hypotheses have we made?
    - [X] Explain how to reduce the impacts? What are good strategies? (Valentin)
- [X] Add more indicators like (km by car, kg of concrete, ...) we can use [impactco2.fr](https://impactco2.fr/). (Valentin)
    - To enrich !
- [ ] Call to actions: (Valentin) 
    - [X] Follow us on LinkedIn
    - Share the results of a simulation (e.g. export an image generated with plotly for instance?)
- [x] Add an advanced/expert tab
    - True number of tokens
    - Expose more inputs like the electricity mix
- [ ] Idea : "estimate a given prompt impact" function which allows to enter a prompt in a text field and estimate its impacts