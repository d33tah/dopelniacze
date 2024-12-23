# Przepisz mi to na Fleta

import random
import json
import sqlite3
import datetime

import flet as ft

# Załaduj dane do pamięci
with open("dopelniacze.json", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]


class DopelniaczeApp(ft.UserControl):
    def __init__(self, page):
        super().__init__()

        self.error_message = ft.Text()

        try:
            self.db, self.score, self.num_questions = self.connect_db()
        except Exception as e:
            self.error_message.value = f"Wystąpił błąd: {e}"
            self.db = None
            self.score = 0
            self.num_questions = 0

        self.page = page
        self.title = ft.Text()
        self.wiktionary_button = ft.ElevatedButton(
            "Otwórz w Wikisłowniku", on_click=self.open_wiktionary
        )

        # make title and wiktionary_button next to each other
        self.title_and_button = ft.Row(
            controls=[self.title, self.wiktionary_button], spacing=10
        )

        self.input_lp = ft.TextField(
            label="Nie mam żadnej/żadnego:", on_submit=self.handle_input
        )
        self.input_lm = ft.TextField(
            label="Nie mam żadnych:", on_submit=self.handle_input
        )
        self.result = ft.Text()
        self.btn_submit = ft.ElevatedButton(
            "Sprawdź", on_click=self.handle_input
        )
        self.score_text = ft.Text()
        self.spacer = ft.Container(height=50)

        # Layout to arrange components vertically
        self.layout = ft.Column(
            controls=[
                self.spacer,
                self.score_text,
                self.result,
                # self.title,
                # self.wiktionary_button,
                self.title_and_button,
                self.input_lp,
                self.input_lm,
                self.btn_submit,
                self.error_message,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )
        self.controls.append(self.layout)

    def connect_db(self):
        conn = sqlite3.connect("dopelniacze.db")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS attempts "
            "(timestamp TEXT, input TEXT, correct TEXT)"
        )
        conn.commit()
        all_questions = conn.execute("SELECT correct FROM attempts").fetchall()
        score = sum(1 for correct in all_questions if correct)
        num_questions = len(all_questions)
        return conn, score, num_questions

    def did_mount(self):
        self.generate_page()

    def on_success(self):
        self.result.value = "Brawo! Odpowiedź poprawna."
        self.result.color = "green"
        self.score += 1

    def on_failure(self):
        self.result.value = (
            f"Niestety, odpowiedź niepoprawna.\n\n"
            f"Pytanie: {self.title.value!r}\n\n"
            "Poprawna odpowiedź to:\n"
            f"Nie ma żadnej/żadnego: {self.correct_lp!r}\n"
            f"Nie ma żadnych: {self.correct_lm!r}\n\n"
            f"Napisałeś/aś: {self.user_dopelniacz_lp!r} / "
            f"{self.user_dopelniacz_lm!r}"
        )
        self.result.color = "red"

    @property
    def user_dopelniacz_lp(self):
        return self.input_lp.value

    @property
    def user_dopelniacz_lm(self):
        return self.input_lm.value

    def commit_attempt(self, title, success):
        try:
            timestamp = datetime.datetime.now().isoformat()
            input = f"{self.input_lp.value} / {self.input_lm.value}"
            correct = f"{self.correct_lp} / {self.correct_lm}"
            self.db.execute(
                "INSERT INTO attempts VALUES (?, ?, ?)",
                (timestamp, input, correct),
            )
            self.db.commit()
        except Exception as e:
            self.error_message.value = f"Wystąpił błąd: {e}"

    def compare_answer(self, user, correct):
        if not bool(correct):
            return True

        user = user.strip().lower()

        if "/" in correct:
            possibilities = [c.strip().lower() for c in correct.split("/")]
            return user in possibilities

        correct = correct.strip().lower()
        return user == correct

    def handle_input(self, event):
        self.num_questions += 1
        user_dopelniacz_lp = self.input_lp.value
        user_dopelniacz_lm = self.input_lm.value
        correct_lp = self.correct_lp
        correct_lm = self.correct_lm

        lp_correct = self.compare_answer(user_dopelniacz_lp, correct_lp)
        lm_correct = self.compare_answer(user_dopelniacz_lm, correct_lm)
        success = lp_correct and lm_correct

        if success:
            self.on_success()
        else:
            self.on_failure()
        self.commit_attempt(self.title.value, success)

        self.update()
        self.generate_page()

    def update_score_text(self):
        # calculate score, display percentage too
        score_text = f"Wynik: {self.score}/{self.num_questions}"
        if self.num_questions > 0:
            score_text += f" ({self.score / self.num_questions:.0%})"
        self.score_text.value = score_text

    def open_wiktionary(self, event):
        self.page.launch_url(
            f"https://pl.wiktionary.org/wiki/{self.title.value}"
        )

    def generate_page(self, event=None):
        item = random.choice(data)
        self.title.value = item["title"]
        self.correct_lp = item["declensions"].get("dopelniacz_lp", "")
        self.correct_lm = item["declensions"].get("dopelniacz_lm", "")

        # reset inputs
        self.input_lp.value = ""
        self.input_lm.value = ""

        self.update_score_text()
        self.update()


def main(page: ft.Page):
    page.title = "Dopełniacze"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # create app control and add it to the page
    page.add(DopelniaczeApp(page))


ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
