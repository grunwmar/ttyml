import bs4
import lxml
import os
import json


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

        subst = {
                "b": "1",
                "f": "2",
                "i": "3",
                "u": "4",
                "s": "9",
                "e": f"7;{APPEARANCE['emphasis']}",
            }

        for tag, code in subst.items():
            for elm in soup.find_all(tag):
                elm.insert_before(f"\033[{code}m")
                elm.insert_after("\033[0m")
                elm.unwrap()

        for elm in soup.find_all("ul"):
            for elm_li in elm.find_all("li"):
                elm_li.insert_before(f"\t\033[{APPEARANCE['ulist-bullet']}m{APPEARANCE['ulist-bullet-char']}\033[0m ")
                elm_li.insert_after("\n")
                elm_li.unwrap()
            elm.insert_before("\n\n")
            elm.insert_after("\n")
            elm.unwrap()

        for elm in soup.find_all("p"):
            elm.insert_before("\n")
            elm.insert_after("\n")
            elm.unwrap()

        for elm in soup.find_all("title"):
            text = f" {elm.string.upper()} "
            text = "  ".join(list(text)).replace("   ", "   ")
            dash = len(text) * "="
            new_text = f"\t \033[1m{text}\033[0m \n\n\t {dash} "
            elm.string = new_text
            elm.insert_before("\n\n")
            elm.insert_after("\n\n")
            elm.unwrap()

        for elm in soup.find_all("sec"):
            depth = int(elm["d"])
            pref = depth * APPEARANCE['section-bullet']
            if depth == 0:
                text = elm.string.upper()
                text = " ".join(list(text))
                elm.string = f"\033[1m\033[7m {text} \033[0m"

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

        for elm in soup.find_all("ln"):
            elm.insert_before(f"\033[{APPEARANCE['link']}m")
            handle = elm.get("handle")
            href = elm.get("href")
            text = elm.string
            link_item = {
                str(handle): [href, text]
                    }
            LINKS.update(link_item)
            elm.insert_after(f"\033[0m \033[{APPEARANCE['link-handle']}m^{handle}\033[0m")
            elm.unwrap()

        for elm in soup.find_all("mark"):
            val = elm["color"]
            elm.insert_before(f"\033[{val}m")
            elm.insert_after(f"\033[0m")
            elm.unwrap()

        for tag in ["html", "body", "head", "ttyml"]:
            for elm in soup.find_all(tag):
                elm.unwrap()

        string = str(soup).replace("&lt;", "<").replace("&gt;", ">")
        #string = string.replace("\t", "")
        
        split_lines = string.split("\n")
        for line in split_lines:
            line = line.strip()

        string = "\n".join(split_lines)


        string = string.replace("\n\n", "\n")

        print(string)

        filename, _ = os.path.splitext(filename)

        directory = os.path.join(f"export", f"{filename}.d")
        filename = os.path.join(directory, filename)
        
        try:
            os.makedirs(directory)
        except Exception as e:
            print(e.__dict__)

        with open(f"{filename}.txt", "w") as f:
            f.write(string)

        with open(f"{filename}.json", "w") as f:
            json.dump(LINKS, f, ensure_ascii=False, indent=4)

load_ttyml("document.xml")
