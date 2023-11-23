from pathlib import Path

import torch

POKEMON_PATH = (
    Path(__file__).absolute().parent.parent / "pokemons"
)

POKEMON_DICT = {v.stem: v for v in POKEMON_PATH.glob("*.png")}

POKEMONS = sorted(list(POKEMON_DICT.keys()))

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
