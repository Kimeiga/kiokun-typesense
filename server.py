from fastapi.middleware.cors import CORSMiddleware
import re
from collections import defaultdict
import json
import os
import re

from fastapi import FastAPI

app = FastAPI()


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Allows requests from your frontend
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# ... (rest of your code)


# map of word/char string to list of indices and raw kanji/hanzi data
index = defaultdict(lambda: defaultdict(list))

# words from dong-chinese (cedict)
c_word_entries = defaultdict(lambda: defaultdict(list))

# words from jmdict
j_word_entries = defaultdict(list)

# words from jmnedict
n_word_entries = defaultdict(list)

with open("entry_data/entry_index_min.json", "r", encoding="utf-8") as file:
    index = json.load(file)

with open("entry_data/c_word_entries.json", "r", encoding="utf-8") as file:
    c_word_entries = json.load(file)

with open("entry_data/j_word_entries.json", "r", encoding="utf-8") as file:
    j_word_entries = json.load(file)

with open("entry_data/n_word_entries.json", "r", encoding="utf-8") as file:
    n_word_entries = json.load(file)


def make_ids_unique(svg_content, suffix):
    # This dictionary will map the original ids to the new unique ids
    id_map = {}

    # Add embedded script for infinite animation
    infinite_script = """
    <script>
    // Infinite loop logic
    (function infinite() {
        var e = document.currentScript.parentElement;
        var s = e.innerHTML;
        var n = (s.match(/--d:[0-9]+s/g) || []).length;
        setInterval(function() {
            e.innerHTML = '';
            e.innerHTML = s;
        }, (n + 1) * 1000);
    })();
    </script>
    """

    # First, replace all id attributes to make them unique
    svg_content = re.sub(
        r'id="([^"]+)"', lambda m: _replace_id(m, id_map, suffix), svg_content)

    # Next, replace all references to those ids (e.g., in clip-path attributes and <use> elements)
    svg_content = re.sub(
        r'url\(#([^)]+)\)', lambda m: _replace_clip_path(m, id_map), svg_content)
    svg_content = re.sub(
        r'xlink:href="#([^"]+)"', lambda m: _replace_use_href(m, id_map), svg_content)

    svg_content = re.sub('#000', "var(--svg-stroke-fg-color)", svg_content)
    svg_content = re.sub('#ccc', "var(--svg-stroke-bg-color)", svg_content)

    s1 = svg_content

    svg_content = re.sub(r'</svg>', infinite_script + '</svg>', svg_content)

    print(s1 == svg_content)

    return svg_content


def _replace_id(match, id_map, suffix):
    original_id = match.group(1)
    if original_id not in id_map:
        # Generate a new unique id and store it in the map
        unique_id = f"{original_id}-{suffix}"
        id_map[original_id] = unique_id
    else:
        # If this id was already replaced, use the same new id
        unique_id = id_map[original_id]
    return f'id="{unique_id}"'


def _replace_clip_path(match, id_map):
    # Extract the original id used in the clip-path
    original_id = match.group(1)
    # Replace it with the new unique id
    # Use the original id if a new one wasn't generated
    unique_id = id_map.get(original_id, original_id)
    return f'url(#{unique_id})'


def _replace_use_href(match, id_map):
    # Extract the original id used in the xlink:href
    original_id = match.group(1)
    # Replace it with the new unique id
    # Use the original id if a new one wasn't generated
    unique_id = id_map.get(original_id, original_id)
    return f'xlink:href="#{unique_id}"'


def get_entry(word):
    try:
        entry = index[word]
    except:
        return {}

    svgs = {}
    if len(word) == 1:
        # get the svg for the character
        for lang, folder in [('j', 'anim/svgsJa'), ('s', 'anim/svgsZhHans'), ('t', 'anim/svgsZhHant')]:
            svg_path = os.path.join(folder, f"{ord(word)}.svg")
            if os.path.exists(svg_path):
                with open(svg_path, "r", encoding="utf-8") as file:
                    svg_data = file.read()
                    # Make IDs unique within each SVG
                    svgs[lang] = make_ids_unique(
                        svg_data, f"{lang}-{ord(word)}")

    # if len(word) == 1:
    #     # get the svg for the character
    #     if os.path.exists(os.path.join("anim/svgsJa", f"{ord(word)}.svg")):
    #         # open the svg and send the data
    #         with open(os.path.join("anim/svgsJa", f"{ord(word)}.svg"), "r", encoding="utf-8") as file:
    #             svgs['j'] = file.read()
    #     if os.path.exists(os.path.join("anim/svgsZhHans", f"{ord(word)}.svg")):
    #         with open(os.path.join("anim/svgsZhHans", f"{ord(word)}.svg"), "r", encoding="utf-8") as file:
    #             svgs['s'] = file.read()
    #     if os.path.exists(os.path.join("anim/svgsZhHant", f"{ord(word)}.svg")):
    #         with open(os.path.join("anim/svgsZhHant", f"{ord(word)}.svg"), "r", encoding="utf-8") as file:
    #             svgs['t'] = file.read()

    return {
        **({"c_c": entry['c_c']} if 'c_c' in entry else {}),
        # japanese character info is embedded
        **({"j_c": entry['j_c']} if 'j_c' in entry else {}),

        # v is chinese variants of japanese character (j2ch(j))
        # we have to get the entries for each of these
        **({"v_c_c": [index[c_char]['c_c'] for c_char in entry['v_c_c']]} if 'v_c_c' in entry else {}),

        # a is japanese variants of chinese character (j2ch(j))
        # we have to get the entries for each of these
        **({"v_j_c": [index[c_char]['j_c'] for c_char in entry['v_j_c']]} if 'v_j_c' in entry else {}),

        # chinese word data requires lookup
        **({"c_w": [c_word_entries[str(i)] for i in entry['c_w']]} if 'c_w' in entry else {}),

        # japanese word data requires lookup
        **({"j_w": [j_word_entries[str(i)] for i in entry['j_w']]} if 'j_w' in entry else {}),

        # japanese name data requires lookup
        **({"j_n": [n_word_entries[str(i)] for i in entry['j_n']]} if 'j_n' in entry else {}),

        # chinese word variants of a japanese word
        **({"v_c_w": [c_word_entries[str(i)] for i in entry['v_c_w']]} if 'v_c_w' in entry else {}),

        # japanese word variants of a chinese word
        **({"v_j_w": [j_word_entries[str(i)] for i in entry['v_j_w']]} if 'v_j_w' in entry else {}),

        # get all substrings that are listed, and if none are listed, get all character substrings...
        # TODO: ...and all components of each character

        # **({"s": [get_entry(word) for word in entry['s']].extend([get_entry(char) for char in word if len(char) > 1])} if 's' in entry else {"s": [get_entry(char) for char in word if len(char) > 1]}),
        **({"s": [get_entry(word) for word in entry['s']] + [get_entry(char) for char in word if len(word) > 1]} if 's' in entry else {"s": [get_entry(char) for char in word if len(word) > 1]}),

        # now get components from the individual character if possible
        **({"h": [get_entry(component['character']) for component in entry['c']['components']]} if 'c' in entry and 'components' in entry['c'] and len(entry['c']['components']) else {}),

        # we also need to provide the japanese character svg (if applicable), the simp chinese character svg (if applicable), and the trad chinese character svg (if applicable)
        # we can do that by, if the word is one character long, looking up the character's codepoint in the animCJK japanese/simpChinese/tradChinese folders of svgs
        # we need to also provide the decomposition data (we can transform the dictionary files with animCJK to get them) so that the frontend knows how to change the svgs so that they color each component differently
        # TODO: in the future, we can double check the decomposition data with CHISE IDS but I'm pretty sure since the animCJK project only has some of the most common characters covered, it's probably correct for those characters.
        # Nonetheless, we can use the CHISE IDS data to provide the decomposition data for the characters that animCJK doesn't have, in order to allow the user to click into their components. Probably for the characters that are present in animCJK, we want to use their decomposition so as not to contradict the svg animations being shown for optimal user experience.

        # g for graphics
        **({"g": svgs} if svgs else {}),

    }


@app.get("/{word}")
def get_word(word):

    # start with these but soon we have to return all substrings of word that are in the index
    # and all components of each character
    return {
        **(get_entry(word))


    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
