from io import BytesIO
from os import path as ospath
from pathlib import Path
from sys import path as syspath

import clip
import requests
import torch
from PIL import Image

from .constants import DEVICE, POKEMON_DICT

CLIP_MODEL, CLIP_PREPROCESS = clip.load("ViT-B/32", device=DEVICE)

ENCODING_DIM = 512


def encode_pokemon(pokemon_name: str):
    assert pokemon_name in POKEMON_DICT.keys(), f"Pokemon {pokemon_name} not found"
    pokemon_path = POKEMON_DICT[pokemon_name]
    return encode_image(pokemon_path)


def encode_image(image_path: str):
    if str(image_path).startswith("https://"):
        response = requests.get(image_path)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        src_image = Image.open(BytesIO(response.content))
    else:
        src_image = Image.open(image_path)

    image = CLIP_PREPROCESS(src_image).unsqueeze(0).to(DEVICE)
    return src_image, CLIP_MODEL.encode_image(image).squeeze(0).cpu().detach().numpy()


def encode_text(text: str):
    return (
        CLIP_MODEL.encode_text(clip.tokenize(text).to(DEVICE))
        .squeeze(0)
        .cpu()
        .detach()
        .numpy()
    )
