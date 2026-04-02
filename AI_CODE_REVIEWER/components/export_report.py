import reflex as rx
from AI_CODE_REVIEWER.state import State

def export_report_section():
    return rx.card(
        rx.vstack(
            # Section header
            rx.heading("Export Detailed Report", size="4", color="white", font_weight="bold"),
            
            # Report content preview
            rx.cond(
                State.summary != "",
                rx.vstack(
                    rx.text(
                        "Your comprehensive code analysis report is ready with:",
                        color="white",
                        font_size="16px"
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.cond(
                                State.errors.length() > 0,
                                rx.hstack(
                                    rx.text("📊 ", color="white"),
                                    rx.text(State.errors.length(), color="white"),
                                    rx.text(" Issues Found", color="white"),
                                    spacing="0"
                                ),
                                rx.text("📊 0 Issues Found", color="white")
                            ),
                            rx.cond(
                                State.optimizations.length() > 0,
                                rx.hstack(
                                    rx.text("💡 ", color="white"),
                                    rx.text(State.optimizations.length(), color="white"),
                                    rx.text(" Suggestions", color="white"),
                                    spacing="0"
                                ),
                                rx.text("💡 0 Suggestions", color="white")
                            ),
                            spacing="2"
                        ),
                        rx.vstack(
                            rx.cond(
                                State.style.length() > 0,
                                rx.hstack(
                                    rx.text("🔍 ", color="white"),
                                    rx.text(State.style.length(), color="white"),
                                    rx.text(" Style Checks", color="white"),
                                    spacing="0"
                                ),
                                rx.text("🔍 0 Style Checks", color="white")
                            ),
                            rx.hstack(
                                rx.text("📈 ", color="white"),
                                rx.text(State.summary, color="white"),
                                spacing="0"
                            ),
                            spacing="2"
                        ),
                        spacing="6",
                        width="100%"
                    ),
                    spacing="4"
                ),
                rx.text(
                    "Run a code analysis first to generate your detailed report.",
                    color="gray",
                    text_align="center",
                    padding="20px"
                )
            ),
            
            # Export buttons
            rx.hstack(
                rx.button(
                    "📄 Download PDF",
                    color_scheme="blue",
                    size="2",
                    is_disabled=State.summary == ""
                ),
                rx.button(
                    "📋 Download Text",
                    color_scheme="gray",
                    size="2",
                    is_disabled=State.summary == "",
                    on_click=State.download_report
                ),
                spacing="4"
            ),
            
            spacing="4",
            align="center",
            width="100%"
        ),
        
        bg="#1e293b",
        border="1px solid #334155",
        border_radius="12px",
        padding="32px",
        width="100%",
        max_width="800px",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    )
