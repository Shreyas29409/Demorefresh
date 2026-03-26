import pytest
from playwright.sync_api import Page, expect

def test_dashboard(page: Page):
    page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/login?redirect_url=%2Fdashboards%2FAutomationDashboard")

    page.locator('[data-test="username-input"]').fill("shreyas")
    page.locator('[data-test="password-input"]').fill("Shreyas@29409")
    page.locator('[data-test="login-loginbutton-button"]').click()

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

    page.get_by_text("CID-").click()
    page.locator('[data-test="customer-select"]').get_by_role("combobox").fill("CID-00038")
    page.locator('[data-test="customer-select"]').get_by_role("combobox").press("Enter")

    page.locator('[data-test="product-select"]').get_by_role("combobox").fill("MB-0060")
    page.get_by_text("MB-").nth(1).click()

    page.locator('[data-test="unity-dashboard-apply-settings-button"]').click()
    page.locator('[data-test="common-expand-button"]').click()
    page.locator('[data-test="layout-header-modal-close"]').click()

Dashboard Pass:
pytest Demo\test_dashboard.py -s -v --headed --browser-channel=chrome
