import reflex as rx
from AI_CODE_REVIEWER.state import State

CARD_BG = "#141a1f"
CARD_BORDER = "1px solid #1f2730"
TEXT = "#e8edf2"
MUTED = "#93a1b2"
ACCENT = "#38d4ff"


def ai_suggestions_below_score():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("sparkles", size=18, color=ACCENT),
                rx.text("AI Suggestions", color=TEXT, font_weight="600", font_size="20px"),
                spacing="2",
                align="center",
            ),
            rx.cond(
                State.optimizations.length() > 0,
                rx.vstack(
                    rx.foreach(
                        State.optimizations,
                        lambda suggestion: rx.box(
                            rx.hstack(
                                rx.icon("alert-triangle", size=16, color="#fbbf24"),
                                rx.text(suggestion, color=TEXT, font_size="12px"),
                                spacing="3",
                            ),
                            bg="#171d24",
                            border="1px solid #222a33",
                            border_radius="14px",
                            padding="12px 16px",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.text("No suggestions yet. Run a review to see details.", color=MUTED, font_size="12px"),
            ),
            spacing="4",
            align="stretch",
            width="100%",
        ),
        bg=CARD_BG,
        border=CARD_BORDER,
        border_radius="22px",
        padding="24px",
        width="100%",
        box_shadow="0 24px 60px rgba(0, 0, 0, 0.35)",
    )
