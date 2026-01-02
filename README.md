# PyMDViewer

A lightweight, fast Markdown viewer for Linux with syntax highlighting and dark mode support.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## ✨ Features

- 🚀 **Ultra-fast startup** (~0.2s with GTK backend)
- 🎨 **Syntax highlighting** for code blocks (Pygments)
- 🌓 **Dark mode** support (auto-detects system preference)
- 📊 **Tables, TOC, and extended Markdown** support
- 🖼️ **Custom icon** support
- 📦 **Lightweight** (~10MB installation)
- 🔧 **Easy integration** with file managers (right-click to open)

## 🎯 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pymdviewer.git
cd pymdviewer

# Run the installer
./install.sh
```

The installer will:

- Create a virtual environment at `~/.local/share/pymdviewer`
- Install dependencies (pywebview, markdown, pygments)
- Create a launcher at `~/.local/bin/pymdviewer`
- Add a desktop entry for "Open With" integration
- Copy your custom icon (if provided)

### Usage

```bash
# View a markdown file
pymdviewer README.md

# Or right-click any .md file and choose "Open With → PyMDViewer"
```

## 📋 Requirements

- **Python 3.8+**
- **PyGObject** (python3-gobject) - Usually pre-installed on Linux
- **GTK3** - Standard on most Linux desktops

On Fedora (usually already installed):

```bash
sudo dnf install python3-gobject gtk3
```

On Ubuntu/Debian:

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.0
```

## ⚡ Performance

PyMDViewer is optimized for speed:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Startup time | 3.7s | 0.2s | **95% faster** |
| Installation size | ~150MB | ~10MB | **93% smaller** |
| Backend | Qt | GTK | **20x speedup** |

See [PERFORMANCE_IMPROVEMENTS.md](PERFORMANCE_IMPROVEMENTS.md) for technical details.

## 📁 Project Structure

```
pymdviewer/
├── app.py                    # Main application
├── styles.css                # GitHub-style CSS
├── requirements.txt          # Python dependencies
├── install.sh                # Installation script
├── icons/                    # Icon files
│   ├── icon.svg             # Application icon
│   └── README.md            # Icon documentation
├── demo.md                   # Example markdown file
├── README.md                 # This file
```

## 🔧 Development

### Running from source (without installing)

```bash
# Create virtual environment with system packages
python3 -m venv --system-site-packages venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py demo.md
```

### Testing performance

```bash
./benchmark.sh
```

Expected output:

```
✓ Window appeared in: 0.2s
✓ Performance: EXCELLENT (< 1s)
```

## 🛠️ Technical Details

- **Backend**: pywebview with GTK (WebKit2GTK)
- **Markdown**: python-markdown with extensions (extra, codehilite, tables, toc)
- **Syntax highlighting**: Pygments
- **CSS**: GitHub-flavored with dark mode support
- **Caching**: Pygments CSS is cached for faster startup

## 📝 Supported Markdown Features

- Headers, paragraphs, lists
- **Bold**, *italic*, `code`
- Code blocks with syntax highlighting
- Tables
- Blockquotes
- Links and images
- Table of contents
- Fenced code blocks
- And more (via markdown.extensions.extra)

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 🐛 Troubleshooting

### App doesn't start

```bash
# Check if GTK is available
python3 -c "import gi; print('GTK OK')"

# Check installation
ls ~/.local/share/pymdviewer/
```

### Icon doesn't appear

```bash
# Update desktop database
update-desktop-database ~/.local/share/applications/

# Check icon path
cat ~/.local/share/applications/pymdviewer.desktop | grep Icon
```

### Slow startup

- Make sure you're using the GTK backend (not Qt)
- Reinstall with `./install.sh` to apply optimizations
- Run `./benchmark.sh` to test performance

## 📚 Documentation

- [ICON_SETUP.md](ICON_SETUP.md) - How to customize the application icon
- [PERFORMANCE_IMPROVEMENTS.md](PERFORMANCE_IMPROVEMENTS.md) - Performance optimization details
- [README_OPTIMIZATION.md](README_OPTIMIZATION.md) - Quick optimization summary

## ⭐ Acknowledgments

- Markdown rendering: [python-markdown](https://python-markdown.github.io/)
- Syntax highlighting: [Pygments](https://pygments.org/)
- Webview: [pywebview](https://pywebview.flowrl.com/)
- Styling inspired by GitHub's Markdown renderer

---

**Made with ❤️ for the Linux community**
