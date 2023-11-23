# CLIP Pokedex

Toy example using CLIP for similarity search.

# Usage

## Build the Pokedex index

```bash
python build_pokedex.py
```

## Search your favorite Pokemon

It's possible to search by text, images, or by finding the most similar Pokemons to a known one.

```bash
python search_pokedex.py --text "geometric"
```

This example shows a plot with the closest Pokemon and the following output text:

```bash
Similar Pokémon to 'geometric': ['cryogonal', 'porygon', 'roggenrola', 'cosmoem', 'minior-red-meteor']
```