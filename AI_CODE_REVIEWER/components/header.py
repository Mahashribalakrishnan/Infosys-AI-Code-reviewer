import reflex as rx
from AI_CODE_REVIEWER.state import State

ACCENT = "#38d4ff"
TEXT = "#e8edf2"
MUTED = "#97a3b6"
HEADER_BG = "rgba(11, 15, 20, 0.92)"


def nav_item(label: str, href: str, is_active: rx.Var):
    return rx.link(
        rx.vstack(
            rx.text(
                label,
                color=rx.cond(is_active, TEXT, MUTED),
                font_size="14px",
                font_weight="600",
                letter_spacing="0.2px",
            ),
            rx.box(
                height="2px",
                width="18px",
                bg=rx.cond(is_active, ACCENT, "transparent"),
                border_radius="999px",
            ),
            spacing="1",
            align="center",
        ),
        href=href,
        color="inherit",
        text_decoration="none",
    )


def header():
    return rx.box(
        rx.hstack(
            rx.text(
                "AI CodeReviewer",
                font_size="16px",
                font_weight="600",
                color=TEXT,
                letter_spacing="0.3px",
            ),
            rx.hstack(
                nav_item("Home", "/", State.current_page == "home"),
                nav_item("History", "/history", State.current_page == "history"),
                nav_item("Reports", "/reports", State.current_page == "reports"),
                spacing="6",
                align="center",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        padding="18px 48px",
        bg=HEADER_BG,
        border_bottom="1px solid rgba(255, 255, 255, 0.06)",
        width="100%",
        position="sticky",
        top="0",
        z_index="100",
        style={"backdrop_filter": "blur(12px)"},
    )
