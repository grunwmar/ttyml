from . import BASIC_CONFIG

def parse_formats(soup):

    subst = {
            "b": "1",
            "f": "2",
            "i": "3",
            "u": "4",
            "s": "9",
            "em": "7",
        }

    for tag, code in subst.items():
        for elm in soup.find_all(tag):
            elm.insert_before(f"\033[{code}m")
            elm.insert_after("\033[0m")
            elm.unwrap()

    return soup