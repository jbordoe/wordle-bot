import random


class WordleResultThemer:
    THEMES = {
        "default": {"absent": "⬛", "present": "🟨", "placed": "🟩", "dark": True},
        "animals": {"absent": "🐁", "present": "🐤", "placed": "🐸", "dark": False},
        "hearts": {"absent": "🖤", "present": "💛", "placed": "💚", "dark": True},
        "circles": {"absent": "⚫️", "present": "🟡", "placed": "🟢", "dark": True},
        "clothes": {"absent": "🎩", "present": "🩳", "placed": "🩲", "dark": True},
        "food": {"absent": "🥚", "present": "🍋", "placed": "🍏", "dark": False},
        "emoji": {"absent": "☹️", "present": "😐", "placed": "🙂", "dark": True},
        "smile": {"absent": "😐", "present": "🙂", "placed": "😃", "dark": False},
        "tree": {"absent": "🌱", "present": "🌿", "placed": "🌳", "dark": False},
        "bird": {"absent": "🥚", "present": "🐣", "placed": "🐓", "dark": False},
        "medals": {"absent": "🥉", "present": "🥈", "placed": "🥇", "dark": False},
        "moon1": {"absent": "🌑", "present": "🌗", "placed": "🌕", "dark": False},
        "moon2": {"absent": "🌚", "present": "🌜", "placed": "🌝", "dark": False},
        "weather": {"absent": "⛈", "present": "🌥", "placed": "🌞", "dark": False},
        "foodmix": {
            "absent": ["🥚", "🦴", "🍚", "🥛", "🎂"],
            "present": ["🧀", "🍌", "🍋", "🥐"],
            "placed": ["🥬", "🥦", "🥒", "🥝", "🍏"],
            "dark": False,
        },
        "misc": {
            "absent": ["🌚", "💣", "🏴", "🎮", "🎱", "🔌", "📞"],
            "present": ["🍯", "🎷", "🛵", "🚜", "🔑", "🧽", "🛎", "📒", "🙃", "🦶"],
            "placed": ["🤢", "🍀", "🥝", "🪀", "🔋", "🦠", "📗", "✅", "🔫"],
            "dark": True,
        },
    }
    VALID_THEMES = list(THEMES.keys()) + ["random", "shuffle"]

    @staticmethod
    def map_result(result: str, theme: str) -> str:
        if theme == "random":
            theme = random.choice(list(WordleResultThemer.THEMES.keys()))
        if theme in [None, "default"]:
            return result.text

        if theme == "shuffle":
            dark = random.choice([True, False])
            tmap = {}
            for key in ["absent", "present", "placed"]:
                tmap[WordleResultThemer.THEMES["default"][key]] = [
                    WordleResultThemer.THEMES[t][key]
                    for t in WordleResultThemer.THEMES
                    if WordleResultThemer.THEMES[t]["dark"] == dark
                ]

            tmap["⬜"] = tmap.get("⬛")
            result_chars = [
                random.choice(tmap[char]) if char in tmap else char
                for char in result.text
            ]
            result_text = "".join(result_chars)
        else:
            result_text = result.text
            for key in ["absent", "present", "placed"]:
                mappings = WordleResultThemer.THEMES[theme][key]
                if isinstance(mappings, list):
                    mapped = random.choice(mappings)
                else:
                    mapped = mappings

                if key == "absent":
                    result_text = result_text.replace("⬜", mapped)

                result_text = result_text.replace(
                    WordleResultThemer.THEMES["default"][key],
                    mapped
                )
        return result_text
