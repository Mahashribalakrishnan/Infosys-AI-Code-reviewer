import reflex as rx
from AI_CODE_REVIEWER.pages.index import index
from AI_CODE_REVIEWER.pages.reports import reports_page
from AI_CODE_REVIEWER.pages.history import history_page

app = rx.App()
app.add_page(index)
app.add_page(reports_page, route="/reports")
app.add_page(history_page, route="/history")