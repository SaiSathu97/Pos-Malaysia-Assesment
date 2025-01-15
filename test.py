from playwright.sync_api import sync_playwright, TimeoutError

def test_rate_calculator():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the Rate Calculator page
        page.goto("https://www.pos.com.my/send/ratecalculator", wait_until="load")

        # Wait for the page to load completely
        page.wait_for_load_state("networkidle")

        try:
            # Log iframe information
            frames = page.frames
            print(f"Found {len(frames)} frames.")
            for idx, frame in enumerate(frames):
                print(f"Frame {idx}: {frame.url}")

            # Identify the correct iframe containing the dropdown
            for frame in frames:
                if "ratecalculator" in frame.url:
                    print("Switching to iframe:", frame.url)
                    target_frame = frame
                    break
            else:
                print("No relevant iframe found.")
                browser.close()
                return

            # Interact with the "sender_country" dropdown in the correct iframe
            target_frame.wait_for_selector("select#sender_country", timeout=20000)
            sender_country = target_frame.locator("select#sender_country")
            sender_country.scroll_into_view_if_needed()
            sender_country.select_option("MY")  # Select "Malaysia"
            print("Sender country selected successfully.")

            # Continue with the script
            target_frame.fill("input#sender_postcode", "35600")
            target_frame.wait_for_selector("select#receiver_country", timeout=20000)
            receiver_country = target_frame.locator("select#receiver_country")
            receiver_country.scroll_into_view_if_needed()
            receiver_country.select_option("IN")  # Select "India"
            print("Receiver country selected successfully.")

            # Weight and calculate
            target_frame.fill("input#weight", "1")
            target_frame.click("button:has-text('Calculate')")

            # Verify shipment options
            target_frame.wait_for_selector("div.rate-results", timeout=20000)
            print("Shipment options found.")
        except TimeoutError:
            print("Failed to find the required selector.")
            page.screenshot(path="error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    test_rate_calculator()
