import asyncio
import os
import re
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
from PIL import Image
from core.convert_image_base64 import embed_images_as_base64
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


import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from PIL import Image
import os

async def html_to_pdf(html_source: str, output_filename: str):
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
        try:
            await page.set_content(html_source, wait_until="domcontentloaded", timeout=120000)
        except PlaywrightTimeoutError as exc:
            print(f"⚠️ Timeout while setting content (domcontentloaded). Retrying without wait condition. Details: {exc}")
            await page.set_content(html_source, timeout=120000)

        print("⏳ Waiting for images to load...")
        try:
            await page.wait_for_load_state("networkidle", timeout=30000)
        except Exception as e:
            print(f"⚠️ Timeout: {e}")

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

        print(f"\n🖼 Image Status: {img_status['loaded']}/{img_status['total']} loaded")
        if img_status['failed'] > 0:
            print(f"⚠️ {img_status['failed']} images failed to load:")
            for src in img_status['failedSrcs'][:5]:
                print(f"   - {src}")

        if failed_requests:
            print(f"\n❌ Failed HTTP requests:")
            for url in set(failed_requests):
                print(f"   - {url}")

        slide_count = await page.evaluate("""() => {
            return document.querySelectorAll('.slide').length;
        }""")

        print(f"\n📊 Found {slide_count} slides")
        print("📸 Taking screenshots of each slide...")

        temp_dir = "temp_screenshots"
        os.makedirs(temp_dir, exist_ok=True)
        screenshot_paths = []

        for i in range(slide_count):
            print(f"   📸 Slide {i+1}/{slide_count}...", end=" ")

            await page.evaluate(f"""() => {{
                const slides = document.querySelectorAll('.slide');
                slides[{i}].scrollIntoView({{block: 'start', inline: 'nearest'}});
            }}""")

            await asyncio.sleep(0.5)
            slide = await page.query_selector(f'.slide:nth-of-type({i+1})')

            if slide:
                screenshot_path = os.path.join(temp_dir, f"slide_{i+1:03d}.png")
                await slide.screenshot(path=screenshot_path, type='png')
                screenshot_paths.append(screenshot_path)
                print("✅")
            else:
                print("❌ Failed")

        await browser.close()

        if screenshot_paths:
            images_to_pdf(screenshot_paths, output_filename)

            try:
                os.rmdir(temp_dir)
            except:
                pass
        else:
            print(" No screenshots were taken!")


async def pass_html_get_pdf(
    file_path: str,
    out_file_name: str = "final_presentation.pdf",
    save_debug: bool = True,
):
    html_path = Path(file_path).expanduser().resolve()

    if not html_path.exists():
        print(f"❌ Error: Could not find {html_path}")
        return

    print(f"📄 HTML file: {html_path}")

    try:
        final_html = html_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return


    if save_debug:
        debug_path = html_path.parent / "debug_embedded.html"
        debug_path.write_text(final_html, encoding="utf-8")
        print(f"🐞 Debug HTML with embedded images saved: {debug_path}")

    await html_to_pdf(final_html, out_file_name)
    print(f"\n Done. PDF saved as: {out_file_name}")
