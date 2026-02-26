import sys
import asyncio

from playwright.async_api import async_playwright

async def run_tests():
    errors = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # collect console errors
        page.on("console", lambda msg: errors.append((msg.type, msg.text)) if msg.type == 'error' else None)
        
        url = 'http://localhost:8080'
        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        # basic sanity: page has subject blocks (exam triggers)
        subjects = await page.query_selector_all('.exam-trigger')
        if not subjects:
            print('❌ No exam trigger buttons found')
            await browser.close()
            return False
        # click first exam to expand
        await subjects[0].click()
        await page.wait_for_timeout(500)  # allow sections to appear

        # click first section button if visible
        sections = await page.query_selector_all('#sections-list button')
        if sections:
            await sections[0].click()
            await page.wait_for_timeout(500)
        else:
            print('⚠️ no sections found for subject')

        # at this point we should either see a count modal or questions loaded
        # if modal appears, click start
        try:
            start_btn = await page.query_selector('button#start-quiz')
            if start_btn:
                await start_btn.click()
                await page.wait_for_timeout(500)
        except Exception:
            pass

        # pick a choice if quiz loaded
        choice = await page.query_selector('.choice')
        if choice:
            await choice.click()
            await page.wait_for_timeout(200)

        await browser.close()

    if errors:
        print('Console errors detected:')
        for etype, text in errors:
            print(f'  [{etype}] {text}')
        return False
    print('✅ UI test passed (no console errors)')
    return True

if __name__ == '__main__':
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
