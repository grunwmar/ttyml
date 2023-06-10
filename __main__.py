import bs4
import lxml
import os
import json

from elements.formats import parse_formats
from elements.lists import parse_ordered_list, parse_unordered_list
from elements.structurals import parse_paragraphs, parse_sections
from elements.others import parse_links, parse_span  


APPEARANCE = {
    "link": "4;34",
    "link-handle": "32",
    "section-bullet": "§",
    "emphasis": "7",
    "ulist-bullet-char": "+",
    "ulist-bullet": "32"
    }


LINKS = dict()


def load_ttyml(filename):

    with open(filename, "r") as f:
    
        data = f.read()
       
        split_lines = data.split("\n")
        for line in split_lines:
            line = line.strip()
        
        data = "".join(split_lines)
        data = data.replace("\t", "")

        for _ in range(4):
            data = data.replace("  ", " ")
            data = data.replace("\n ", "\n")
    
        soup = bs4.BeautifulSoup(data, features="lxml")

        for elm in soup.find_all("title"):
            text = f" {elm.string.upper()} "
            text = "  ".join(list(text)).replace("   ", "   ")
            dash = len(text) * "="
            new_text = f"\t \033[1m{text}\033[0m \n\n\t {dash} "
            elm.string = new_text
            elm.insert_before("\n\n")
            elm.insert_after("\n\n")
            elm.unwrap()


        soup = parse_sections(soup)
        soup = parse_paragraphs(soup)
        soup = parse_formats(soup)
        soup = parse_unordered_list(soup)
        soup = parse_links(soup, LINKS)
        soup = parse_span(soup)

        for tag in ["html", "body", "head", "ttyml"]:
            for elm in soup.find_all(tag):
                elm.unwrap()

        string = str(soup).replace("&lt;", "<").replace("&gt;", ">")
        
        split_lines = string.split("\n")
        for line in split_lines:
            line = line.strip()

        string = "\n".join(split_lines)
        string = string.replace("\n\n", "\n")
    

        try:
            os.makedirs(os.environ["DOC_FDIR"])
        except Exception as e:
            print(e.__dict__)

        with open(os.environ["DOC_FDIR_TEXT"], "w") as f:
            f.write(string)

        with open(os.environ["DOC_FDIR_LINKS"], "w") as f:
            json.dump(LINKS, f, ensure_ascii=False, indent=4)


load_ttyml(os.environ["DOC_FNAME"])
