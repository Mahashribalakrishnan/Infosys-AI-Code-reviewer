import reflex as rx

from AI_CODE_REVIEWER.components.header import header
from AI_CODE_REVIEWER.components.source_input import source_input_section
from AI_CODE_REVIEWER.components.quality_score import quality_score_section
from AI_CODE_REVIEWER.components.ai_suggested_code import ai_suggested_code_section
from AI_CODE_REVIEWER.components.ai_suggestions_below_score import ai_suggestions_below_score
from AI_CODE_REVIEWER.state import State

TEXT = "#e8edf2"
MUTED = "#93a1b2"
ACCENT = "#38d4ff"


def hero_section():
    return rx.vstack(
        rx.heading(
            rx.text("Refine your ", as_="span"),
            rx.text("Code", as_="span", color=ACCENT),
            rx.text(".", as_="span"),
            size="7",
            color=TEXT,
            font_weight="700",
            text_align="center",
        ),
        rx.text(
            "Our AI Code Reviewer instantly detects bugs, performance issues, and style errors, providing context-aware suggestions to help you write cleaner, faster, and more maintainable code.",
            color=MUTED,
            font_size="14px",
            text_align="center",
            max_width="720px",
        ),
        spacing="3",
        align="center",
        width="100%",
        padding="36px 0 28px 0",
    )


def index():
    return rx.box(
        rx.vstack(
            header(),
            rx.box(
                rx.vstack(
                    hero_section(),
                    rx.hstack(
                        rx.vstack(
                            source_input_section(),
                            spacing="6",
                            width="100%",
                            flex="1",
                        ),
                        rx.vstack(
                            ai_suggested_code_section(),
                            spacing="6",
                            width="100%",
                            flex="1",
                        ),
                        spacing="6",
                        width="100%",
                        align="start",
                    ),
                    rx.vstack(
                        quality_score_section(),
                        spacing="6",
                        width="100%",
                        align="center",
                        padding="28px 0 16px 0",
                    ),
                    rx.vstack(
                        ai_suggestions_below_score(),
                        spacing="6",
                        width="100%",
                        align="center",
                        padding="0 0 32px 0",
                    ),
                    spacing="0",
                    align="stretch",
                    width="100%",
                    padding="0 48px",
                ),
                width="100%",
            ),
            spacing="0",
            align="stretch",
            width="100%",
            height="100%",
        ),
        min_height="100vh",
        width="100%",
        style={
            "background": "radial-gradient(1200px 600px at 50% -200px, #1a2330 0%, #0b0f14 55%)",
            "font_family": "'Outfit', 'Segoe UI', sans-serif",
        },
        on_mount=State.set_current_page("home"),
    )
