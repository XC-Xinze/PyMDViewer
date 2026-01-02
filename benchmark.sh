#!/bin/bash
# Benchmark script to measure startup performance

echo "======================================"
echo "PyMDViewer Performance Benchmark"
echo "======================================"
echo ""

# Check which backend is being used
echo "Testing backend detection..."
source ~/.local/share/pymdviewer/venv/bin/activate

python3 << 'EOF'
import webview
import time
import sys

print("Creating test window...")
window = webview.create_window('Benchmark', html='<h1>Testing...</h1>', width=400, height=300)

start_time = time.time()

def on_shown():
    elapsed = time.time() - start_time
    print(f"\n✓ Window appeared in: {elapsed:.3f}s")
    if elapsed < 1.0:
        print("✓ Performance: EXCELLENT (< 1s)")
    elif elapsed < 2.0:
        print("✓ Performance: GOOD (< 2s)")
    else:
        print("⚠ Performance: SLOW (> 2s)")

    import threading
    def close():
        time.sleep(0.3)
        window.destroy()
    threading.Thread(target=close, daemon=True).start()

window.events.shown += on_shown

print("Starting webview with GTK backend...")
start_time = time.time()
webview.start(gui='gtk', debug=False)
print("\nBenchmark complete!")
EOF

deactivate

echo ""
echo "======================================"
echo "Expected results:"
echo "  - GTK backend: < 1s (OPTIMIZED)"
echo "  - Qt backend: 3-4s (SLOW)"
echo "======================================"
