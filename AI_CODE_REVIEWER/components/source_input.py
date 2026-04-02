import reflex as rx
from AI_CODE_REVIEWER.state import State

CARD_BG = "#141a1f"
CARD_BORDER = "1px solid #1f2730"
TEXT = "#e8edf2"
MUTED = "#93a1b2"
ACCENT = "#38d4ff"
INPUT_BG = "#22282f"


def source_input_section():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon("code", size=14, color=ACCENT),
                        width="24px",
                        height="24px",
                        border_radius="7px",
                        bg="rgba(56, 212, 255, 0.15)",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                    rx.text(
                        "SOURCE CODE INPUT",
                        font_size="12px",
                        letter_spacing="1px",
                        font_weight="700",
                        color=MUTED,
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.badge(
                    "PYTHON",
                    bg="#1b2a31",
                    color="#9be4ff",
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
                rx.text_area(
                    placeholder="// Paste your code here...",
                    value=State.code,
                    on_change=State.set_code,
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
                    rx.icon("sparkles", size=16),
                    rx.text("Review Code", font_weight="700"),
                    spacing="2",
                    align="center",
                ),
                size="3",
                bg=ACCENT,
                color="#0b0f14",
                on_click=State.analyze,
                loading=State.loading,
                disabled=State.loading,
                width="100%",
                border_radius="999px",
                height="46px",
                box_shadow="0 8px 24px rgba(56, 212, 255, 0.35)",
                _hover={"filter": "brightness(1.05)"},
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
