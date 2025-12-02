import json
import re
from pathlib import Path
from typing import List, Optional

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    sync_playwright = None

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def extract_plotly_json_from_html(html_path: Path) -> Optional[dict]:
    """
    Extract Plotly figure JSON from an HTML file.
    
    Args:
        html_path: Path to the HTML file
        
    Returns:
        Plotly figure dictionary or None if not found
    """
    html_content = html_path.read_text(encoding="utf-8")
    

    pattern = r"Plotly\.(?:newPlot|plot)\([^,]+,\s*(\{.*?\})\s*,\s*(\{.*?\})\s*(?:,\s*(\{.*?\}))?\)"
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        data_str = match.group(1)
        layout_str = match.group(2)
        config_str = match.group(3) if match.group(3) else "{}"
        
        try:
            data = json.loads(data_str)
            layout = json.loads(layout_str)
            config = json.loads(config_str) if config_str else {}
            
            return {"data": data, "layout": layout, "config": config}
        except json.JSONDecodeError as e:
            print(f"  ⚠️  Failed to parse JSON in {html_path.name}: {e}")
            return None
    
    pattern2 = r"window\.PLOTLYENV\s*=\s*({.*?});"
    match2 = re.search(pattern2, html_content, re.DOTALL)
    
    if match2:
        pass
    
    pattern3 = r'<script[^>]*id=["\']plotly-data["\'][^>]*>(.*?)</script>'
    match3 = re.search(pattern3, html_content, re.DOTALL)
    
    if match3:
        try:
            figure_json = json.loads(match3.group(1))
            return figure_json
        except json.JSONDecodeError:
            pass

    json_pattern = r'<script[^>]*>(.*?Plotly.*?)</script>'
    for script_match in re.finditer(json_pattern, html_content, re.DOTALL):
        script_content = script_match.group(1)
        json_obj_pattern = r'(\{[^{}]*"data"\s*:\s*\[.*?\])'
        json_match = re.search(json_obj_pattern, script_content, re.DOTALL)
        if json_match:
            try:
                figure_json = json.loads(json_match.group(1))
                return figure_json
            except json.JSONDecodeError:
                continue
    
    return None


def extract_figure_from_html(html_path: Path) -> Optional[go.Figure]:
    """
    Load a Plotly figure from an HTML file.
    
    Args:
        html_path: Path to the HTML file
        
    Returns:
        Plotly figure object or None if extraction failed
    """
    html_content = html_path.read_text(encoding="utf-8")

    plotly_match = re.search(r'Plotly\.(?:newPlot|react)\s*\(', html_content)
    if not plotly_match:
        print("    ⚠️  No Plotly.newPlot or Plotly.react call found")
        return None
    
    start_pos = plotly_match.end()
    
    div_id_match = re.match(r'\s*["\'][^"\']+["\']\s*,', html_content[start_pos:])
    if not div_id_match:
        return None
    
    data_start = start_pos + div_id_match.end()
    
    def extract_json_string(content: str, start: int) -> tuple:
        """Extract a JSON string (array or object) with balanced brackets."""
        if start >= len(content):
            return None, start
        
        first_char = content[start].strip()
        if first_char == '[':
            open_char, close_char = '[', ']'
        elif first_char == '{':
            open_char, close_char = '{', '}'
        else:
            return None, start
        
        depth = 0
        in_string = False
        escape_next = False
        end_pos = start
        
        for i in range(start, len(content)):
            char = content[i]
            
            if escape_next:
                escape_next = False
                continue
            
            if char == '\\':
                escape_next = True
                continue
            
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
            
            if in_string:
                continue
            
            if char == open_char:
                depth += 1
            elif char == close_char:
                depth -= 1
                if depth == 0:
                    end_pos = i + 1
                    break
        
        if depth == 0:
            return content[start:end_pos], end_pos
        return None, start
    
    data_str, data_end = extract_json_string(html_content, data_start)
    if not data_str:
        print("    ⚠️  Failed to extract data array")
        return None
    
    layout_start = data_end
    while layout_start < len(html_content) and html_content[layout_start] in ',\n\r\t ':
        layout_start += 1
    
    layout_str, layout_end = extract_json_string(html_content, layout_start)
    if not layout_str:
        print(" Failed to extract layout dict")
        return None
    
    try:
        data = json.loads(data_str)
        layout = json.loads(layout_str)
        
        fig = go.Figure(data=data, layout=layout)
        return fig
    except json.JSONDecodeError as e:
        print(f"    ⚠️  JSON parse error: {e}")
        return None


def html_to_png_playwright(html_path: Path, output_dir: Optional[Path] = None, width: int = 1200, height: int = 800) -> Optional[Path]:
    """
    Convert an HTML file to PNG image using Playwright (headless browser).
    This is the recommended method as it works reliably for any HTML content.
    
    Args:
        html_path: Path to the HTML file
        output_dir: Directory to save PNG (defaults to same as HTML file)
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        Path to the created PNG file, or None if conversion failed
    """
    if not PLAYWRIGHT_AVAILABLE:
        print("    ⚠️  Playwright is not installed. Install it with: pip install playwright && playwright install")
        return None
    
    if output_dir is None:
        output_dir = html_path.parent
    
    png_path = output_dir / html_path.with_suffix('.png').name
    
    try:
        print(f"    Loading {html_path.name} in browser...")
        
        abs_html_path = html_path.resolve()
        file_url = f"file:///{abs_html_path.as_posix()}"
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": height})
            
            # Load the HTML file
            page.goto(file_url, wait_until="networkidle", timeout=30000)
            
            # Wait for Plotly to render (look for plotly-graph-div elements)
            try:
                page.wait_for_selector(".plotly-graph-div", timeout=10000)
                # Additional wait to ensure Plotly is fully rendered
                page.wait_for_timeout(1000)  # Wait 1 second for animations/rendering
            except Exception:
                # If no plotly-graph-div found, just wait a bit for content to load
                page.wait_for_timeout(2000)
            
            # Take screenshot (viewport size is already set when creating the page)
            print(f"    Taking screenshot ({width}x{height})...")
            page.screenshot(path=str(png_path), full_page=False)
            
            browser.close()
        
        print(f"    ✓ Saved {png_path.name}")
        return png_path
        
    except Exception as e:
        print(f"    ⚠️  Failed to export PNG: {e}")
        return None


def html_to_png(html_path: Path, output_dir: Optional[Path] = None, width: int = 1200, height: int = 800, use_playwright: bool = True) -> Optional[Path]:
    """
    Convert a Plotly HTML file to PNG image.
    
    This function tries Playwright first (recommended), then falls back to
    Plotly's write_image if Playwright is not available.
    
    Args:
        html_path: Path to the HTML file
        output_dir: Directory to save PNG (defaults to same as HTML file)
        width: Image width in pixels
        height: Image height in pixels
        use_playwright: If True, use Playwright (recommended). If False, try Plotly extraction.
        
    Returns:
        Path to the created PNG file, or None if conversion failed
    """
    print(f"  Converting {html_path.name} to PNG...")
    
    # Prefer Playwright if available and requested
    if use_playwright and PLAYWRIGHT_AVAILABLE:
        return html_to_png_playwright(html_path, output_dir, width, height)
    
    # Fallback to Plotly extraction method (requires Kaleido)
    if not PLOTLY_AVAILABLE:
        print("    ⚠️  Neither Playwright nor Plotly available. Install Playwright: pip install playwright && playwright install")
        return None
    
    fig = extract_figure_from_html(html_path)
    if fig is None:
        print(f"    ⚠️  Failed to extract figure from {html_path.name}")
        return None
    
    # Determine output path
    if output_dir is None:
        output_dir = html_path.parent
    
    png_path = output_dir / html_path.with_suffix('.png').name
    
    try:
        print(f"    Exporting to {png_path.name} using Plotly (requires Kaleido)...")
        fig.write_image(str(png_path), width=width, height=height, scale=1)
        print(f"    ✓ Saved {png_path.name}")
        return png_path
    except Exception as e:
        print(f"    ⚠️  Failed to export PNG: {e}")
        print("    💡 Try using Playwright instead: use_playwright=True")
        return None


def batch_convert_html_to_png(
    html_dir: Path,
    pattern: str = "*_plotly.html",
    width: int = 1200,
    height: int = 800,
    use_playwright: bool = True
) -> List[Path]:
    """
    Convert all Plotly HTML files in a directory to PNG images.
    
    Args:
        html_dir: Directory containing HTML files
        pattern: Glob pattern to match HTML files (default: "*_plotly.html")
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        List of paths to created PNG files
    """
    html_dir = Path(html_dir)
    html_files = list(html_dir.glob(pattern))
    
    if not html_files:
        print(f"No HTML files found matching pattern '{pattern}' in {html_dir}")
        return []
    
    print(f"Found {len(html_files)} HTML file(s) to convert...")
    print()
    
    png_files = []
    for i, html_path in enumerate(html_files, 1):
        print(f"[{i}/{len(html_files)}] Processing {html_path.name}...")
        png_path = html_to_png(html_path, output_dir=html_dir, width=width, height=height, use_playwright=use_playwright)
        if png_path:
            png_files.append(png_path)
        print()
    
    print(f"✓ Successfully converted {len(png_files)}/{len(html_files)} HTML files to PNG")
    return png_files


if __name__ == "__main__":
    import sys
    
    # Check if Playwright is available
    if not PLAYWRIGHT_AVAILABLE:
        print("⚠️  Playwright is not installed!")
        print("   Install it with: uv pip install playwright")
        print("   Then install browsers: playwright install chromium")
        print()
        print("   Or install manually: pip install playwright && playwright install chromium")
        sys.exit(1)
    
    # Default: convert all HTML files in notebook_images directory
    html_dir = Path("notebook_images")
    
    # Allow directory to be specified as command line argument
    if len(sys.argv) > 1:
        html_dir = Path(sys.argv[1])
    
    if not html_dir.exists():
        print(f"Error: Directory '{html_dir}' does not exist")
        sys.exit(1)
    
    print(f"Converting Plotly HTML files in: {html_dir}")
    print("Using Playwright (headless browser) for reliable conversion")
    print("=" * 60)
    print()
    
    png_files = batch_convert_html_to_png(html_dir, use_playwright=True)
    
    if png_files:
        print()
        print("Created PNG files:")
        for png_path in png_files:
            print(f"  {png_path}")

