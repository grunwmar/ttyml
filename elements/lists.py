from . import BASIC_CONFIG


def parse_unordered_list(soup):

    bullet_char = BASIC_CONFIG["bullet"]["ul"][0]
    bullet_color = BASIC_CONFIG["bullet"]["ul"][1]

    for elm in soup.find_all("ul"):
        for elm_li in elm.find_all("li"):
            elm_li.insert_before(f"\t\033[{bullet_color}m{bullet_char}\033[0m ")
            elm_li.insert_after("\n")
            elm_li.unwrap()
        elm.insert_before("\n\n")
        elm.insert_after("\n")
        elm.unwrap()
    return soup


def parse_ordered_list(soup):

    bullet_char = BASIC_CONFIG["bullet"]["ol"][0]
    bullet_color = BASIC_CONFIG["bullet"]["ol"][1]

    for elm in soup.find_all("ol"):
        for index, elm_li in enumerate(elm.find_all("li"), start=1):
            elm_li.insert_before(f"\t\033[{bullet_color}m{index}{bullet_char}\033[0m ")
            elm_li.insert_after("\n")
            elm_li.unwrap()
        elm.insert_before("\n\n")
        elm.insert_after("\n")
        elm.unwrap()
    return soup