import os
import random
import pandas as pd
from playwright.async_api import Playwright
# from python_ghost_cursor.playwright_sync import create_cursor
from python_ghost_cursor.playwright_async import create_cursor

_GT_START_PAGE = 'https://trends.google.com/trends?geo=&hl=en-US&tz=0'
_SEARCH_BAR_SELECTOR = 'label'

_LINE_PLOT_SELECTOR = '.fe-atoms-generic-content-container'
_DATE_SELECTION_SELECTOR = '#select_value_label_9'
_CUSTOM_DATE_RANGE_SELECTOR = 'div.custom-date-picker-select-container md-option:last-child'

_DOWNLOAD_BTN_SELECTOR = 'div.fe-line-chart-header-container button.widget-actions-item.export'

    # async def run(playwright: Playwright):
    # chromium = playwright.chromium # or "firefox" or "webkit".
    # browser = await chromium.launch()
    # page = await browser.new_page()
    # await page.goto("http://example.com")
    # # other actions...
    # await browser.close()
async def scrap_gt_page(playwright: Playwright, KEYWORD: str, START_DATE: str, END_DATE: str):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = await chromium.launch(channel="chrome", headless=False, args=['--start-maximized'])
    page = await browser.new_page(no_viewport=True)
    cursor = create_cursor(page)

    try:
        await page.goto(_GT_START_PAGE)
                
        # Wait for page load
        await page.wait_for_selector(_SEARCH_BAR_SELECTOR)
        print("0.0.", "GT Page loaded.")

        await cursor.click(_SEARCH_BAR_SELECTOR)

        # Insert query
        print("0.1.", "Typing keyword:", KEYWORD)
        await page.keyboard.type(KEYWORD, delay=random.randint(50, 1200))
        await page.keyboard.press("Enter")
        print("0.2.", "Search submitted.")

        # 0. Make sure the line plot is loaded before proceeding.
        # page.wait_for_selector("line-chart-directive")
        print("1.0.", "Waiting for line plot the complete drawing...")
        await page.wait_for_selector(_LINE_PLOT_SELECTOR, timeout=10_000)
        print("1.0.", "Line plot found.")
        
        print("1.0.", "Remove cookie banner")
        await page.wait_for_selector("a.cookieBarButton.cookieBarConsentButton", timeout=2_000)
        await cursor.click("a.cookieBarButton.cookieBarConsentButton")

        # 1. Change region
        # 1.1. Click region selector
        print("1.1.", "Waiting region selector")
        await page.wait_for_selector('div.hierarchy-select[role="button"]', timeout=5_000)
        await cursor.click('div.hierarchy-select[role="button"]')
        print("1.1.", "Clicked the region selector")

        # 1.2. Wait for dropdown
        print("1.2.", "Waiting for dropdown...")
        await page.wait_for_selector('li[role="button"][tabindex="0"]', timeout=5_000)
        await cursor.click('li[role="button"][tabindex="0"]')
        print('1.2.', 'Clicked "Worldwide".')

        # 2. Change Date
        # 2.1. Select custom date selector
        print("2.1.", "Finding date selector...")
        await cursor.click(_DATE_SELECTION_SELECTOR)
        print("2.1.", "Found date selector.")


        # 2.2 Wait for dropdown
        print("2.2.", 'Waiting for dropdown...')
        await page.wait_for_selector(_CUSTOM_DATE_RANGE_SELECTOR, timeout=5000)
        print("2.2.", 'Dropdown found. Clicking "Custom Date".')
        await cursor.click(_CUSTOM_DATE_RANGE_SELECTOR)
        print("2.2.", "Clicked Custom Date Selector.")


        # 2.3 Wait for pop-up
        print("2.3.", "Waiting for the custom-date-picker modal...")
        await page.wait_for_selector("div.md-datepicker-input-container", timeout=5000)
        print("2.3.", "Date picker modal found.")


        # 2.4 Update date range
        print("2.4.", "Changing start and end date...")
        print("2.4.", "DEBUG - START_DATE", START_DATE, type(START_DATE))
        print("2.4.", "DEBUG - END_DATE", END_DATE, type(END_DATE))
        # cursor.click("div.custom-date-picker-dialog-range-from input.md-datepicker-input")
        from_selector = page.locator('div.custom-date-picker-dialog-range-from input.md-datepicker-input')
        await from_selector.fill(START_DATE)
        # page.keyboard.press("Enter")

        # page.keyboard.press("Tab")
        # page.keyboard.press("Tab")
        # cursor.click("div.custom-date-picker-dialog-range-to input.md-datepicker-input")
        to_selector = page.locator('div.custom-date-picker-dialog-range-to input.md-datepicker-input')
        await to_selector.fill(END_DATE)

        print("2.4.", "Start and End dates changed.")

        # 2.5 Confirm date update
        print("2.5.", "Confirming custom date...")
        await cursor.click(".custom-date-picker-dialog-button.md-button.md-ink-ripple:last-child")

        # await page.pause()

        # 2.6 Wait for page load (again)
        await page.wait_for_selector(_LINE_PLOT_SELECTOR, timeout=5000)
        print("2.6.", "Confirmed the page is correctly loaded.")

        print('3.1.', 'Download RSV...')
        async with page.expect_download() as download_info:
            await page.wait_for_selector(_DOWNLOAD_BTN_SELECTOR)
            await cursor.click(_DOWNLOAD_BTN_SELECTOR)
                
        print("3.2.", 'RSV downloaded.')
        download = await download_info.value

        filename = os.getcwd() + "/temp/" + KEYWORD.replace("/", "_") + "_" + START_DATE + ".csv"
        await download.save_as(filename)

        print("3.3.", "RSV parsed as pandas dataframe.")
        df = pd.read_csv(filename, skiprows=3, names=['date', 'value'], parse_dates=['date'])
        df.to_csv(filename, index=True)

        if len(df) == 29:
            os.remove(filename)

        return df
    finally:
        await browser.close()


# scrap_gt_page('/g/11bytn80mf', '2023-04-04', '2023-05-02')