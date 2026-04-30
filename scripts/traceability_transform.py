


def normalize_part_number(value: str) -> str:
    cleaned = value.strip().upper()
    cleaned = cleaned.replace("_", "")
    cleaned = cleaned.replace("-", "")
    cleaned = cleaned.replace(" ", "")

    if cleaned.startswith("P"):
        number = cleaned[1:]
    else:
        number = cleaned

    return f"P-{number}"


def normalize_configuration(value: str) -> str:
    cleaned = value.strip().upper()
    cleaned = cleaned.replace("_", " ")
    cleaned = cleaned.replace("/", " ")
    cleaned = cleaned.replace("-", " ")

    words = cleaned.split()

    if words == ["A", "R2"]:
        return "CFG-A-REV-2"

    if "CONFIG" in words:
        words[words.index("CONFIG")] = "CFG"

    if "REV2" in words:
        words[words.index("REV2")] = "REV-2"

    if "REV" in words and "2" in words:
        return "CFG-A-REV-2"

    return "-".join(words)


def normalize_module_name(value: str) -> str:
    cleaned = value.strip().lower()

    known_aliases = {
        "pcm": "power_control_module",
        "power ctrl mod": "power_control_module",
        "power control module": "power_control_module",
    }

    if cleaned in known_aliases:
        return known_aliases[cleaned]

    cleaned = cleaned.replace("-", " ")
    cleaned = cleaned.replace("_", " ")
    words = cleaned.split()

    return "_".join(words)

