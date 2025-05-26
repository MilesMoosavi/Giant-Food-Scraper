# Giant Food Web Scraper Project

This project demonstrates web scraping techniques for collecting product data from grocery store websites, specifically targeting Giant Food's product catalog.

## Important Notice

Due to anti-bot measures implemented by Giant Food's website, direct scraping returns 403 Forbidden errors. This is common for major retail websites that protect their data from automated access.

## Project Structure

```
Giant Food Scraper/
├── scraper/
│   ├── __init__.py
│   ├── main_scraper.py      # Main scraper with robust error handling
│   └── demo_scraper.py      # Demo with mock data showing expected functionality
├── data/                    # Output directory for scraped data
├── .venv/                   # Python virtual environment
├── .vscode/                 # VS Code configuration
│   ├── tasks.json
│   └── launch.json
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

### Main Scraper (`main_scraper.py`)
- Robust HTTP handling with retry logic and delays
- Enhanced browser headers to mimic real browser requests
- Multiple selector strategies to handle different HTML structures
- CSV output with product data (name, size, price, URL)
- Error handling for network issues and parsing problems
- Debug functionality saves HTML for analysis when scraping fails

### Demo Scraper (`demo_scraper.py`)
- Mock data generation showing expected scraper output
- Multiple output formats (CSV and JSON)
- Data analysis with price and brand statistics
- Educational example of scraper functionality

## Installation & Setup

1. **Activate Virtual Environment**
   ```bash
   .\.venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   .venv\Scripts\activate        # Windows Command Prompt
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run Demo Scraper (Recommended)
```bash
python -m scraper.demo_scraper
```

### Run Main Scraper (will encounter 403 errors)
```bash
python -m scraper.main_scraper
```

### VS Code Tasks
- Press `Ctrl+Shift+P` and search for "Tasks: Run Task"
- Select "Run Giant Food Scraper" or "Install Dependencies"

## Technical Approach

### Web Scraping Strategy
1. Session Management: Uses `requests.Session()` for persistent connections
2. Browser Mimicking: Comprehensive headers including:
   - User-Agent (Chrome 120)
   - Accept headers
   - Security headers (Sec-Fetch-*)
   - Cache control

3. Resilient Parsing: Multiple CSS selector strategies for:
   - Product containers
   - Product names
   - Sizes/units
   - Prices
   - Product URLs

4. Error Handling:
   - Network timeouts
   - HTTP error codes
   - Parsing failures
   - Missing elements

### Data Output
- CSV Format: Compatible with Excel and data analysis tools
- JSON Format: Structured data with metadata
- File Organization: All outputs saved to `data/` directory

## Dependencies

- `requests`: HTTP library for web requests
- `beautifulsoup4`: HTML parsing and navigation
- `lxml`: Fast XML and HTML parser
- Built-in modules: `csv`, `json`, `os`, `time`, `urllib.parse`

## Ethical Considerations

This project is for educational purposes and demonstrates:
- Respectful scraping practices (delays between requests)
- Error handling for blocked requests
- Alternative approaches when direct scraping fails

### Best Practices Implemented:
- Reasonable delays between requests
- Proper User-Agent headers
- Graceful handling of 403/403 errors
- Session reuse to minimize server load
- Limited request volume for testing

## Troubleshooting

### 403 Forbidden Errors
This is expected behavior for Giant Food's website. Consider:
- Using official APIs if available
- Contacting the website for data access permissions
- Using the demo scraper to understand expected functionality

### Missing Dependencies
```bash
pip install requests beautifulsoup4 lxml
```

### Virtual Environment Issues
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Development Notes

### VS Code Configuration
- Debugging: Configured Python debugger for `main_scraper.py`
- Tasks: Automated commands for running scraper and installing dependencies
- IntelliSense: Full Python support with virtual environment detection

### Future Enhancements
- [ ] API integration for official data access
- [ ] Database storage (SQLite/PostgreSQL)
- [ ] Product price tracking over time
- [ ] Category-specific scrapers
- [ ] Proxy rotation for large-scale scraping
- [ ] Selenium integration for JavaScript-heavy pages

## Legal and Compliance

This project is for educational purposes. Website Terms of Service and robots.txt should be reviewed before scraping. Production use requires proper permissions and rate limiting.

## Output Examples

### CSV Output
```csv
name,size,price,url,category,brand
Lay's Classic Potato Chips,10.5 oz,$3.99,https://giantfood.com/products/lays-classic,Potato Chips,Lay's
Pringles Original,5.5 oz,$2.49,https://giantfood.com/products/pringles-original,Potato Chips,Pringles
```

### JSON Output
```json
{
  "scrape_date": "2024-12-19T10:30:00",
  "total_products": 8,
  "source": "Demo Giant Food Scraper",
  "products": [
    {
      "name": "Lay's Classic Potato Chips",
      "size": "10.5 oz",
      "price": "$3.99",
      "url": "https://giantfood.com/products/lays-classic",
      "category": "Potato Chips",
      "brand": "Lay's"
    }
  ]
}
```
