import flet as ft
import os
import asyncio
from scraper import async_scraper

def main(page: ft.Page):
    page.title = "🕸️ Webscraper Quotes"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    page.padding = 20

    # Título
    page.add(ft.Text("🕸️ Webscraper Quotes", size=32, weight="bold", color=ft.Colors.CYAN_400))

    # Status
    status = ft.Text("Defina o número de páginas e clique em 'Rodar Scraper'.", size=16, color=ft.Colors.WHITE70)
    page.add(status)

    # Input para número de páginas
    pages_input = ft.TextField(
        label="Número de páginas (0 = todas)",
        value="0",
        width=250,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
    )

    # Campo de busca (autor/tag)
    search_input = ft.TextField(
        label="Filtrar por autor ou tag",
        value="",
        width=300,
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        on_change=lambda e: apply_filter(),
    )

    page.add(ft.Row([pages_input, search_input], spacing=20))

    # Preview com scroll
    quotes_preview = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=False, height=400)
    page.add(quotes_preview)

    quotes_data = []

    def run_scraper(e):
        nonlocal quotes_data
        try:
            max_pages = int(pages_input.value)
        except ValueError:
            status.value = "⚠️ Digite um número válido para páginas."
            page.update()
            return

        status.value = "⏳ Coletando dados..."
        quotes_preview.controls.clear()
        page.update()

        # roda o scraper assíncrono
        quotes_data = asyncio.run(
            async_scraper.crawl_all_quotes(max_pages=max_pages if max_pages > 0 else None)
        )
        status.value = f"✅ {len(quotes_data)} citações coletadas!"

        render_quotes(quotes_data)
        page.update()

    def render_quotes(data):
        """Renderiza citações na ListView"""
        quotes_preview.controls.clear()
        for q in data:
            quotes_preview.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"“{q.text}”", size=16, italic=True, color=ft.Colors.WHITE),
                            ft.Text(f"- {q.author}", weight="bold", color=ft.Colors.CYAN_300),
                            ft.Text(f"Tags: {', '.join(q.tags)}", size=12, color=ft.Colors.WHITE70),
                        ],
                        spacing=2,
                    ),
                    padding=10,
                    border_radius=8,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                )
            )

    def apply_filter():
        """Aplica filtro por autor ou tag"""
        query = search_input.value.strip().lower()
        if not query:
            render_quotes(quotes_data)
        else:
            filtered = [
                q for q in quotes_data
                if query in q.author.lower() or any(query in tag.lower() for tag in q.tags)
            ]
            render_quotes(filtered)
        page.update()

    def export_csv(e):
        if not quotes_data:
            status.value = "⚠️ Nenhuma citação coletada ainda."
        else:
            os.makedirs("data", exist_ok=True)
            async_scraper.save_to_csv(quotes_data, "data/quotes_ui.csv")
            status.value = "💾 Exportado para data/quotes_ui.csv"
        page.update()

    def export_json(e):
        if not quotes_data:
            status.value = "⚠️ Nenhuma citação coletada ainda."
        else:
            os.makedirs("data", exist_ok=True)
            async_scraper.save_to_json(quotes_data, "data/quotes_ui.json")
            status.value = "💾 Exportado para data/quotes_ui.json"
        page.update()

    # Botão estilizado (hover com overlay_color)
    def styled_button(text, icon, on_click, color):
        return ft.ElevatedButton(
            text,
            icon=ft.Icon(name=icon),
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor=color,
                color=ft.Colors.WHITE,
                overlay_color=ft.Colors.BLUE_700,  # efeito hover
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=5,
            ),
        )

    btn_scrape = styled_button("Rodar Scraper", "play_arrow", run_scraper, ft.Colors.CYAN_700)
    btn_csv = styled_button("Exportar CSV", "file_present", export_csv, ft.Colors.GREEN_700)
    btn_json = styled_button("Exportar JSON", "data_object", export_json, ft.Colors.AMBER_700)

    page.add(ft.Row([btn_scrape, btn_csv, btn_json], alignment="center", spacing=15))

ft.app(target=main)
