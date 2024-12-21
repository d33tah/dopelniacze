import sys
import xml.etree.ElementTree as ET
import logging
import json
import re

# Konfiguracja logowania
# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def extract_title_and_declension(input_xml):
    try:
        # Używamy iterparse do strumieniowego przetwarzania pliku XML
        logging.info("Starting XML streaming...")
        context = ET.iterparse(input_xml, events=("start", "end"))
        _, root = next(context)  # Pobieramy element root dla przestrzeni nazw

        namespace = {"mw": "http://www.mediawiki.org/xml/export-0.11/"}
        current_title = None

        for event, elem in context:
            if event == "start":
                if elem.tag == f"{{{namespace['mw']}}}title":
                    current_title = None
                elif elem.tag == f"{{{namespace['mw']}}}text":
                    if current_title and elem.text:
                        text = elem.text
                        if "{{odmiana-rzeczownik-polski" in text:
                            logging.debug(f"Found 'odmiana-rzeczownik-polski' template in page: {current_title}")
                            lines = text.split('\n')
                            declensions = {}

                            # Regularne wyrażenia do dopasowania z dowolną ilością białych znaków
                            dopełniacz_lp_pattern = re.compile(r"^\s*\|\s*Dopełniacz\s*lp\s*=\s*(.+)\s*$")
                            dopełniacz_lm_pattern = re.compile(r"^\s*\|\s*Dopełniacz\s*lm\s*=\s*(.+)\s*$")

                            parsing_now = False

                            for line in lines:

                                if "{{odmiana-rzeczownik-polski" in line:
                                    parsing_now = True
                                    continue

                                if parsing_now and line.strip() == "}}":
                                    parsing_now = False
                                    continue

                                if not parsing_now:
                                    continue

                                lp_match = dopełniacz_lp_pattern.match(line)
                                lm_match = dopełniacz_lm_pattern.match(line)

                                lp_match_result = lp_match.group(1).strip() if lp_match else ''
                                lm_match_result = lm_match.group(1).strip() if lm_match else ''

                                if lp_match_result and '{' not in lp_match_result and '<' not in lp_match_result:
                                    declensions["dopelniacz_lp"] = lp_match_result
                                    logging.debug(f"Extracted singular declension: {declensions['dopelniacz_lp']}")
                                if lm_match_result and '{' not in lm_match_result and '<' not in lm_match_result:
                                    declensions["dopelniacz_lm"] = lm_match_result
                                    logging.debug(f"Extracted plural declension: {declensions['dopelniacz_lm']}")

                            if declensions:
                                result = {
                                    "title": current_title,
                                    "declensions": declensions
                                }
                                print(json.dumps(result, ensure_ascii=False))
                            else:
                                logging.warning(f"No declensions found for page: {current_title}")

            elif event == "end":
                if elem.tag == f"{{{namespace['mw']}}}page":
                    root.clear()

            if elem.tag == f"{{{namespace['mw']}}}title":
                current_title = elem.text
                logging.debug(f"Processing page: {current_title}")

    except ET.ParseError as e:
        logging.error(f"Error parsing XML: {e}")

if __name__ == "__main__":
    extract_title_and_declension(sys.stdin)
