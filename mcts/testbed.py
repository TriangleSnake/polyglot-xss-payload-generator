# testbed_async.py
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import quote_plus
from urls import TESTBED_URLS

async def evaluate(url: str, payload: str) -> bool:
    triggered = False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        async def on_dialog(dialog):
            nonlocal triggered
            triggered = True
            await dialog.dismiss()

        page.on("dialog", on_dialog)

        targets = [
            f"{url}?#{payload}",
            f"{url}?q={payload}&url={payload}",
            f"{url}/{payload}"
        ]

        for target in targets:
            try:
                await page.goto(target, timeout=1000)
            except Exception as e:
                print(f"[x] Timeout / Error at {target}: {e}")

    return triggered

async def testbed(payload: str) -> int:
    tasks = [evaluate(url, payload) for url in TESTBED_URLS]
    results = await asyncio.gather(*tasks)
    
    trigger_count = 0
    for url, triggered in results:
        if triggered:
            trigger_count += 1
            print(f"[v] Triggered XSS in {url} with payload: {payload}")
        else:
            print(f"[x] No trigger in {url}")

    return trigger_count

if __name__ == "__main__":
    polyglot = 'alert()'
    result = asyncio.run(testbed(polyglot))
    print("觸發 XSS context 數：", result)