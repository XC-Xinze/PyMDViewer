#!/bin/bash

APP_NAME="pymdviewer"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Installing $APP_NAME..."

# 1. Create directory and copy files
mkdir -p "$INSTALL_DIR"
cp app.py styles.css requirements.txt "$INSTALL_DIR"

# Copy icon if it exists
if [ -f "icons/icon.svg" ]; then
    cp icons/icon.svg "$INSTALL_DIR/"
    ICON_PATH="$INSTALL_DIR/icon.svg"
    echo "Using custom SVG icon"
elif [ -f "icons/icon.png" ]; then
    cp icons/icon.png "$INSTALL_DIR/"
    ICON_PATH="$INSTALL_DIR/icon.png"
    echo "Using custom PNG icon"
else
    # Fallback to system icon
    ICON_PATH="text-markdown"
    echo "No custom icon found, using system icon"
fi

# 2. Setup Virtual Environment
echo "Setting up virtual environment..."
# Use --system-site-packages to access system GTK (PyGObject) for faster startup
python3 -m venv --system-site-packages "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"
pip install -r "$INSTALL_DIR/requirements.txt"
deactivate

# 3. Create Launcher Script
echo "Creating launcher..."
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/$APP_NAME" <<EOF
#!/bin/bash
source "$INSTALL_DIR/venv/bin/activate"
python "$INSTALL_DIR/app.py" "\$@"
deactivate
EOF
chmod +x "$BIN_DIR/$APP_NAME"

# 4. Create Desktop Entry
echo "Creating desktop entry..."
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_DIR/$APP_NAME.desktop" <<EOF
[Desktop Entry]
Name=PyMDViewer
Comment=Lightweight Markdown Viewer
Exec=$BIN_DIR/$APP_NAME %f
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Utility;TextTools;
MimeType=text/markdown;text/x-markdown;
EOF

# Update desktop database
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo "Installation complete!"
echo "You can now run '$APP_NAME <file>' from terminal"
echo "or right-click a Markdown file and choose 'Open With -> PyMDViewer'."
