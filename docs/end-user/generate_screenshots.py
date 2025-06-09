import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright, expect
from contextlib import asynccontextmanager

# ==============================================================================
# HELPERS/BOILERPLATE
# ==============================================================================

# --- Configuration ---
APP_URL = "http://localhost:5173"
SCREENSHOTS_DIR = Path(__file__).parent / "docs" / "assets" / "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# --- Reusable Browser Logic ---

@asynccontextmanager
async def managed_browser(app_url: str, headless: bool = True, viewport: dict = None):
    """A context manager to handle browser setup, teardown, and error handling."""
    if viewport is None:
        viewport = {"width": 1280, "height": 800}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        await page.set_viewport_size(viewport)
        
        try:
            print(f"Navigating to {app_url}...")
            await page.goto(app_url, wait_until="domcontentloaded")
            await page.get_by_test_id("main-heading").wait_for()
            print("App loaded successfully.")
            
            # Inject the fake cursor into the page
            await page.evaluate(JS_CREATE_CURSOR)
            
            yield page
            
            print("\nScenario finished successfully!")

        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print(f"Please ensure the development server for the app is running at {app_url}")
            
            # Dump DOM on failure for debugging
            dom_dump_path = Path("dom_on_failure.html")
            with open(dom_dump_path, "w", encoding="utf-8") as f:
                f.write(await page.content())
            print(f"DOM content saved to '{dom_dump_path}' for debugging.")
            raise e
        finally:
            await browser.close()
            print("Browser closed.")

# --- Reusable Screenshot and Cursor Logic ---

async def take_screenshot(page_or_locator, filename: str, description: str, **kwargs):
    """Logs, takes a screenshot, and verifies its existence."""
    path = SCREENSHOTS_DIR / filename
    print(f"  - Taking screenshot: {description} -> '{path.name}'")
    await page_or_locator.screenshot(path=path, **kwargs)
    assert path.exists(), f"Screenshot file not found: {path}"

async def move_mouse_to(page, locator):
    """Moves the mouse to the center of a locator and updates the fake cursor."""
    box = await locator.bounding_box()
    if box:
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2
        await page.mouse.move(x, y)
        await page.evaluate(JS_MOVE_CURSOR, [x, y])
        await page.wait_for_timeout(200) # Give cursor time to move

# JavaScript to create a fake cursor
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

# ==============================================================================
# SCREENSHOT SCENARIO
# ==============================================================================

async def generate_app_screenshots():
    """
    Runs through a sequence of user actions in the To-Do app 
    to generate screenshots for documentation.
    """
    async with managed_browser(APP_URL, headless=True) as page:
        print("\nStarting screenshot generation process...")

        # 1. Initial view
        await take_screenshot(
            page,
            "01-initial-view.png",
            "Initial full-page view"
        )

        # 2. Adding a task
        add_task_input = page.get_by_test_id("add-task-input").locator("input")
        await move_mouse_to(page, add_task_input)
        await add_task_input.fill("Review documentation screenshots")
        
        await take_screenshot(
            page.get_by_test_id("add-task-form"),
            "02-adding-task.png",
            "Entering a new task"
        )

        # 3. Completed task
        new_task_locator = page.get_by_test_id("task-list").locator("li").first
        checkbox_locator = new_task_locator.get_by_role("checkbox")
        await move_mouse_to(page, checkbox_locator)
        await checkbox_locator.check()
        await page.wait_for_timeout(200)
        
        await take_screenshot(
            new_task_locator,
            "03-completed-task.png",
            "Marking a task as complete"
        )

        # 4. Deleting a task
        task_to_delete_locator = page.get_by_test_id("task-item-1")
        delete_button = page.get_by_test_id("task-item-delete-button-1")
        await move_mouse_to(page, delete_button)
        await page.wait_for_timeout(200)

        await take_screenshot(
            task_to_delete_locator,
            "04-deleting-task.png",
            "Hovering to delete a task"
        )
        await delete_button.click()
        await page.wait_for_timeout(500)
    

async def main():
    await generate_app_screenshots()

if __name__ == "__main__":
    asyncio.run(main())