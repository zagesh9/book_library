import requests
from bs4 import BeautifulSoup
import logging
from django.db import transaction
from .models import Book
import re

class BookScraper:
    BASE_URL = 'http://books.toscrape.com/'

    @classmethod
    def get_all_categories(cls):
        """
        Scrape all available book categories from the website with their index
        """
        try:
            response = requests.get(cls.BASE_URL)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find categories in the side navigation
            category_links = soup.select('.side_categories ul li a')
            
            # Extract and clean category names with their corresponding index
            categories = [
                {
                    'name': link.text.strip(),
                    'index': cls._get_category_index(link['href'])
                } 
                for link in category_links 
                if link.text.strip() and link.text.strip() != 'Books'
            ]
            
            return categories
        
        except Exception as e:
            logging.error(f"Error scraping categories: {e}")
            return []

    @classmethod
    def _get_category_index(cls, href):
        """
        Extract category index from href
        """
        match = re.search(r'_(\d+)/', href)
        return int(match.group(1)) if match else None

    @classmethod
    def scrape_category(cls, category_info):
        """
        Scrape books for a specific category
        """
        try:
            # Sanitize category for URL
            sanitized_category = category_info['name'].lower().replace(' ', '-')
            
            # Construct category URL
            category_url = f'{cls.BASE_URL}catalogue/category/books/{sanitized_category}_{category_info["index"]}/index.html'
            print(f"Scraping URL: {category_url}")  # Debug print
            
            # Fetch category page
            response = requests.get(category_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find book elements
            book_elements = soup.select('.product_pod')
            print(f"Total book elements found: {len(book_elements)}")  # Debug print
            
            scraped_books = []
            
            # Process each book
            for book in book_elements:
                try:
                    # Extract book title
                    title_elem = book.select_one('h3 a')
                    title = title_elem['title'] if title_elem else 'Unknown Title'
                    
                    # Extract price
                    price_elem = book.select_one('.price_color')
                    price = float(price_elem.text.replace('£', '')) if price_elem else 0.00
                    
                    # Create or update book in database
                    with transaction.atomic():
                        book_obj, created = Book.objects.get_or_create(
                            title=title,
                            defaults={
                                'genre': category_info['name'],
                                'price': price,
                                'description': 'Scraped book'
                            }
                        )
                        
                        # Print whether book was created or already existed
                        # print(f"Book: {title}, Created: {created}")
                        
                        scraped_books.append(book_obj)
                
                except Exception as book_error:
                    print(f"Error processing individual book: {book_error}")
            
            return scraped_books
        
        except Exception as e:
            print(f"Error scraping category {category_info['name']}: {e}")
            return []