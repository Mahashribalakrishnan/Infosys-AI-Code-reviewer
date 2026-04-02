import reflex as rx
from AI_CODE_REVIEWER.state import State

CARD_BG = "#141a1f"
CARD_BORDER = "1px solid #1f2730"
TEXT = "#e8edf2"
MUTED = "#93a1b2"
ACCENT = "#39d4ff"
INPUT_BG = "#22282f"


def ai_suggested_code_section():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon("sparkles", size=14, color="#77f6c8"),
                        width="24px",
                        height="24px",
                        border_radius="7px",
                        bg="rgba(119, 246, 200, 0.15)",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.text(
                        "AI CORRECTED CODE",
                        font_size="12px",
                        letter_spacing="1px",
                        font_weight="700",
                        color=MUTED,
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.badge(
                    "OPTIMIZED",
                    bg="#1b2f2a",
                    color="#77f6c8",
                    font_size="10px",
                    border_radius="999px",
                    padding="4px 10px",
                    letter_spacing="0.6px",
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            rx.box(
                rx.cond(
                    State.loading,
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text("AI is analyzing your code...", color=MUTED, font_size="13px"),
                        spacing="3",
                        align="center",
                        padding="40px",
                    ),
                    rx.text_area(
                        value=rx.cond(
                            State.corrected_code != "",
                            State.corrected_code,
                            rx.cond(
                                State.optimizations.length() > 0,
                                State.optimizations[0],
                                "No corrected code yet.",
                            ),
                        ),
                        height="320px",
                        width="100%",
                        font_family="'Space Mono', monospace",
                        font_size="13px",
                        bg=INPUT_BG,
                        color=TEXT,
                        border="1px solid #2b343d",
                        border_radius="16px",
                        padding="18px",
                        resize="none",
                        read_only=True,
                    ),
                ),
                rx.icon(
                    "copy",
                    size=16,
                    color="#c2cad4",
                    position="absolute",
                    bottom="16px",
                    right="16px",
                ),
                position="relative",
                width="100%",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("history", size=16),
                    rx.text("View History", font_weight="600"),
                    spacing="2",
                    align="center",
                ),
                size="3",
                bg="#1a2027",
                color=TEXT,
                width="100%",
                border_radius="999px",
                height="46px",
                border="1px solid #2b343d",
                _hover={"bg": "#202730"},
            ),
            spacing="4",
            align="stretch",
            width="100%",
        ),
        bg=CARD_BG,
        border=CARD_BORDER,
        border_radius="22px",
        padding="22px",
        width="100%",
        box_shadow="0 24px 60px rgba(0, 0, 0, 0.35)",
        height="100%",
    )
