# scraper/main_scraper.py
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup

class GiantFoodScraper:
    def __init__(self):
        self.url = "https://giantfood.com/groceries/snacks/chips/potato-chips.html"
        self.data_dir = "data"
        self.products = []

    def fetch_page_source(self):
        """Uses Selenium to fetch the full HTML of a page after JavaScript has loaded."""
        print(f"Attempting to fetch LIVE data using Selenium from: {self.url}\n")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36")
        
        driver = None
        try:
            # Use Selenium's built-in driver management (Selenium 4.6.0+)
            # This automatically downloads the correct ChromeDriver version
            driver = webdriver.Chrome(service=ChromeService(), options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.get(self.url)
            
            print("Page loaded. Waiting 5 seconds for dynamic content...")
            time.sleep(5)
            
            print("Retrieving page source...")
            page_source = driver.page_source
            return page_source

        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
            print("Make sure Chrome browser is installed and accessible.")
            return None

        finally:
            if driver:
                driver.quit()

    def parse_products(self, page_source):
        """Parses the HTML source to extract product information."""
        soup = BeautifulSoup(page_source, 'html.parser')
        product_containers = soup.find_all('a', class_='pdl-static-category_product')

        if not product_containers:
            print("Could not find any product containers. The website's HTML structure may have changed or the block is very strong.")
            return        print(f"Found {len(product_containers)} products. Parsing now...")
        for product in product_containers:
            try:
                # Get the raw product name element
                name_element = product.find('h2', class_='pdl-static-category_product_name')
                
                # Clean up the product name
                if name_element:
                    # Extract and clean the product name
                    raw_name = name_element.text.strip()
                    
                    # Special handling for "Ahold Wedge Icon" products
                    if "Ahold Wedge Icon" in raw_name:
                        # Extract the actual product name (last non-empty line)
                        name_lines = [line.strip() for line in raw_name.split('\n') if line.strip()]
                        if name_lines:
                            name = name_lines[-1]  # Get the last non-empty line
                        else:
                            name = "Unknown Product"
                    else:
                        # For normal products, just use the text with basic cleanup
                        name = ' '.join(raw_name.split())  # Normalize whitespace
                else:
                    name = "Unknown Product"
                
                size = product.find('p', class_='pdl-static-category_product_unit').text.strip()
                # Placeholder for price/other details if they were to be added
                # price_element = product.find(...) 
                # price = price_element.text.strip() if price_element else "N/A"

                self.products.append({'name': name, 'size': size})
            except AttributeError:
                # This handles cases where a product card might be structured differently
                print("Skipping a product card due to missing name or size element.")
                continue
    
    def save_to_csv(self):
        """Saves the scraped product data to a CSV file."""
        if not self.products:
            print("No products to save.")
            return

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        filepath = os.path.join(self.data_dir, "live_giant_food_products.csv")
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.products)
        
        print(f"\nSuccessfully saved {len(self.products)} products to {filepath}")

    def run(self):
        """Main execution flow for the scraper."""
        try:
            html = self.fetch_page_source()
            if html:
                self.parse_products(html)
                self.save_to_csv()
        except Exception as e:
            print(f"A critical error occurred during the scraping process: {e}")
        
        print("\n✨ Live scraper run finished.")

def main():
    scraper = GiantFoodScraper()
    scraper.run()

if __name__ == "__main__":
    main()
