import sys
import os
import argparse
import webview
import markdown
from pygments.formatters import HtmlFormatter

# Cache the Pygments CSS (generated once, never changes)
_PYGMENTS_CSS_CACHE = None

def get_pygments_css():
    """Get Pygments CSS with caching to avoid regeneration."""
    global _PYGMENTS_CSS_CACHE
    if _PYGMENTS_CSS_CACHE is None:
        _PYGMENTS_CSS_CACHE = HtmlFormatter().get_style_defs('.codehilite')
    return _PYGMENTS_CSS_CACHE

def get_icon_path():
    """Find and return the path to the application icon."""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Try different icon locations and formats
    icon_locations = [
        os.path.join(base_dir, 'icon.svg'),       # Installed location
        os.path.join(base_dir, 'icon.png'),       # Installed location
        os.path.join(base_dir, 'icons', 'icon.svg'),  # Development location
        os.path.join(base_dir, 'icons', 'icon.png'),  # Development location
    ]

    for icon_path in icon_locations:
        if os.path.exists(icon_path):
            return icon_path

    return None  # No icon found, will use default

def get_html_content(file_path):
    if not file_path or not os.path.exists(file_path):
        return "<h1>File not found</h1><p>Please provide a valid markdown file.</p>"

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extensions for tables, fenced code blocks, code highlighting
    md_extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc'
    ]

    html_body = markdown.markdown(text, extensions=md_extensions)
    return html_body

def main():
    parser = argparse.ArgumentParser(description="PyMDViewer - A lightweight Markdown viewer")
    parser.add_argument("file", nargs='?', help="Path to the markdown file to view")
    args = parser.parse_args()

    # Determine paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(base_dir, "styles.css")

    # Read Base CSS
    css_content = ""
    if os.path.exists(style_path):
        with open(style_path, 'r') as f:
            css_content = f.read()

    # Add Pygments CSS for code highlighting (cached)
    css_content += "\n" + get_pygments_css()

    content = ""
    title = "PyMDViewer"

    if args.file:
        file_path = os.path.abspath(args.file)
        title = os.path.basename(file_path)
        content = get_html_content(file_path)
    else:
        content = """
        <h1>Welcome to PyMDViewer</h1>
        <p>Usage: <code>pymdviewer path/to/file.md</code></p>
        <p>Or set this application as the default handler for .md files.</p>
        """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            {css_content}
        </style>
    </head>
    <body>
        {content}
    </body>
    </html>
    """

    # Get icon path
    icon_path = get_icon_path()

    # Create window - try Qt backend for better icon support on Linux
    # Qt backend handles window icons more reliably than GTK
    window = webview.create_window(
        title,
        html=full_html,
        width=1000,
        height=800,
        text_select=True
    )

    # Start with Qt backend (better icon support) or fallback to GTK
    if icon_path:
        webview.start(gui='qt', icon=icon_path)
    else:
        webview.start(gui='qt')

if __name__ == '__main__':
    main()
