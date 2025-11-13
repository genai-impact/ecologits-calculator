import json

import requests
import pandas as pd
import streamlit as st
from ecologits.model_repository import models as model_repository, ArchitectureTypes
from ecologits.status_messages import ModelArchNotReleasedWarning, ModelArchMultimodalWarning
from ecologits.utils.range_value import RangeValue

from src.constants import MODEL_REPOSITORY_URL, MAIN_MODELS


def clean_models_data(df, with_filter=True):
    dict_providers = {
        "google": "Google",
        "mistralai": "MistralAI",
        "meta-llama": "Meta",
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "cohere": "Cohere",
        "microsoft": "Microsoft",
        "mistral-community": "Mistral Community",
        "databricks": "Databricks",
    }

    models_to_keep = MAIN_MODELS

    df.drop("type", axis=1, inplace=True)

    df.loc[df["name"].str.contains("/"), "name_clean"] = (
        df.loc[df["name"].str.contains("/"), "name"].str.split("/").str[1]
    )
    df["name_clean"] = df["name_clean"].fillna(df["name"])
    df["name_clean"] = df["name_clean"].replace({"-": " ", "latest": ""}, regex=True)

    df.loc[df["provider"] == "huggingface_hub", "provider_clean"] = (
        df.loc[df["provider"] == "huggingface_hub", "name"].str.split("/").str[0]
    )
    df["provider_clean"] = df["provider_clean"].fillna(df["provider"])
    df["provider_clean"] = df["provider_clean"].replace(dict_providers, regex=True)

    df["architecture_type"] = df["architecture"].apply(lambda x: x["type"])
    df["architecture_parameters"] = df["architecture"].apply(lambda x: x["parameters"])
    df["total_parameters"] = df["architecture_parameters"].apply(
        lambda x: x["total"] if isinstance(x, dict) and "total" in x.keys() else x
    )
    df["active_parameters"] = df["architecture_parameters"].apply(
        lambda x: x["active"] if isinstance(x, dict) and "active" in x.keys() else x
    )

    df["warnings"] = (
        df["warnings"].apply(lambda x: ", ".join(x) if x else None).fillna("none")
    )
    df["warning_arch"] = df["warnings"].apply(lambda x: "model-arch-not-released" in x)
    df["warning_multi_modal"] = df["warnings"].apply(
        lambda x: "model-arch-multimodal" in x
    )

    if with_filter == True:
        df = df[df["name"].isin(models_to_keep)]

    return df[
        [
            "provider",
            "provider_clean",
            "name",
            "name_clean",
            "architecture_type",
            "architecture_parameters",
            "total_parameters",
            "active_parameters",
            "warning_arch",
            "warning_multi_modal",
        ]
    ]


PROVIDERS_FORMAT = {
    "anthropic": "Anthropic",
    "cohere": "Cohere",
    "google_genai": "Google",
    "mistralai": "Mistral AI",
    "openai": "OpenAI",
}


@st.cache_data
def load_models(filter_main=True) -> pd.DataFrame:
    data = []
    for m in model_repository.list_models():
        if filter_main and m.name not in MAIN_MODELS:
            continue    # Ignore "not main" models when filter is enabled

        if m.architecture.type == ArchitectureTypes.DENSE:
            if isinstance(m.architecture.parameters, RangeValue):
                total_parameters = dict(m.architecture.parameters)
            else:
                total_parameters = m.architecture.parameters
            active_parameters = total_parameters

        elif m.architecture.type == ArchitectureTypes.MOE:
            if isinstance(m.architecture.parameters.total, RangeValue):
                total_parameters = dict(m.architecture.parameters.total)
            else:
                total_parameters = m.architecture.parameters.total

            if isinstance(m.architecture.parameters.active, RangeValue):
                active_parameters = dict(m.architecture.parameters.active)
            else:
                active_parameters = m.architecture.parameters.active

        else:
            continue    # Ignore model

        warning_arch = False
        warning_multi_modal = False
        for w in m.warnings:
            if isinstance(w, ModelArchNotReleasedWarning):
                warning_arch = True
            if isinstance(w, ModelArchMultimodalWarning):
                warning_multi_modal = True

        data.append({
            "provider": m.provider.value,
            "provider_clean": PROVIDERS_FORMAT.get(m.provider.value, m.provider.value),
            "name": m.name,
            "name_clean": clean_model_name(m.name),
            "architecture_type": m.architecture.type.value,
            "total_parameters": total_parameters,
            "active_parameters": active_parameters,
            "warning_arch": warning_arch,
            "warning_multi_modal": warning_multi_modal,
        })

    return pd.DataFrame(data)


def clean_model_name(model_name: str) -> str:
    model_name = model_name.replace("latest", "")
    model_name = model_name.replace("-", " ")
    model_name = model_name.replace("_", " ")
    return model_name
