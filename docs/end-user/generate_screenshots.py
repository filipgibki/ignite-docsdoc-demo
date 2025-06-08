import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Configuration
APP_URL = "http://localhost:5173"
SCREENSHOTS_DIR = Path(__file__).parent / "docs" / "assets" / "screenshots"

# Ensure the screenshot directory exists
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# JavaScript to create a fake cursor using an SVG
JS_CREATE_CURSOR = """
    () => {
        const cursor = document.createElement('div');
        cursor.id = 'playwright-mouse-cursor';
        cursor.style.position = 'absolute';
        cursor.style.width = '24px';
        cursor.style.height = '24px';
        cursor.style.zIndex = '99999';
        cursor.style.pointerEvents = 'none';
        cursor.style.transition = 'left 0.1s ease-in-out, top 0.1s ease-in-out';
        cursor.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 28" fill="black" style="filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.4));">
            <path fill="white" d="M4.23 23.77L15.5 4.5l6.49 6.49L10.72 22.25l-3.1-3.1.9-2.2 3.1 3.1 2.2-.9L21.99 11l-6.49-6.49L4.23 23.77z"/>
            <path d="M10.72 22.25l-6.49-6.48 11.27-11.27 6.49 6.49-11.27 11.26zm-5.59-6.48l5.59 5.59 10.37-10.37-5.59-5.59-10.37 10.37z"/>
        </svg>`;
        document.body.appendChild(cursor);
    }
"""

# JavaScript to move the fake cursor
JS_MOVE_CURSOR = """
    ([x, y]) => {
        const cursor = document.getElementById('playwright-mouse-cursor');
        if (cursor) {
            cursor.style.left = x + 'px';
            cursor.style.top = y + 'px';
        }
    }
"""

async def move_mouse_and_update_cursor(page, locator):
    """Moves the mouse to the center of a locator and updates the fake cursor."""
    box = await locator.bounding_box()
    if box:
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2
        await page.mouse.move(x, y)
        await page.evaluate(JS_MOVE_CURSOR, [x, y])
        await page.wait_for_timeout(200) # Give cursor time to move

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})

        try:
            print(f"Navigating to {APP_URL}...")
            await page.goto(APP_URL, wait_until="domcontentloaded")
            await page.wait_for_selector('h1:has-text("To-Do List")')
            print("App loaded successfully.")

            # Inject the fake cursor into the page
            await page.evaluate(JS_CREATE_CURSOR)

            # 1. Initial view screenshot (Full page)
            print("Taking screenshot: 01-initial-view.png")
            await page.screenshot(path=SCREENSHOTS_DIR / "01-initial-view.png")

            # 2. Adding a task screenshot (Partial)
            print("Taking screenshot: 02-adding-task.png")
            add_task_input = page.get_by_placeholder("What needs to be done?")
            await move_mouse_and_update_cursor(page, add_task_input)
            await add_task_input.fill("Review documentation screenshots")
            input_area_locator = add_task_input.locator('xpath=../../..')
            await input_area_locator.screenshot(path=SCREENSHOTS_DIR / "02-adding-task.png")
            await add_task_input.press("Enter")
            await page.wait_for_timeout(500)

            # 3. Completed task screenshot (Partial)
            print("Taking screenshot: 03-completed-task.png")
            new_task_locator = page.locator('li:has-text("Review documentation screenshots")')
            checkbox_locator = new_task_locator.get_by_role("checkbox")
            await move_mouse_and_update_cursor(page, checkbox_locator)
            await checkbox_locator.check()
            await page.wait_for_timeout(200)
            await new_task_locator.screenshot(path=SCREENSHOTS_DIR / "03-completed-task.png")

            # 4. Deleting a task screenshot (Partial)
            print("Taking screenshot: 04-deleting-task.png")
            task_to_delete_locator = page.locator('li:has-text("Buy groceries")')
            delete_button = task_to_delete_locator.get_by_role("button")
            await move_mouse_and_update_cursor(page, delete_button)
            await page.wait_for_timeout(200)
            await task_to_delete_locator.screenshot(path=SCREENSHOTS_DIR / "04-deleting-task.png")

            print("Screenshots generated successfully!")

        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Please ensure the development server for the app is running at {APP_URL}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main()) 