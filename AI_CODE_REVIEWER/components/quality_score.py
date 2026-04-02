import reflex as rx
from AI_CODE_REVIEWER.state import State

CARD_BG = "#141a1f"
CARD_BORDER = "1px solid #1f2730"
TEXT = "#e8edf2"
MUTED = "#93a1b2"
ACCENT = "#38d4ff"


def quality_score_section():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Code Quality Score", color=TEXT, font_weight="600", font_size="20px"),
                    rx.text("Based on architectural metrics", color=MUTED, font_size="12px"),
                    spacing="1",
                    align="start",
                ),
                rx.hstack(
                    rx.text(State.analysis_score, color=ACCENT, font_weight="700", font_size="36px"),
                    rx.text("/100", color=MUTED, font_size="14px", padding_top="12px"),
                    spacing="1",
                    align="end",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.progress(
                value=State.analysis_score,
                max=100,
                width="100%",
                height="8px",
                color_scheme=rx.cond(
                    State.analysis_score >= 80,
                    "green",
                    rx.cond(State.analysis_score >= 60, "yellow", "red"),
                ),
            ),
            rx.hstack(
                rx.badge(
                    rx.hstack(
                        rx.text("TIME COMPLEXITY:", font_size="12px", letter_spacing="0.4px"),
                        rx.text(State.time_complexity, font_size="12px", letter_spacing="0.4px"),
                        spacing="1",
                        align="center",
                    ),
                    bg="#1c232b",
                    color="#9be4ff",
                    border_radius="999px",
                    padding="5px 10px",
                ),
                rx.badge(
                    rx.hstack(
                        rx.text("SPACE COMPLEXITY:", font_size="12px", letter_spacing="0.4px"),
                        rx.text(State.space_complexity, font_size="12px", letter_spacing="0.4px"),
                        spacing="1",
                        align="center",
                    ),
                    bg="#1c232b",
                    color="#9be4ff",
                    border_radius="999px",
                    padding="5px 10px",
                ),
                spacing="3",
                align="center",
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
