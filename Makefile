.PHONY: build format json

format:
	ruff format main.py

build:
	flet run 
	ruff check main.py
	flet build apk

json:
	pv plwiktionary-20241220-pages-articles.xml.bz2| bzcat | python3 ./parse_wiktionary.py > /dev/null
