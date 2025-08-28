from lxml import etree
from collections import defaultdict
import os


class JMDictPOS:
    def __init__(self, xml_path: str):
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"JMdict XML file not found: {xml_path}")

        # Parse with entity resolution (DTD inside file)
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()

        # Dictionary: keb (preferred) or reb (fallback) -> {pos: [...], readings: [...]}
        self.dictionary = defaultdict(lambda: {"pos": [], "readings": []})

        for entry in root.findall("entry"):
            keb = entry.findtext("k_ele/keb")
            if keb:
                key = keb
            else:
                key = entry.findtext("r_ele/reb")

            # Collect all readings for the entry
            readings = [reb.text for reb in entry.findall("r_ele/reb") if reb.text]

            # Collect POS
            pos_list = [pos.text for pos in entry.findall("sense/pos") if pos.text]

            # Update dictionary
            self.dictionary[key]["pos"].extend(pos_list)
            self.dictionary[key]["readings"].extend(readings)

    def lookup(self, word: str):
        """
        Return dictionary with POS and readings for a given word, 
        or {"pos": [], "readings": []} if not found.
        """
        return self.dictionary.get(word, {"pos": [], "readings": []})