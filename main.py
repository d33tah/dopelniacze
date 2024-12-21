# Przepisz mi to na Fleta

"""

Equivalent of the following program, but in flet:

from flask import Flask, render_template_string, request, redirect, url_for
import random
import json

app = Flask(__name__)

# Załaduj dane do pamięci
with open('dopelniacze.json', 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]


def handle_input():

    LINK = '''
           <a href="/">Spróbuj ponownie</a>
    '''

    user_dopelniacz_lp = request.form.get('dopelniacz_lp')
    user_dopelniacz_lm = request.form.get('dopelniacz_lm')
    correct_lp = request.form.get('correct_lp')
    correct_lm = request.form.get('correct_lm')

    lp_correct = not bool(correct_lp) or user_dopelniacz_lp == correct_lp
    lm_correct = not bool(correct_lm) or user_dopelniacz_lm == correct_lm

    result = ''

    if lp_correct and lm_correct:
        result += 'Brawo! Odpowiedź <font color="green">poprawna</font>.' + LINK
    else:
        result += 'Niestety, odpowiedź <font color="red">niepoprawna</font>. Poprawna odpowiedź to: <br>'
        result += f'Nie mam żadnej/żadnego: {correct_lp!r}<br>'
        result += f'Nie mam żadnych: {correct_lm!r}<br>'
        result += 'Twoja odpowiedź: <br><font color="red">'
        result += f'Nie mam żadnej/żadnego: {user_dopelniacz_lp}<br>'
        result += f'Nie mam żadnych: {user_dopelniacz_lm}<br></font>'
        result += LINK

    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return handle_input()
    else:
        return generate_page()

def generate_page():

    TEMPLATE = '''
    <!doctype html>
    <html lang="pl">
      <head>
        <meta charset="utf-8">
        <title>Dopełniacze</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
      </head>
      <body>
        <h2>{{ title }}</h2>
        <form method="post">
          <div>
            <label>Nie mam żadnej/żadnego:</label>
            <input type="text" name="dopelniacz_lp" required>
          </div>
          <div>
            <label>Nie mam żadnych:</label>
            <input type="text" name="dopelniacz_lm" required>
          </div>
          <input type="hidden" name="correct_lp" value="{{ dopelniacz_lp }}">
          <input type="hidden" name="correct_lm" value="{{ dopelniacz_lm }}">
          <button type="submit">Sprawdź</button>
        </form>
      </body>
    </html>
    '''

    item = random.choice(data)
    title = item['title']
    dopelniacz_lp = item['declensions'].get('dopelniacz_lp', '')
    dopelniacz_lm = item['declensions'].get('dopelniacz_lm', '')

    return render_template_string(TEMPLATE, title=title, dopelniacz_lp=dopelniacz_lp, dopelniacz_lm=dopelniacz_lm)

"""

# Póki co mam tyle:

import flet as ft

class DopelniaczeApp(ft.Column):
    pass

def main(page: ft.Page):
    page.title = "Dopelniacze"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # create app control and add it to the page
    page.add(DopelniaczeApp())

ft.app(main)
