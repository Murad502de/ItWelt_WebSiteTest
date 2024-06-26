from base.WebdriverSetup import get_firefox_driver
from actions.ScreenshotHelpers import ScreenshotActions
import os
import pytest


@pytest.mark.parametrize("width,height", [
    (1920, 1080),
    (1366, 768),
    (768, 1024),
    (375, 667),
])
def test_screenshot(width, height):
    url = "https://your-landing-page-url.com"
    baseline_screenshot = f"baseline/{width}x{height}.png"
    current_screenshot = f"current/{width}x{height}.png"

    driver = get_firefox_driver()
    actions = ScreenshotActions(driver)

    try:
        actions.take_screenshot_with_size(url, width, height, current_screenshot)

        if os.path.exists(baseline_screenshot):
            score, imageA, imageB, diff = actions.compare_images(baseline_screenshot, current_screenshot)
            assert score > 0.95, f"Images are too different: SSIM={score}"
        else:
            print(f"Baseline image not found for resolution {width}x{height}. Saving current screenshot as baseline.")
            os.makedirs(os.path.dirname(baseline_screenshot), exist_ok=True)
            os.rename(current_screenshot, baseline_screenshot)
    finally:
        driver.quit()
