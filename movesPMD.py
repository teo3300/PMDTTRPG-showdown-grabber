dataDir      = "data"
outputDir    = "output"

learnsetURL  = "https://play.pokemonshowdown.com/data/learnsets.json"
pokedexURL   = "https://play.pokemonshowdown.com/data/pokedex.json"

filePMD      = f"{dataDir}/Moves and Rare Qualities Sheet.xlsx"

import sys
from numpy import result_type
import pandas as pd;

# Utils functions {{{

def stop(*args):
    print(*args, file=sys.stderr)
    exit(1)

def sanitize(moveName):
    moveName = moveName.replace(' ','')
    moveName = moveName.replace('-','')
    return moveName.lower()

def fetchCachedJson(url):

    import os
    import json
    import gzip

    name = url.split('/')[-1]

    if os.path.isfile(f"./{dataDir}/{name}.gz"):
        with gzip.open(f"./{dataDir}/{name}.gz", "rt", encoding="utf-8") as file:
            return json.load(file)

    import requests
    r = requests.get(url);
    if r.status_code != 200:
        stop(f"Impossibile raggiungere {url}")
    data = r.json()
    with gzip.open(f"./{dataDir}/{name}.gz","wt", encoding="utf-8") as file:
        json.dump(data, file)
    return data

def _getEvos(pokemonName, pokedex):
    # If some evos exist
    if 'evos' in pokedex[pokemonName]:
        evos = pokedex[pokemonName]['evos']
        listEvos = []
        for evo in evos:
            # Collect all evos and their subsequent evos
            listEvos += _getEvos(sanitize(evo), pokedex) + [sanitize(evo)]
        return listEvos
    else:
        # Return an empty list
        return []

def _getPreEvo(pokemonName, pokedex):
    # If a prevo exists
    if 'prevo' in pokedex[pokemonName]:
        # return prevo + all its prevo line
        prevo = pokedex[pokemonName]['prevo']
        return _getPreEvo(sanitize(prevo), pokedex) + [sanitize(prevo)]
    else:
        # return an empty list
        return []

# Fetch whole evolution line
def getEvoLine(pokemonName, pokedex):
    queryRes = [pokemonName] + _getPreEvo(pokemonName, pokedex) + _getEvos(pokemonName, pokedex)
    print(f"Opzione \"evo\", utilizzo la linea evolutiva - {queryRes}")
    return queryRes
# }}}

def queryName(inputName, evo=False):

    # Fetch smogon data
    learnset = fetchCachedJson(learnsetURL)
    pokedex  = fetchCachedJson(pokedexURL)

    # Load PMD excel
    movesPMD = pd.read_excel(filePMD, sheet_name="Moves")
    rareQualitiesPMD = pd.read_excel(filePMD, sheet_name="Rare Qualities")

    # Get the pokemon name
    pokemonName = sanitize(inputName)

    # Check pokemon exists
    if not pokemonName in pokedex:
        stop(f"Non trovo \"{inputName}\" nel database di showdown")

    # If specified "evo" returns the whole evolution line
    queryNames = []
    if evo:
        queryNames = getEvoLine(pokemonName, pokedex)
    else:
        queryNames = [pokemonName]

    # Compute learnset of a query
    queryLearnset = set()
    for name in queryNames:
        pokemonLearnset = set(learnset[name]['learnset'].keys())
        queryLearnset = queryLearnset | pokemonLearnset

    # Define filter for the moves: retains
    # - non string lines (blank/numbers?)
    # - strings that, when sanitized, are in the queryLearnset (learnset of a pokemon or an evoline)
    moveFilter = lambda x: not isinstance(x, str) or sanitize(x) in queryLearnset

    # Apply query filter
    resultMoves = movesPMD.loc[movesPMD['[Name]'].apply(moveFilter)]
    resultMoves = resultMoves.iloc[:, 1:]

    # Save
    # saveFile = f"{outputDir}/{"evo-" if evo else ""}{pokemonName}.xlsx"
    # print(f"Salvo il risultato in \"{saveFile}\"")
    # resultMoves.to_excel(saveFile, startcol=1, index=False)
    resultMoves = resultMoves.fillna('')

    return list(map(lambda x: pokedex[x]['name'], queryNames)), [resultMoves.columns.tolist()] + resultMoves.values.tolist()
