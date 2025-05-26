"""
Demo scraper with mock data to demonstrate the Giant Food scraper functionality.

This demonstrates how the scraper would work if the Giant Food website allowed scraping.
It creates sample data that matches the expected structure and saves it to CSV.
"""

import csv
import os
import json
from datetime import datetime

class DemoGiantFoodScraper:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def generate_mock_products(self):
        """Generate realistic mock product data that would come from Giant Food"""
        mock_products = [
            {
                'name': 'Lay\'s Classic Potato Chips',
                'size': '10.5 oz',
                'price': '$3.99',
                'url': 'https://giantfood.com/products/lays-classic-potato-chips',
                'category': 'Potato Chips',
                'brand': 'Lay\'s'
            },
            {
                'name': 'Pringles Original',
                'size': '5.5 oz',
                'price': '$2.49',
                'url': 'https://giantfood.com/products/pringles-original',
                'category': 'Potato Chips',
                'brand': 'Pringles'
            },
            {
                'name': 'Kettle Brand Sea Salt Potato Chips',
                'size': '8.5 oz',
                'price': '$4.79',
                'url': 'https://giantfood.com/products/kettle-brand-sea-salt',
                'category': 'Potato Chips',
                'brand': 'Kettle Brand'
            },
            {
                'name': 'Ruffles Original',
                'size': '8.5 oz',
                'price': '$3.69',
                'url': 'https://giantfood.com/products/ruffles-original',
                'category': 'Potato Chips',
                'brand': 'Ruffles'
            },
            {
                'name': 'Cape Cod Original Kettle Cooked Chips',
                'size': '8 oz',
                'price': '$4.29',
                'url': 'https://giantfood.com/products/cape-cod-original',
                'category': 'Potato Chips',
                'brand': 'Cape Cod'
            },
            {
                'name': 'Utz Original Potato Chips',
                'size': '9.5 oz',
                'price': '$3.89',
                'url': 'https://giantfood.com/products/utz-original',
                'category': 'Potato Chips',
                'brand': 'Utz'
            },
            {
                'name': 'Wise Original Potato Chips',
                'size': '9 oz',
                'price': '$3.59',
                'url': 'https://giantfood.com/products/wise-original',
                'category': 'Potato Chips',
                'brand': 'Wise'
            },
            {
                'name': 'Terra Original Vegetable Chips',
                'size': '6.8 oz',
                'price': '$5.49',
                'url': 'https://giantfood.com/products/terra-vegetable-chips',
                'category': 'Vegetable Chips',
                'brand': 'Terra'
            }
        ]
        
        return mock_products
    
    def save_to_csv(self, products, filename="demo_giant_food_products.csv"):
        """Save products to CSV file"""
        if not products:
            print("No products to save")
            return
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'size', 'price', 'url', 'category', 'brand']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for product in products:
                writer.writerow(product)
        
        print(f"Saved {len(products)} products to {filepath}")
        return filepath
    
    def save_to_json(self, products, filename="demo_giant_food_products.json"):
        """Save products to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        
        output_data = {
            'scrape_date': datetime.now().isoformat(),
            'total_products': len(products),
            'source': 'Demo Giant Food Scraper',
            'products': products
        }
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(output_data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(products)} products to {filepath}")
        return filepath
    
    def run_demo(self):
        """Run the demo scraper"""
        print("🛒 Giant Food Demo Scraper")
        print("=" * 50)
        print("This demo shows how the scraper would work with real data.")
        print("Due to anti-bot measures, we're using mock data that represents")
        print("the structure and content you'd get from the actual website.\n")
        
        # Generate mock data
        products = self.generate_mock_products()
        
        print(f"Generated {len(products)} sample products:")
        print("-" * 50)
        
        for i, product in enumerate(products, 1):
            print(f"{i:2d}. {product['name']}")
            print(f"    Size: {product['size']} | Price: {product['price']} | Brand: {product['brand']}")
            print(f"    URL: {product['url']}")
            print()
        
        # Save to both CSV and JSON formats
        csv_file = self.save_to_csv(products)
        json_file = self.save_to_json(products)
        
        print("\n📊 Data Analysis:")
        print("-" * 20)
        
        # Basic analysis
        brands = {}
        sizes = []
        prices = []
        
        for product in products:
            brand = product['brand']
            brands[brand] = brands.get(brand, 0) + 1
            
            # Extract numeric price for analysis
            try:
                price = float(product['price'].replace('$', ''))
                prices.append(price)
            except:
                pass
        
        print(f"Unique brands: {len(brands)}")
        print(f"Brand breakdown: {dict(brands)}")
        
        if prices:
            print(f"Price range: ${min(prices):.2f} - ${max(prices):.2f}")
            print(f"Average price: ${sum(prices)/len(prices):.2f}")
        
        print(f"\n💾 Files created:")
        print(f"  • CSV: {csv_file}")
        print(f"  • JSON: {json_file}")
        
        return products

def main():
    demo_scraper = DemoGiantFoodScraper()
    products = demo_scraper.run_demo()
    
    print("\n✨ Demo completed successfully!")
    print("The files in the 'data' directory show the expected output format")
    print("for when the scraper can successfully access the Giant Food website.")

if __name__ == "__main__":
    main()
