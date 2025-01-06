from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)


def scrape_matches():
    # Explicitly set the path to chromedriver
    chrome_driver_path = "/usr/bin/chromedriver"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Specify the service for chromedriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL of the target page
    url = 'https://www.stoiximan.gr/sport/podosfairo/ellada/stoiximan-super-league/1636/'
    driver.get(url)

    # Close any modal if it exists
    try:
        close_button = driver.find_element(
            By.CLASS_NAME, 'sb-modal__close__btn')
        close_button.click()
    except:
        print('Close button not found or already closed.')

    # Initialize a set to track unique matches
    unique_matches = set()
    results = []

    # Smooth scrolling to the bottom of the page
    scroll_pause_time = 0.5
    scroll_increment = 300

    print("Starting smooth scroll...")
    while True:
        driver.execute_script(
            "window.scrollBy(0, arguments[0]);", scroll_increment)
        time.sleep(scroll_pause_time)

        # Get the fully loaded HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Find all matches in the rendered HTML
        matches = soup.find_all(
            'div', class_='vue-recycle-scroller__item-view')

        if not matches:
            print("No matches found.")
            break

        for match in matches:
            match_link = match.find('a', {'data-testid': True})
            if match_link:
                match_href = match_link.get('href')
                if match_href and match_href not in unique_matches:
                    unique_matches.add(match_href)

                    data_testid = match_link.get('data-testid')
                    if data_testid:
                        teams = data_testid.split(' - ')
                        if len(teams) == 2:
                            team1, team2 = teams
                            team1_src = match.find_all('img')[0].get('src')
                            team2_src = match.find_all('img')[1].get('src')

                    date_time_elements = match.find_all(
                        'span', class_='tw-m-0')
                    match_date = date_time_elements[0].get_text(
                        strip=True) if len(date_time_elements) > 0 else 'N/A'
                    match_time = date_time_elements[1].get_text(
                        strip=True) if len(date_time_elements) > 1 else 'N/A'

                    odds_elements = match.find_all(
                        'div', class_='selections__selection selection-horizontal-button tw-flex tw-flex-row tw-items-center tw-justify-center tw-h-[36px] tw-flex-1 tw-cursor-pointer tw-py-[10px] tw-px-n tw-rounded-s tw-border-n tw-border-solid dark:tw-bg-n-22-licorice dark:tw-border-n-28-cloud-burst tw-bg-n-97-porcelain tw-border-n-90-dark-snow dark:tw-text-white-snow tw-text-n-13-steel tw-relative tw-overflow-hidden tw-outline-none tw-select-none tw-break-words tw-text-center selections__selection--columns-4 hover:tw-bg-n-94-dirty-snow hover:tw-border-n-silver-mist dark:hover:tw-border-n-36-east-bay dark:hover:tw-bg-n-28-cloud-burst tw-mr-n last:tw-mr-0'
                    )
                    odds = []
                    for odd in odds_elements:
                        label = odd.get('aria-label')
                        if label:
                            odds_value = label.split(
                                'with odds')[-1].strip('.')
                            odds.append(odds_value)

                    results.append({
                        "team1": team1,
                        "team2": team2,
                        "team1_src": team1_src,
                        "team2_src": team2_src,
                        "date": match_date,
                        "time": match_time,
                        "odds": odds
                    })

        scroll_height = driver.execute_script(
            "return document.body.scrollHeight")
        current_scroll_position = driver.execute_script(
            "return window.scrollY + window.innerHeight")
        if current_scroll_position >= scroll_height - 1:
            print("Reached the bottom of the page.")
            break

    driver.quit()
    return results


@app.route('/api/scrape', methods=['GET'])
def scrape_endpoint():
    try:
        matches = scrape_matches()
        return jsonify({"status": "success", "data": matches}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Default to 5000 if PORT is not set
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
