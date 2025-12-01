import asyncio
import os
import re
from playwright.async_api import async_playwright
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
from PIL import Image

class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if not any(x in args[0] for x in ['favicon', 'tailwind']):
            print(f"📥 {args[0]}")
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

def fix_image_paths(html_content: str, html_relative_path: str) -> str:
    """
    Since images in HTML are relative to the HTML file location,
    and the HTML is in data/, we need to preserve that context.
    """
    html_dir = os.path.dirname(html_relative_path)
    
    print(f"\n🔧 Fixing image paths (HTML is in: {html_dir})")
    
    # Pattern to match src attributes
    pattern = r'src="(?!(?:http://|https://|data:))([^"]+)"'
    
    def replace_src(match):
        relative_path = match.group(1)
        
        # Clean up the path
        clean_path = relative_path.lstrip('./')
        
        # Build absolute path: since HTML is in data/, 
        # images referenced as "notebook/..." are actually "data/notebook/..."
        if html_dir:
            full_path = f"{html_dir}/{clean_path}"
        else:
            full_path = clean_path
        
        # Remove any double slashes
        full_path = full_path.replace('//', '/')
        
        new_src = f'src="http://localhost:8000/{full_path}"'
        print(f"   {relative_path} → /{full_path}")
        return new_src
    
    fixed_html = re.sub(pattern, replace_src, html_content)
    return fixed_html

def start_http_server(root_dir: str, port: int = 8000):
    """Start a local HTTP server in a background thread."""
    original_dir = os.getcwd()
    os.chdir(root_dir)
    
    print(f"📁 HTTP Server root: {os.getcwd()}")
    print(f"📂 Contents:")
    for item in os.listdir('.')[:10]:  # Show first 10 items
        print(f"   - {item}")
    
    server = HTTPServer(("localhost", port), QuietHTTPRequestHandler)
    
    def serve():
        try:
            server.serve_forever()
        finally:
            os.chdir(original_dir)
    
    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    time.sleep(1.5)
    print(f"🌐 HTTP Server started at http://localhost:{port}\n")
    return server

def verify_image_paths(html_content: str, root_dir: str):
    """Check if image files actually exist"""
    print("\n🔍 Verifying image files exist:")
    pattern = r'src="http://localhost:8000/([^"]+)"'
    matches = re.findall(pattern, html_content)
    
    missing = []
    found = []
    
    for img_path in matches:
        full_path = os.path.join(root_dir, img_path)
        if os.path.exists(full_path):
            found.append(img_path)
            print(f"   ✅ {img_path}")
        else:
            missing.append(img_path)
            print(f"   ❌ {img_path} (NOT FOUND)")
    
    print(f"\n📊 Summary: {len(found)} found, {len(missing)} missing")
    
    if missing:
        print("\n⚠️  Missing files - checking alternative locations:")
        for img_path in missing[:3]:  # Check first 3 missing
            # Try to find the file
            filename = os.path.basename(img_path)
            print(f"\n   Looking for: {filename}")
            for root, dirs, files in os.walk(root_dir):
                if filename in files:
                    rel_path = os.path.relpath(os.path.join(root, filename), root_dir)
                    print(f"   💡 Found at: {rel_path}")
                    break
    
    return len(missing) == 0

def images_to_pdf(image_paths: list, output_filename: str):
    """Convert a list of images to a single PDF."""
    print(f"\n📄 Converting {len(image_paths)} screenshots to PDF...")
    
    # Open all images
    images = []
    for img_path in image_paths:
        img = Image.open(img_path)
        # Convert to RGB if necessary (PDF doesn't support RGBA)
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            images.append(rgb_img)
        else:
            images.append(img.convert('RGB'))
    
    if images:
        images[0].save(
            output_filename,
            save_all=True,
            append_images=images[1:],
            resolution=300.0,
            quality=95,
            optimize=False
        )
        print(f"✅ PDF created: {output_filename}")
    

    print("🗑️  Cleaning up temporary screenshots...")
    for img_path in image_paths:
        try:
            os.remove(img_path)
        except:
            pass

async def html_to_pdf(html_source: str, output_filename: str, port: int = 8000):
    """Converts HTML content to PDF by taking screenshots of each slide."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            color_scheme='dark',
            device_scale_factor=2,
        )
        page = await context.new_page()
        
        failed_requests = []
        page.on("requestfailed", lambda request: failed_requests.append(request.url))
        
        print("📄 Loading HTML content...")
        await page.set_content(html_source, wait_until="domcontentloaded")
        
        print("⏳ Waiting for images to load...")
        try:
            await page.wait_for_load_state("networkidle", timeout=30000)
        except Exception as e:
            print(f"⚠️  Timeout: {e}")
        
        await asyncio.sleep(2)
        
        img_status = await page.evaluate("""() => {
            const images = document.querySelectorAll('img');
            let loaded = 0, failed = 0;
            const failedSrcs = [];
            
            images.forEach(img => {
                if (img.complete && img.naturalHeight !== 0) {
                    loaded++;
                } else {
                    failed++;
                    failedSrcs.push(img.src);
                }
            });
            
            return {total: images.length, loaded, failed, failedSrcs};
        }""")
        
        print(f"\n📊 Image Status: {img_status['loaded']}/{img_status['total']} loaded")
        
        if img_status['failed'] > 0:
            print(f"❌ {img_status['failed']} images failed to load:")
            for src in img_status['failedSrcs'][:5]:
                print(f"   - {src}")
        
        if failed_requests:
            print(f"\n❌ Failed HTTP requests:")
            for url in set(failed_requests)[:5]:
                print(f"   - {url}")
        
        # Get all slides
        slide_count = await page.evaluate("""() => {
            return document.querySelectorAll('.slide').length;
        }""")
        
        print(f"\n📊 Found {slide_count} slides")
        print("📸 Taking screenshots of each slide...")
        
        # Create temp directory for screenshots
        temp_dir = "temp_screenshots"
        os.makedirs(temp_dir, exist_ok=True)
        
        screenshot_paths = []
        
        # Screenshot each slide
        for i in range(slide_count):
            print(f"   📸 Slide {i+1}/{slide_count}...", end=" ")
            
            # Scroll to the slide
            await page.evaluate(f"""() => {{
                const slides = document.querySelectorAll('.slide');
                slides[{i}].scrollIntoView({{block: 'start', inline: 'nearest'}});
            }}""")
            
            await asyncio.sleep(0.5)  # Wait for scroll
            
            # Get slide element
            slide = await page.query_selector(f'.slide:nth-of-type({i+1})')
            
            if slide:
                screenshot_path = os.path.join(temp_dir, f"slide_{i+1:03d}.png")
                await slide.screenshot(
                    path=screenshot_path,
                    type='png',
                )
                screenshot_paths.append(screenshot_path)
                print("✅")
            else:
                print("❌ Failed")
        
        await browser.close()
        
        # Convert screenshots to PDF
        if screenshot_paths:
            images_to_pdf(screenshot_paths, output_filename)
            
            # Remove temp directory
            try:
                os.rmdir(temp_dir)
            except:
                pass
        else:
            print("❌ No screenshots were taken!")

async def main():
    current_dir = os.getcwd()
    
    input_html_filename = "Final_slides.html"
    output_pdf_filename = "final_presentation_inflation.pdf"
    
    html_path = os.path.join(current_dir, input_html_filename)
    
    if not os.path.exists(html_path):
        print(f"❌ Error: Could not find {input_html_filename}")
        print(f"   Looking in: {html_path}")
        return
    
    print(f"📂 Project root: {current_dir}")
    print(f"📄 HTML file: {html_path}\n")
    
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            raw_html = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    # Start HTTP server
    server = start_http_server(current_dir)
    
    try:
        # Fix image paths
        final_html = fix_image_paths(raw_html, input_html_filename)
        
        # Save debug HTML
        debug_path = os.path.join(current_dir, "debug_fixed.html")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"\n💾 Debug HTML saved: {debug_path}")
        
        # Verify files exist
        all_found = verify_image_paths(final_html, current_dir)
        
        if not all_found:
            print("\n⚠️  WARNING: Some images are missing!")
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Aborted.")
                return
        
        print(f"\n🌐 You can test in browser: http://localhost:8000/debug_fixed.html")
        print("   (Press Ctrl+C in another terminal to stop if needed)\n")
        

        await html_to_pdf(final_html, output_pdf_filename)
        
    finally:
        server.shutdown()
        print("\n🛑 HTTP Server stopped")

if __name__ == "__main__":
    asyncio.run(main())