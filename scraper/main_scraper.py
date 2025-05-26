import requests
from bs4 import BeautifulSoup
import time
import csv
import os
from urllib.parse import urljoin

class GiantFoodScraper:
    def __init__(self):
        self.base_url = "https://giantfood.com"
        self.session = requests.Session()
        
        # Enhanced headers to better mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Create data directory if it doesn't exist
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_page(self, url, retries=3, delay=2):
        """Fetch a webpage with retry logic and delay"""
        for attempt in range(retries):
            try:
                print(f"Attempt {attempt + 1} - Fetching: {url}")
                
                # Add delay between requests to be respectful
                if attempt > 0:
                    time.sleep(delay * attempt)
                
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    print(f"403 Forbidden - Website may be blocking requests. Attempt {attempt + 1}/{retries}")
                    time.sleep(delay * 2)  # Longer delay for 403 errors
                else:
                    print(f"HTTP {response.status_code} - {response.reason}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed on attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
        
        return None    
    def parse_products(self, soup):
        """Parse product information from the soup object"""
        products = []
        
        # Try multiple possible selectors for product containers
        selectors = [
            'a.pdl-static-category_product',
            '.product-item',
            '.product-card',
            '[data-testid="product-card"]',
            '.grid-item'
        ]
        
        product_containers = []
        for selector in selectors:
            product_containers = soup.select(selector)
            if product_containers:
                print(f"Found {len(product_containers)} products using selector: {selector}")
                break
        
        if not product_containers:
            print("No product containers found. Searching for any links...")
            # Fallback: look for any links that might contain product info
            all_links = soup.find_all('a', href=True)
            print(f"Found {len(all_links)} total links on the page")
            return products
        
        for product in product_containers[:10]:  # Limit to first 10 for testing
            try:
                # Try multiple selectors for product name
                name_selectors = [
                    'h2.pdl-static-category_product_name',
                    '.product-name',
                    '.product-title',
                    'h2', 'h3', 'h4'
                ]
                
                name = "Name not found"
                for selector in name_selectors:
                    name_element = product.select_one(selector)
                    if name_element:
                        name = name_element.get_text().strip()
                        break
                
                # Try multiple selectors for size/unit
                size_selectors = [
                    'p.pdl-static-category_product_unit',
                    '.product-size',
                    '.product-unit',
                    '.size-info'
                ]
                
                size = "Size not found"
                for selector in size_selectors:
                    size_element = product.select_one(selector)
                    if size_element:
                        size = size_element.get_text().strip()
                        break
                
                # Try to get price information
                price_selectors = [
                    '.price',
                    '.product-price',
                    '.current-price',
                    '[data-testid="price"]'
                ]
                
                price = "Price not found"
                for selector in price_selectors:
                    price_element = product.select_one(selector)
                    if price_element:
                        price = price_element.get_text().strip()
                        break
                
                # Get product URL if available
                product_url = product.get('href', '')
                if product_url and not product_url.startswith('http'):
                    product_url = urljoin(self.base_url, product_url)
                
                product_data = {
                    'name': name,
                    'size': size,
                    'price': price,
                    'url': product_url
                }
                
                products.append(product_data)
                
            except Exception as e:
                print(f"Error parsing product: {e}")
                continue
        
        return products
    
    def save_to_csv(self, products, filename="giant_food_products.csv"):
        """Save products to CSV file"""
        if not products:
            print("No products to save")
            return
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'size', 'price', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for product in products:
                writer.writerow(product)
        
        print(f"Saved {len(products)} products to {filepath}")
    
    def scrape_category(self, category_url):
        """Scrape a specific category page"""
        print(f"Scraping category: {category_url}")
        
        response = self.get_page(category_url)
        if not response:
            print("Failed to fetch the webpage after multiple attempts")
            return []
        
        print(f"Successfully fetched page (Status: {response.status_code})")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug: Print page title and some basic info
        title = soup.find('title')
        if title:
            print(f"Page title: {title.get_text().strip()}")
        
        # Look for common page elements to understand structure
        print(f"Total page length: {len(response.content)} bytes")
        print(f"Total links found: {len(soup.find_all('a'))}")
        print(f"Total divs found: {len(soup.find_all('div'))}")
        
        products = self.parse_products(soup)
        
        if products:
            print(f"\nFound {len(products)} products:")
            for i, product in enumerate(products[:5], 1):
                print(f"{i}. {product['name']} - {product['size']} - {product['price']}")
            
            self.save_to_csv(products)
        else:
            print("No products found. The website structure may have changed.")
            # Save page content for debugging
            debug_file = os.path.join(self.data_dir, "debug_page.html")
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Saved page content to {debug_file} for debugging")
        
        return products

def main():
    scraper = GiantFoodScraper()
    
    # Test with the potato chips category
    potato_chips_url = "https://giantfood.com/groceries/snacks/chips/potato-chips.html"
    products = scraper.scrape_category(potato_chips_url)
    
    if not products:
        print("\nTrying alternative URLs...")
        # Try some alternative URLs that might work
        alternative_urls = [
            "https://giantfood.com/groceries/snacks/chips",
            "https://giantfood.com/groceries/snacks",
            "https://giantfood.com/groceries"
        ]
        
        for url in alternative_urls:
            print(f"\nTrying: {url}")
            products = scraper.scrape_category(url)
            if products:
                break

if __name__ == "__main__":
    main()
