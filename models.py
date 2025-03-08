import requests
import json
import pandas as pd
from src.constants import MODEL_REPOSITORY_URL

def clean_models_data(df):
    
    dict_providers = {
        'google': 'Google',
        'mistralai': 'MistralAI',
        'meta-llama': 'Meta',
        'openai': 'OpenAI',
        'anthropic': 'Anthropic',
        'cohere': 'Cohere',
        'microsoft': 'Microsoft',
        'mistral-community': 'Mistral Community',
        'databricks': 'Databricks'
    }
    
    df.drop('type', axis=1, inplace=True)

    df.loc[df['name'].str.contains('/'), 'name_clean'] = df.loc[df['name'].str.contains('/'), 'name'].str.split('/').str[1]
    df['name_clean'] = df['name_clean'].fillna(df['name'])
    df['name_clean'] = df['name_clean'].replace({'-': ' '}, regex = True)
    
    df.loc[df['provider'] == 'huggingface_hub', 'provider_clean'] = df.loc[df['provider'] == 'huggingface_hub', 'name'].str.split('/').str[0]
    df['provider_clean'] = df['provider_clean'].fillna(df['provider'])
    df['provider_clean'] = df['provider_clean'].replace(dict_providers, regex = True)
    
    df['architecture_type'] = df['architecture'].apply(lambda x: x['type'])
    df['architecture_parameters'] = df['architecture'].apply(lambda x: x['parameters'])
    
    df['warnings'] = df['warnings'].apply(lambda x: ', '.join(x) if x else None).fillna('none')
    df['warning_arch'] = df['warnings'].apply(lambda x: 'model-arch-not-released' in x)
    df['warning_multi_modal'] = df['warnings'].apply(lambda x: 'model-arch-multimodal' in x)
    
    return df[['provider', 'provider_clean', 'name', 'name_clean', 'architecture_type', 'architecture_parameters', 'warning_arch', 'warning_multi_modal']]

def load_models():

    resp = requests.get(MODEL_REPOSITORY_URL)
    data = json.loads(resp.text)
    df = pd.DataFrame(data['models'])

    return clean_models_data(df)

