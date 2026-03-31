import allure
import pytest
from playwright.sync_api import sync_playwright, expect
from utils import get_test_data

# Load Excel Data
test_data = get_test_data("Code/testdata.xlsx")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("data", test_data)
def test_ddd(data):
    customer_id = data["CustomerId"]
    product_id = data["ProductId"]

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        def screenshot_step(name: str):
            allure.attach(
                page.screenshot(full_page=True),
                name=f"{name}_{customer_id}",
                attachment_type=allure.attachment_type.PNG
            )

        # Step 1: Navigate to login page
        with allure.step(f"Login and navigate for Customer: {customer_id}"):
            page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/login?redirect_url=%2Fqc%2Fquotes")

            page.locator("[data-test='username-input']").fill("shreyas")
            page.locator("[data-test='password-input']").fill("Shreyas@29409")
            page.locator("[data-test='login-loginbutton-button']").click()

            screenshot_step("Login completed")

        # Step 2: Navigate to dashboard
        with allure.step("Open Dashboard"):
            page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/qc/quotes")

            page.locator("[data-test='appheader-togglebutton']").click()
            page.get_by_role("link", name="Dashboards").click()

            page.locator(".ant-select-selector").click()
            page.get_by_text("AutomationDashboard").nth(2).click()

            screenshot_step("Dashboard opened")

        # Step 3: Set Dates
        with allure.step("Set date filters"):
            page.locator('[data-test="fromdate-input"]').click()
            page.get_by_role("button", name="2020").click()
            page.get_by_role("cell", name="2023").click()
            page.get_by_text("1", exact=True).first.click()

            page.locator('[data-test="todate-input"]').click()
            page.get_by_role("button", name="2024").click()
            page.get_by_text("2026", exact=True).click()
            page.get_by_role("button", name="Dec").click()
            page.get_by_text("Mar", exact=True).click()
            page.get_by_role("table").get_by_text("31", exact=True).click()

            screenshot_step("Dates selected")

        ## ✅ Step 4: Dynamic Customer Selection
        with allure.step(f"Select Customer: {customer_id}"):
            dropdown = page.locator("[data-test='customer-select']")
            dropdown.click()

            # Type value
            page.keyboard.type(customer_id, delay=100)

            # ✅ Wait ONLY for attachment (not visibility)
            page.wait_for_selector("div[role='option']", state="attached", timeout=10000)

            # ✅ Use keyboard to select (MOST reliable)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            screenshot_step("Customer selected")

        # ✅ Step 5: Dynamic Product Selection
        with allure.step(f"Select Product: {product_id}"):
            dropdown = page.locator("[data-test='product-select']")
            dropdown.click()

            # Type value
            page.keyboard.type(product_id, delay=100)

            # Wait for options to be attached (NOT visible)
            page.wait_for_selector("div[role='option']", state="attached", timeout=10000)

            # Use keyboard selection
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")

            screenshot_step("Product selected")

        # Step 6: Apply Filters
        with allure.step("Apply filters"):
            apply_button = page.locator("[data-test='unity-dashboard-apply-settings-button']")

            with page.expect_response(lambda r: "dashboard" in r.url and r.status == 200):
                apply_button.click()
                page.wait_for_timeout(10000)
        browser.close()

  ## Excel From local [Custometr ID Product ID sample 4] add the utils.py file to import location --important--
