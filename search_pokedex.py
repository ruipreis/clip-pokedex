import argparse
import textwrap

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from pokemon_finder import POKEMON_DICT, POKEMONS
from pokemon_finder.encoder import (
    ENCODING_DIM,
    encode_image,
    encode_pokemon,
    encode_text,
)
from pokemon_finder.vector_db import FaissManager


def get_pokemon_image(pokemon: str):
    return Image.open(POKEMON_DICT[pokemon])


def wrap_text(text, max_width):
    return "\n".join(textwrap.wrap(text, max_width))


def display_pokemon_images(original, similarities, pokemon_names, num_columns=5, image_path:str="pokemon.png"):
    num_images = len(pokemon_names) + 1  # +1 for the original
    num_rows = int(np.ceil(num_images / num_columns))
    fig, axes = plt.subplots(
        num_rows, num_columns, figsize=(3 * num_columns, 3 * num_rows)
    )
    plt.subplots_adjust(hspace=0.5)

    # Flatten the axes array for easy indexing and turn off all axes initially
    axes = axes.flatten()
    for ax in axes:
        ax.axis("off")

    # Display the original Pokémon image or text
    if isinstance(original, Image.Image):
        axes[0].imshow(original)
    else:  # If the original is a string, display it as text
        wrapped_text = wrap_text(original, max_width=40)
        axes[0].text(
            0.5,
            0.5,
            wrapped_text,
            fontsize=12,
            ha="center",
            va="center",
            transform=axes[0].transAxes,
        )

    axes[0].set_title("Original")

    # Display similar Pokémon images with scores
    for i, (similarity, pokemon_name) in enumerate(zip(similarities, pokemon_names)):
        ax = axes[i + 2]  # Start placing after separator
        img = get_pokemon_image(pokemon_name)
        ax.imshow(img)
        ax.set_title(f"{pokemon_name}\nScore: {similarity:.4f}")
        ax.axis("off")

    # Turn off remaining axes if there are any
    for ax in axes[len(pokemon_names) + 2 :]:
        ax.axis("off")

    if image_path is not None:
        plt.savefig(image_path, bbox_inches='tight')
        plt.close(fig)
    else:  
        plt.show()
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find similar Pokémon using FAISS.")
    parser.add_argument("--pokemon", help="Name of the Pokémon to find similar ones")
    parser.add_argument("--image", help="Path to the image to find similar Pokémon")
    parser.add_argument("--text", help="Text to find similar Pokémon")
    parser.add_argument(
        "--index", default="pokedex.idx", help="Path to the FAISS index file"
    )
    parser.add_argument(
        "--N", type=int, default=8, help="Number of similar Pokémon results to display"
    )
    args = parser.parse_args()

    pokedex = FaissManager(ENCODING_DIM)
    pokedex.load_index(args.index)

    if args.pokemon:
        original_pokemon = args.pokemon
        pokemon_image, original_vector = encode_pokemon(original_pokemon)
    elif args.image:
        original_pokemon = "UNKNOWN"
        pokemon_image, original_vector = encode_image(args.image)
    elif args.text:
        original_pokemon = f"'{args.text}'"
        pokemon_image = args.text
        original_vector = encode_text(args.text)

    pokemon_similarity, pokemon_indices = pokedex.search(original_vector, args.N)
    pokemon_names = [POKEMONS[i] for i in pokemon_indices[0]]
    similarities = pokemon_similarity[0]

    print(f"Similar Pokémon to {original_pokemon}: {pokemon_names}")

    # Display images
    display_pokemon_images(pokemon_image, similarities, pokemon_names)
