# Przepisz mi to na Fleta

import flet as ft
import random
import json

# Załaduj dane do pamięci
with open('dopelniacze.json', 'r', encoding='utf-8') as f:
    data = [json.loads(line) for line in f]

class DopelniaczeApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.title = ft.Text()

        self.input_lp = ft.TextField(label="Nie mam żadnej/żadnego:")
        self.input_lm = ft.TextField(label="Nie mam żadnych:")
        self.result = ft.Text()
        self.btn_submit = ft.ElevatedButton("Sprawdź", on_click=self.handle_input)
        self.score = 0
        self.num_questions = 0
        self.score_text = ft.Text()
        self.spacer = ft.Container(height=50)

        # Layout to arrange components vertically
        self.layout = ft.Column(
            controls=[
                self.spacer,
                self.score_text,
                self.result,
                self.title,
                self.input_lp,
                self.input_lm,
                self.btn_submit,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )
        self.controls.append(self.layout)

    def did_mount(self):
        self.generate_page()

    def handle_input(self, event):
        self.num_questions += 1
        user_dopelniacz_lp = self.input_lp.value
        user_dopelniacz_lm = self.input_lm.value
        correct_lp = self.correct_lp
        correct_lm = self.correct_lm

        lp_correct = not bool(correct_lp) or user_dopelniacz_lp == correct_lp
        lm_correct = not bool(correct_lm) or user_dopelniacz_lm == correct_lm

        if lp_correct and lm_correct:
            self.result.value = 'Brawo! Odpowiedź poprawna.'
            self.result.color = 'green'
            self.score += 1
        else:
            self.result.value = (
                f'Niestety, odpowiedź niepoprawna. Poprawna odpowiedź to:\n'
                f'Nie mam żadnej/żadnego: {correct_lp}\n'
                f'Nie mam żadnych: {correct_lm}\n'
            )
            self.result.color = 'red'

        self.update()
        self.generate_page()

    def update_score_text(self):
        # calculate score, display percentage too
        score_text = f'Wynik: {self.score}/{self.num_questions}'
        if self.num_questions > 0:
            score_text += f' ({self.score / self.num_questions:.0%})'
        self.score_text.value = score_text

    def generate_page(self, event=None):
        item = random.choice(data)
        self.title.value = item['title']
        self.correct_lp = item['declensions'].get('dopelniacz_lp', '')
        self.correct_lm = item['declensions'].get('dopelniacz_lm', '')

        # reset inputs
        self.input_lp.value = ''
        self.input_lm.value = ''

        self.update_score_text()
        self.update()

def main(page: ft.Page):
    page.title = "Dopełniacze"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # create app control and add it to the page
    page.add(DopelniaczeApp())

ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
