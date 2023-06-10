from . import BASIC_CONFIG


def parse_links(soup, jd):
    
    handle_char = BASIC_CONFIG["handle"]["link"][0]
    handle_color = BASIC_CONFIG["handle"]["link"][1]

    color = BASIC_CONFIG["link"][0]
    opening_char = BASIC_CONFIG["link"][1]
    closing_char = BASIC_CONFIG["link"][2]

    for elm in soup.find_all("a"):

        elm.insert_before(f"\033[{color}m{opening_char}")

        handle = elm.get("handle")
        href = elm.get("href")
        text = elm.string
        
        link_item = {
            str(handle): [href, text]
            }
        
        jd.update(link_item)
        elm.insert_after(f"{closing_char} \033[0m\033[{handle_color}m{handle_char}{handle}\033[0m")
        elm.unwrap()
    return soup


def parse_span(soup):
    
    for elm in soup.find_all("span"):
        val = elm["color"]
        elm.insert_before(f"\033[{val}m")
        elm.insert_after(f"\033[0m")
        elm.unwrap()
    return soup
