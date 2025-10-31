from playwright.sync_api import Page, expect

from ..conftest import TEST_DATA_DIR


def test_upload_flow_nav_and_validation(live_server, page: Page):
    page.goto(live_server.url)
    expect(page.locator("nav")).to_contain_text("Text Shuffler")
    page.locator("nav a").first.click()
    page.wait_for_selector('input[name="text_file"]', timeout=5000)
    page.click('button[type="submit"]')
    expect(page.locator("input:invalid")).to_have_count(1)

    test_file = TEST_DATA_DIR / "text_file.txt"
    page.set_input_files('input[name="text_file"]', str(test_file))

    page.click('button[type="submit"]')
    expect(page.locator("pre#original")).to_be_visible()
    expect(page.locator("pre#shuffled")).to_be_visible()

    file_content = test_file.read_text()
    expect(page.locator("pre#original")).to_contain_text(file_content)
