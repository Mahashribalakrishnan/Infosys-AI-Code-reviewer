import reflex as rx
from AI_CODE_REVIEWER.components.header import header
from AI_CODE_REVIEWER.state import State

CARD_BG = "#141a1f"
CARD_BORDER = "1px solid #1f2730"
TEXT = "#e8edf2"
MUTED = "#93a1b2"
ACCENT = "#38d4ff"


def history_card(entry: dict):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(entry["timestamp"], color=MUTED, font_size="12px"),
                    rx.hstack(
                        rx.text("Score", color=MUTED, font_size="12px"),
                        rx.text(entry["score"], color=TEXT, font_weight="700", font_size="16px"),
                        rx.text("/100", color=MUTED, font_size="12px"),
                        spacing="2",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.badge("Good", bg="#1b2f2a", color="#77f6c8", font_size="10px"),
                justify="between",
                align="start",
                width="100%",
            ),
            rx.hstack(
                rx.vstack(
                    rx.text(entry["issues_count"], color=TEXT, font_weight="700", font_size="14px"),
                    rx.text("Issues", color=MUTED, font_size="11px"),
                    align="center",
                ),
                rx.vstack(
                    rx.text(entry["suggestions_count"], color=TEXT, font_weight="700", font_size="14px"),
                    rx.text("Suggestions", color=MUTED, font_size="11px"),
                    align="center",
                ),
                rx.vstack(
                    rx.text(entry.get("style_count", 0), color=TEXT, font_weight="700", font_size="14px"),
                    rx.text("Style", color=MUTED, font_size="11px"),
                    align="center",
                ),
                spacing="6",
                width="100%",
            ),
            rx.vstack(
                rx.text("Code Preview", color=MUTED, font_size="11px"),
                rx.box(
                    rx.text(
                        entry.get("code_preview", ""),
                        color=TEXT,
                        font_family="'Space Mono', monospace",
                        font_size="11px",
                    ),
                    bg="#171d24",
                    border="1px solid #222a33",
                    border_radius="10px",
                    padding="10px 12px",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            rx.button(
                "View Details",
                size="2",
                bg=ACCENT,
                color="#0b0f14",
                border_radius="10px",
                on_click=lambda e=entry: State.load_history_entry(e),
                _hover={"filter": "brightness(1.05)"},
                width="100%",
            ),
            spacing="3",
            align="stretch",
            width="100%",
        ),
        bg=CARD_BG,
        border=CARD_BORDER,
        border_radius="18px",
        padding="18px",
        width="100%",
        box_shadow="0 18px 40px rgba(0, 0, 0, 0.3)",
    )


def history_page():
    return rx.box(
        rx.vstack(
            header(),
            rx.heading("Analysis History", size="5", color=TEXT, margin_top="1.5em", padding_x="2em"),
            rx.cond(
                State.analysis_history.length() > 0,
                rx.vstack(
                    rx.foreach(State.analysis_history, history_card),
                    spacing="4",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("No Analysis History", size="4", color=TEXT),
                        rx.text(
                            "Start analyzing code to build your history.",
                            color=MUTED,
                            text_align="center",
                        ),
                        rx.link(
                            rx.button("Go to Home", bg=ACCENT, color="#0b0f14"),
                            href="/",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    bg=CARD_BG,
                    border=CARD_BORDER,
                    border_radius="18px",
                    padding="32px",
                    width="100%",
                ),
            ),
            spacing="6",
            align="center",
            width="100%",
            padding_x="2em",
        ),
        bg="#0b0f14",
        min_height="100vh",
        width="100%",
        on_mount=[State.set_current_page("history"), State.load_history],
    )
