import pytest
import allure
from playwright.sync_api import Page, expect
from allure_commons.types import Severity, AttachmentType


@allure.suite("PriceFX Automation Dashboard")
@allure.label("owner", "Shreyas B.H")
@allure.severity(Severity.CRITICAL)
@allure.description("""
Test automates PriceFX dashboard with date range (2023-01 to 2026-03-31), 
customer CID-00038, and product MB-0060.
""")
def test_dashboard(page: Page):
    # Navigate - SPA optimized 
    with allure.step("Navigate to PriceFX Dashboard Login"):
        page.goto(
            "https://demo.pricefx.com/app/?partition=demofx_experis#/login?redirect_url=%2Fdashboards%2FAutomationDashboard",
            wait_until="domcontentloaded",
            timeout=30000
        )
        page.wait_for_timeout(2000)
        allure.attach(page.screenshot(), name="Login Page Loaded", attachment_type=AttachmentType.PNG)
        expect(page.locator('[data-test="username-input"]')).to_be_visible(timeout=20000)

    # Login
    with allure.step("Enter credentials and login"):
        page.locator('[data-test="username-input"]').fill("shreyas")
        page.locator('[data-test="password-input"]').fill("Shreyas@29409")
        page.locator('[data-test="login-loginbutton-button"]').click()
        page.wait_for_selector('[data-test="fromdate-input"], [data-test="todate-input"]', timeout=30000)
        page.wait_for_timeout(2000)
        allure.attach(page.screenshot(), name="Login Successful", attachment_type=AttachmentType.PNG)
        expect(page.locator('[data-test="fromdate-input"]')).to_be_visible(timeout=10000)

    # From Date
    with allure.step("Select From Date: 2023-01-01"):
        page.locator('[data-test="fromdate-input"]').click()
        page.wait_for_timeout(1500)
        expect(page.get_by_role("button", name="2020")).to_be_visible(timeout=8000)
        page.get_by_role("button", name="2020").click()
        expect(page.get_by_role("cell", name="2023")).to_be_visible(timeout=5000)
        page.get_by_role("cell", name="2023").click()
        expect(page.get_by_text("1", exact=True).first).to_be_visible(timeout=5000)
        page.get_by_text("1", exact=True).first.click()
        page.wait_for_timeout(1000)
        allure.attach(page.screenshot(), name="From Date Selected", attachment_type=AttachmentType.PNG)

    # To Date
    with allure.step("Select To Date: 2026-03-31"):
        page.locator('[data-test="todate-input"]').click()
        page.wait_for_timeout(1500)
        expect(page.get_by_role("button", name="2024")).to_be_visible(timeout=8000)
        page.get_by_role("button", name="2024").click()
        expect(page.get_by_text("2026", exact=True)).to_be_visible(timeout=5000)
        page.get_by_text("2026", exact=True).click()
        expect(page.get_by_role("button", name="Dec")).to_be_visible(timeout=5000)
        page.get_by_role("button", name="Dec").click()
        expect(page.get_by_text("Mar", exact=True)).to_be_visible(timeout=5000)
        page.get_by_text("Mar", exact=True).click()
        expect(page.get_by_role("table").get_by_text("31", exact=True)).to_be_visible(timeout=5000)
        page.get_by_role("table").get_by_text("31", exact=True).click()
        page.wait_for_timeout(1000)
        allure.attach(page.screenshot(), name="To Date Selected", attachment_type=AttachmentType.PNG)

    # Customer
    with allure.step("Select Customer: CID-00038"):
        page.get_by_text("CID-").click()
        page.wait_for_timeout(1000)
        customer_select = page.locator('[data-test="customer-select"]').get_by_role("combobox")
        expect(customer_select).to_be_visible(timeout=10000)
        customer_select.fill("CID-00038")
        page.wait_for_timeout(800)
        customer_select.press("Enter")
        page.wait_for_timeout(1500)
        allure.attach(page.screenshot(), name="Customer Selected", attachment_type=AttachmentType.PNG)

    # Product
    with allure.step("Select Product: MB-0060"):
        product_select = page.locator('[data-test="product-select"]').get_by_role("combobox")
        expect(product_select).to_be_visible(timeout=10000)
        product_select.fill("MB-0060")
        page.wait_for_timeout(800)
        expect(page.get_by_text("MB-").nth(1)).to_be_visible(timeout=8000)
        page.get_by_text("MB-").nth(1).click()
        page.wait_for_timeout(1500)
        allure.attach(page.screenshot(), name="Product Selected", attachment_type=AttachmentType.PNG)

    # Apply & Final steps
    with allure.step("Apply settings and validate dashboard"):
        apply_btn = page.locator('[data-test="unity-dashboard-apply-settings-button"]')
        expect(apply_btn).to_be_visible(timeout=10000)
        apply_btn.click()
        page.wait_for_timeout(4000)  # Dashboard processing

        expand_btn = page.locator('[data-test="common-expand-button"]')
        if expand_btn.count() > 0:
            expand_btn.first.click()
            page.wait_for_timeout(1000)

            close_btn = page.locator('[data-test="layout-header-modal-close"]')
            if close_btn.count() > 0:
                close_btn.click()
                page.wait_for_timeout(1000)

        expect(apply_btn).to_be_visible(timeout=8000)
        allure.attach(page.screenshot(), name="Test Complete", attachment_type=AttachmentType.PNG)
