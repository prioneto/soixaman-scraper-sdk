# Soixaman Scraper SDK

This project is a web scraper for Stoiximan's football matches using Flask and Selenium.

## Requirements

- Python 3.x
- Flask
- Selenium
- BeautifulSoup4

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/soixaman-scraper-sdk.git
   cd soixaman-scraper-sdk
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask server:

   ```sh
   python3 api/server.py
   ```

2. Visit the following URL in your browser to scrape the data:
   - For Premier League matches:
     ```
     https://127.0.0.1:5000/api/scrape?l=premier
     ```
   - For Greek Super League matches:
     ```
     https://127.0.0.1:5000/api/scrape?l=greek
     ```

## Endpoints

- `/api/scrape?l=premier`: Scrapes Premier League matches.
- `/api/scrape?l=greek`: Scrapes Greek Super League matches.

## Example

To scrape Premier League matches, visit:

```
https://127.0.0.1:5000/api/scrape?l=premier
```

To scrape Greek Super League matches, visit:

```
https://127.0.0.1:5000/api/scrape?l=greek
```

## License

This project is licensed under the MIT License.
