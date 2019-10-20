from WebScraper.WebScraper import SelectorFactory

import json

if __name__ == '__main__':
    with open("../../../../WebScraper.json", encoding="utf-8") as f:
        sitemap = json.load(f)

    json_selectors = sitemap.get("selectors", None)
    tree = SelectorFactory.bulid_selector_tree(json_selectors)
    pass
