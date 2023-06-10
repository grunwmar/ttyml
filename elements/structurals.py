from elements import BASIC_CONFIG


def parse_paragraphs(soup):
    for elm in soup.find_all("p"):
        elm.insert_before("\n")
        elm.insert_after("\n")
        elm.unwrap()
    return soup


def parse_sections(soup):

    bullet_char = BASIC_CONFIG["bullet"]['section'][0]
    bullet_color = BASIC_CONFIG["bullet"]['section'][1]

    for elm in soup.find_all("section"):
        depth = int(elm["depth"])
        pref = depth * bullet_char
        if depth == 0:
            text = elm.string.upper()
            text = " ".join(list(text))
            elm.string = f"\033[1;4m{text}\033[0m"

        elif depth == 1:
            text = elm.string.upper()
            elm.string = f"\033[4;1m{pref} {text}\033[0m"

        elif depth == 2:
            text = elm.string
            elm.string = f"\033[4;1m{pref} {text}\033[0m"

        elif depth == 3:
            text = elm.string
            elm.string = f"\033[4m{pref} {text}\033[0m"

        elif depth == 4:
            text = elm.string
            elm.string = f"\033[4;3m{pref} {text}\033[0m"

        else:
            text = elm.string
            elm.string = f"\033[3m<{pref} {text}>\033[0m"

        elm.insert_before("\n\n")
        elm.insert_after("\n")
        elm.unwrap()
    return soup