from tqdm import tqdm

from pokemon_finder import POKEMON_DICT, POKEMONS
from pokemon_finder.encoder import ENCODING_DIM, encode_pokemon
from pokemon_finder.vector_db import FaissManager

if __name__ == "__main__":
    pokedex = FaissManager(ENCODING_DIM)

    for pokemon in tqdm(POKEMONS):
        pokedex.add_vectors(encode_pokemon(pokemon))

    pokedex.save_index("pokedex.idx")
