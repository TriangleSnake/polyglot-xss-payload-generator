# testbed.py
import asyncio
from playwright.async_api import async_playwright,Dialog
from urllib.parse import quote_plus
from urls import TESTBED_URLS

async def evaluate(url: str, payload: str) -> bool:
    if "alert()" not in payload:
        return False
    triggered = False
    
    #print(f"Testing {url} with payload: {payload}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        async def on_dialog(dialog:Dialog):
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
                pass
                #print(f"[x] Timeout / Error at {target}: {e}")
    if triggered:
        print(f"[v] Triggered XSS")
    return triggered

async def testbed(payload: str) -> int:
    trigger_count = 0
    tasks = [evaluate(url, payload) for url in TESTBED_URLS]
    batch_size = 20
    results = []
    for i in range(len(TESTBED_URLS)//batch_size):
        results += await asyncio.gather(*tasks[i*batch_size:(i+1)*batch_size])
    trigger_count = sum(results)
    
    return trigger_count

if __name__ == "__main__":
    polyglot = 'alert()'
    result = asyncio.run(testbed(polyglot))
    print("觸發 XSS context 數：", result)