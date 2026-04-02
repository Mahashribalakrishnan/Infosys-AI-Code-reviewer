import reflex as rx
from AI_CODE_REVIEWER.state import State

def history_section():
    return rx.card(
        rx.vstack(
            rx.heading("Analysis History", size="4", color="white", font_weight="bold"),
            
            rx.cond(
                State.analysis_history.length() > 0,
                rx.vstack(
                    rx.foreach(
                        State.analysis_history,
                        lambda entry: rx.vstack(
                            # Header with timestamp
                            rx.hstack(
                                rx.text(entry["timestamp"], color="gray", font_size="12px"),
                                rx.button(
                                    "Load",
                                    size="1",
                                    color_scheme="blue",
                                    on_click=lambda e=entry: State.load_history_entry(e)
                                ),
                                justify="between",
                                align="start",
                                width="100%"
                            ),
                            
                            # Code preview
                            rx.text(
                                entry["code_preview"],
                                color="white",
                                font_family="monospace",
                                font_size="11px",
                                bg="#1a1a1a",
                                padding="8px",
                                border_radius="4px",
                                width="100%",
                                overflow="hidden",
                                text_overflow="ellipsis",
                                white_space="nowrap"
                            ),
                            
                            spacing="2",
                            padding="8px",
                            border_bottom="1px solid #334155",
                            width="100%"
                        )
                    ),
                    spacing="0",
                    width="100%",
                    max_height="400px",
                    overflow_y="auto"
                ),
                rx.vstack(
                    rx.text("No analysis history yet.", color="gray"),
                    rx.text("Start analyzing code to see your history here.", color="gray", font_size="12px"),
                    spacing="2",
                    align="center",
                    padding="20px"
                )
            ),
            
            spacing="4",
            align="stretch",
            width="100%"
        ),
        
        bg="#1e293b",
        border="1px solid #334155",
        border_radius="12px",
        padding="24px",
        width="100%",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    )