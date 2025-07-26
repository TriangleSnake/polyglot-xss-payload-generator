from playwright.sync_api import sync_playwright, Page, Dialog
def evaluate(url: str, payload: str) -> bool:
    """
    Payload Example: https://xss.trianglesnake.com/
    """
    
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    triggered = False
    
    def is_triggered(dialog: Dialog):
        nonlocal triggered
        triggered = True
        dialog.dismiss()

    page.on("dialog", is_triggered)
    
    
    page.goto(f"{url}?q={payload}&url={payload}")
    page.goto(f"{url}/{payload}")
    page.goto(f"{url}#{payload}")
    
    return triggered

foo = evaluate("https://public-firing-range.appspot.com/address/location.hash/eval", "alert()")
print(foo)