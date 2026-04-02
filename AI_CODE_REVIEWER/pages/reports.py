import reflex as rx
from AI_CODE_REVIEWER.components.header import header
from AI_CODE_REVIEWER.state import State

def reports_page():
    return rx.box(
        rx.vstack(
            header(),
            
            # Page title
            rx.heading("Code Analysis Reports", size="5", color="white", margin_top="2em", padding_x="2em"),
            
            # Current analysis report
            rx.cond(
                State.summary != "",
                rx.card(
                    rx.vstack(
                        rx.heading("Latest Analysis Report", size="4", color="white"),
                        
                        # Report summary
                        rx.vstack(
                            rx.hstack(
                                rx.text("Quality Score:", color="gray"),
                                rx.text(State.analysis_score, color="white", font_weight="bold"),
                                rx.text("/100", color="gray"),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.text("Issues Found:", color="gray"),
                                rx.text(State.errors.length(), color="white", font_weight="bold"),
                                spacing="2"
                            ),
                            rx.hstack(
                                rx.text("Suggestions:", color="gray"),
                                rx.text(State.optimizations.length(), color="white", font_weight="bold"),
                                spacing="2"
                            ),
                            spacing="3"
                        ),
                        
                        # Code section
                        rx.vstack(
                            rx.heading("Analyzed Code", size="3", color="white"),
                            rx.box(
                                rx.text_area(
                                    value=State.code,
                                    height="300px",
                                    width="100%",
                                    font_family="monospace",
                                    font_size="12px",
                                    bg="#1a1a1a",
                                    color="white",
                                    border="1px solid #333",
                                    read_only=True
                                ),
                                border_radius="8px",
                                overflow="hidden",
                                width="100%"
                            ),
                            spacing="2"
                        ),
                        
                        # Issues section
                        rx.cond(
                            State.errors.length() > 0,
                            rx.vstack(
                                rx.heading("Issues Found", size="3", color="white"),
                                rx.vstack(
                                    rx.foreach(
                                        State.errors,
                                        lambda error: rx.callout(
                                            rx.hstack(
                                                rx.text("⚠️", color="#f59e0b"),
                                                rx.text(error, color="white"),
                                                spacing="2"
                                            ),
                                            bg="#1e293b",
                                            border="1px solid #334155",
                                            padding="8px 12px"
                                        )
                                    ),
                                    spacing="2"
                                ),
                                spacing="3"
                            )
                        ),
                        
                        # Suggestions section
                        rx.cond(
                            State.optimizations.length() > 0,
                            rx.vstack(
                                rx.heading("AI Suggestions", size="3", color="white"),
                                rx.vstack(
                                    rx.foreach(
                                        State.optimizations,
                                        lambda suggestion: rx.callout(
                                            rx.hstack(
                                                rx.text("💡", color="#10b981"),
                                                rx.text(suggestion, color="white"),
                                                spacing="2"
                                            ),
                                            bg="#1e293b",
                                            border="1px solid #334155",
                                            padding="8px 12px"
                                        )
                                    ),
                                    spacing="2"
                                ),
                                spacing="3"
                            )
                        ),
                        
                        # Download button
                        rx.button(
                            "📄 Download Full Report",
                            on_click=State.download_report,
                            color_scheme="blue",
                            size="3"
                        ),
                        
                        spacing="4",
                        align="stretch",
                        width="100%"
                    ),
                    
                    bg="#1e293b",
                    border="1px solid #334155",
                    border_radius="12px",
                    padding="32px",
                    width="100%"
                ),
                
                # No analysis yet message
                rx.card(
                    rx.vstack(
                        rx.heading("No Analysis Available", size="4", color="white"),
                        rx.text(
                            "Please analyze some code first to generate a report.",
                            color="gray",
                            text_align="center"
                        ),
                        rx.link(
                            rx.button("Go to Home", color_scheme="blue"),
                            href="/"
                        ),
                        spacing="4",
                        align="center"
                    ),
                    bg="#1e293b",
                    border="1px solid #334155",
                    border_radius="12px",
                    padding="32px",
                    width="100%"
                )
            ),
            
            spacing="6",
            align="center",
            width="100%",
            padding_x="2em"
        ),
        
        bg="#0f172a",
        min_height="100vh",
        width="100%",
        on_mount=State.set_current_page("reports")
    )
