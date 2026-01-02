import sys
import os
import argparse
import time

# Timing decorator
def measure_time(label):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"[TIMING] {label}: {elapsed:.4f}s", file=sys.stderr)
            return result
        return wrapper
    return decorator

# Measure module imports
print("[TIMING] Starting imports...", file=sys.stderr)
start_total = time.time()

start = time.time()
import webview
print(f"[TIMING] Import webview: {time.time()-start:.4f}s", file=sys.stderr)

start = time.time()
import markdown
print(f"[TIMING] Import markdown: {time.time()-start:.4f}s", file=sys.stderr)

start = time.time()
from pygments.formatters import HtmlFormatter
print(f"[TIMING] Import pygments: {time.time()-start:.4f}s", file=sys.stderr)

@measure_time("get_html_content")
def get_html_content(file_path):
    if not file_path or not os.path.exists(file_path):
        return "<h1>File not found</h1><p>Please provide a valid markdown file.</p>"

    start = time.time()
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"[TIMING]   File read: {time.time()-start:.4f}s", file=sys.stderr)

    # Extensions for tables, fenced code blocks, code highlighting
    md_extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc'
    ]

    start = time.time()
    html_body = markdown.markdown(text, extensions=md_extensions)
    print(f"[TIMING]   Markdown processing: {time.time()-start:.4f}s", file=sys.stderr)
    return html_body

def main():
    parser = argparse.ArgumentParser(description="PyMDViewer - A lightweight Markdown viewer")
    parser.add_argument("file", nargs='?', help="Path to the markdown file to view")
    args = parser.parse_args()

    # Determine paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(base_dir, "styles.css")

    # Read Base CSS
    start = time.time()
    css_content = ""
    if os.path.exists(style_path):
        with open(style_path, 'r') as f:
            css_content = f.read()
    print(f"[TIMING] CSS file read: {time.time()-start:.4f}s", file=sys.stderr)

    # Add Pygments CSS for code highlighting
    start = time.time()
    css_content += "\n" + HtmlFormatter().get_style_defs('.codehilite')
    print(f"[TIMING] Pygments CSS generation: {time.time()-start:.4f}s", file=sys.stderr)

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

    start = time.time()
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
    print(f"[TIMING] HTML template generation: {time.time()-start:.4f}s", file=sys.stderr)

    # Create window
    start = time.time()
    webview.create_window(title, html=full_html, width=1000, height=800)
    print(f"[TIMING] create_window: {time.time()-start:.4f}s", file=sys.stderr)

    print(f"[TIMING] TOTAL (before webview.start): {time.time()-start_total:.4f}s", file=sys.stderr)

    start = time.time()
    webview.start()
    print(f"[TIMING] webview.start: {time.time()-start:.4f}s", file=sys.stderr)

if __name__ == '__main__':
    main()
