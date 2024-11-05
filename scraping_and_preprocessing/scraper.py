from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urljoin
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import os

# Setup
chrome_binary = "chrome-mac-arm64/Google Chrome for Testing.app"
options = webdriver.ChromeOptions()
options.binary_location = chrome_binary
driver = webdriver.Chrome(options=options)

def handle_popup(driver):
    try:
        # Wait for the popup to appear
        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.modal-content"))
        )
        # Find and click the close button (you may need to adjust the selector)
        close_button = popup.find_element(By.CSS_SELECTOR, "button.close-modal")
        close_button.click()
    except:
        # If no popup appears or we can't find the close button, just continue
        pass




def save_product_images(soup, product_name, base_url=None):
    # Create the 'images' folder if it doesn't exist
    images_folder = 'images'
    os.makedirs(images_folder, exist_ok=True)
    
    # Create a folder for the product images inside the 'images' folder
    product_folder_name = product_name.replace(' ', '_').replace('"', '').replace("'", "")
    product_folder_path = os.path.join(images_folder, product_folder_name)
    os.makedirs(product_folder_path, exist_ok=True)

    # Find all <picture> tags with the specified class
    images = soup.find_all('picture', class_='ImageItem_nextImageBox__28bbe')
    saved_images = []

    for i, picture_tag in enumerate(images):
        img_url = None

        # 1. Try to extract from <img> tag if present
        img_tag = picture_tag.find('img')
        if img_tag:
            # Prefer 'srcset' if available for higher resolutions
            if 'srcset' in img_tag.attrs:
                srcset = img_tag['srcset'].split(',')
                # Take the highest resolution image (last entry)
                img_url = srcset[-1].split()[0]
            elif 'src' in img_tag.attrs:
                img_url = img_tag['src']

        # 2. If no image URL yet, check the background-image in the <picture> style attribute
        if not img_url:
            style_attr = picture_tag.get('style', '')
            if 'background-image' in style_attr:
                # Extract the URL from background-image
                start = style_attr.find('url("') + len('url("')
                end = style_attr.find('")', start)
                img_url = style_attr[start:end]
        
        # 3. Check if the URL is an Edgio URL and needs parsing
        if img_url and img_url.startswith('/__edgio__/image'):
            parsed_url = urlparse(img_url)
            query_params = parse_qs(parsed_url.query)
            if 'url' in query_params:
                img_url = query_params['url'][0]

        # Handle relative URLs if the base URL is provided
        if base_url and img_url and img_url.startswith('/'):
            img_url = urljoin(base_url, img_url)

        # 4. Download and save the image
        if img_url:
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()  # Raise an exception for bad status codes
                # Save the image as image_{i+1}.jpg in the product folder
                img_filename = f"{product_folder_path}/image_{i+1}.jpg"
                with open(img_filename, 'wb') as f:
                    f.write(img_response.content)
                print(f"Saved image: {img_filename}")
                saved_images.append(img_filename)
            except requests.RequestException as e:
                print(f"Error downloading image {i+1}: {str(e)}")
        else:
            print(f"No valid image URL found for picture {i+1}.")
    
    return saved_images

# def extract_product_details(product_url):
#     driver.get(product_url)
#     time.sleep(2)  # Wait for page to load
    
#     # Handle popup
#     handle_popup(driver)
    
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
    
#     product = {}
    
#     # Extract product name
#     product['name'] = soup.find('h2', class_='ProductCard_title__WUhWA').text.strip()

#     product['images'] = save_product_images(soup, product['name'])
    
#     # Extract prices
#     price_box = soup.find('div', class_='Price_box__Yk31H')
#     if price_box:
#         current_price = price_box.find('div', class_='Price_currentPrice__ugez0')
#         original_price = price_box.find('div', class_='Price_standardPrice__SwHHc')
#         product['current_price'] = current_price.text.strip() if current_price else 'N/A'
#         product['original_price'] = original_price.text.strip() if original_price else 'N/A'
#     else:
#         product['current_price'] = 'N/A'
#         product['original_price'] = 'N/A'
    
#     # Extract rating and reviews
#     rating_container = soup.find('div', class_='bv_avgRating_component_container')
#     reviews_container = soup.find('div', class_='bv_numReviews_text')
#     product['rating'] = rating_container.text.strip() if rating_container else 'N/A'
#     product['num_reviews'] = reviews_container.text.strip().replace('(', '').replace(')', '') if reviews_container else 'N/A'
    
#     # Extract other details
#     specs_list = soup.find('ul', class_='Specs_list___uzDZ Specs_separator__v9Yn6')
#     if specs_list:
#         for item in specs_list.find_all('li', class_='Specs_listItem__TQ0PI'):
#             title = item.find('div', class_='Specs_title__exggr').text.strip().lower()
#             content = item.find('div', class_='Specs_text__ibZWh')
#             if content:
#                 product[title] = content.text.strip()
    
#     # Extract mattributes
#     mattributes = soup.find('div', class_='ProductCard_mattributes__jzsma')
#     if mattributes:
#         for item in mattributes.find_all('li', class_='Specs_listItem__TQ0PI'):
#             title = item.find('div', class_='Specs_title__exggr').text.strip()
#             content = item.find('div', class_='Specs_text__ibZWh')
#             product[title] = 'Yes' if content else 'No'
    
#     return product


# def extract_product_details(product_url):
#     driver.get(product_url)
#     time.sleep(5)  # Wait for page to load

#     # Handle popup
#     handle_popup(driver)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     product = {}

#     # Try extracting product name
#     try:
#         product['name'] = soup.find('h2', class_='ProductCard_title__WUhWA').text.strip()
#     except AttributeError:
#         print(f"Could not find product name for {product_url}")
#         product['name'] = 'N/A'

#     # Extract images
#     product['images'] = save_product_images(soup, product['name'])

#     # Extract prices
#     price_box = soup.find('div', class_='Price_box__Yk31H')
#     if price_box:
#         current_price = price_box.find('div', class_='Price_currentPrice__ugez0')
#         original_price = price_box.find('div', class_='Price_standardPrice__SwHHc')
#         product['current_price'] = current_price.text.strip() if current_price else 'N/A'
#         product['original_price'] = original_price.text.strip() if original_price else 'N/A'
#     else:
#         product['current_price'] = 'N/A'
#         product['original_price'] = 'N/A'

#     # Extract rating and reviews
#     rating_container = soup.find('div', class_='bv_avgRating_component_container')
#     reviews_container = soup.find('div', class_='bv_numReviews_text')
#     product['rating'] = rating_container.text.strip() if rating_container else 'N/A'
#     product['num_reviews'] = reviews_container.text.strip().replace('(', '').replace(')', '') if reviews_container else 'N/A'

#     # Extract other details
#     specs_list = soup.find('ul', class_='Specs_list___uzDZ Specs_separator__v9Yn6')
#     if specs_list:
#         for item in specs_list.find_all('li', class_='Specs_listItem__TQ0PI'):
#             title = item.find('div', class_='Specs_title__exggr').text.strip().lower()
#             content = item.find('div', class_='Specs_text__ibZWh')
#             if content:
#                 product[title] = content.text.strip()

#     # Extract mattributes
#     mattributes = soup.find('div', class_='ProductCard_mattributes__jzsma')
#     if mattributes:
#         for item in mattributes.find_all('li', class_='Specs_listItem__TQ0PI'):
#             title = item.find('div', class_='Specs_title__exggr').text.strip()
#             content = item.find('div', class_='Specs_text__ibZWh')
#             product[title] = 'Yes' if content else 'No'

#     return product



def extract_product_details(product_url,size):
    driver.get(product_url)
    time.sleep(5)  # Wait for page to load

    # Handle popup
    handle_popup(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product = {}

    # Try extracting product name from <h1> first, then fallback to <h2> if needed
    try:
        # Search for product name in <h1> tag first
        product_name = soup.find('h1', class_='ProductHeader_title__gx4zY')
        if product_name:
            product['name'] = product_name.text.strip()
        else:
            # Fallback to the <h2> tag if the <h1> is not found
            product['name'] = soup.find('h2', class_='ProductCard_title__WUhWA').text.strip()
    except AttributeError:
        print(f"Could not find product name for {product_url}")
        product['name'] = 'N/A'

    # Extract images
    product["size"]=size
    product['images'] = save_product_images(soup, product['name'])

    # Extract prices
    price_box = soup.find('div', class_='Price_box__Yk31H')
    if price_box:
        current_price = price_box.find('div', class_='Price_currentPrice__ugez0')
        original_price = price_box.find('div', class_='Price_standardPrice__SwHHc')
        product['current_price'] = current_price.text.strip() if current_price else 'N/A'
        product['original_price'] = original_price.text.strip() if original_price else 'N/A'
    else:
        product['current_price'] = 'N/A'
        product['original_price'] = 'N/A'

    # Extract rating and reviews
    rating_container = soup.find('div', class_='bv_avgRating_component_container')
    reviews_container = soup.find('div', class_='bv_numReviews_text')
    product['rating'] = rating_container.text.strip() if rating_container else 'N/A'
    product['num_reviews'] = reviews_container.text.strip().replace('(', '').replace(')', '') if reviews_container else 'N/A'

    # Extract other details
    specs_list = soup.find('ul', class_='Specs_list___uzDZ Specs_separator__v9Yn6')
    if specs_list:
        for item in specs_list.find_all('li', class_='Specs_listItem__TQ0PI'):
            title = item.find('div', class_='Specs_title__exggr').text.strip().lower()
            content = item.find('div', class_='Specs_text__ibZWh')
            if content:
                product[title] = content.text.strip()

    # Extract mattributes
    mattributes = soup.find('div', class_='ProductCard_mattributes__jzsma')
    if mattributes:
        for item in mattributes.find_all('li', class_='Specs_listItem__TQ0PI'):
            title = item.find('div', class_='Specs_title__exggr').text.strip()
            content = item.find('div', class_='Specs_text__ibZWh')
            product[title] = 'Yes' if content else 'No'

    return product





# def get_product_urls(category_url):
#     driver.get(category_url)
#     time.sleep(4)  # Wait for page to load
    
#     # Handle popup
#     handle_popup(driver)
    
#     product_urls = []
    
#     # Scroll to load all products
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     scroll_pause_time = 4
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height
    
#     # Find all product links
#     product_elements = driver.find_elements(By.CSS_SELECTOR, "div.productCard_cardImage__rux2L a")
    
#     for element in product_elements[:25]:  # Limit to 25 products
#         url = element.get_attribute('href')
#         if url:
#             product_urls.append(url)
    
#     return product_urls


# if __name__ == "__main__":
#     # List of category URLs (replace with actual URLs)
#     categories = [
#         "https://www.mattressfirm.com/mattresses/queen/",
        
#     ]

#     all_products = []

#     for category_url in categories:
#         try:
#             product_urls = get_product_urls(category_url)
            
#             for url in product_urls:
#                 try:
#                     product_details = extract_product_details(url)
#                     all_products.append(product_details)
#                     print(f"Scraped product: {product_details['name']}")
#                 except Exception as e:
#                     print(f"Error extracting details from {url}: {str(e)}")
#                     continue
#         except Exception as e:
#             print(f"Error processing category {category_url}: {str(e)}")
#             continue

#     # Create a DataFrame and save to CSV
#     df = pd.DataFrame(all_products)
#     df.to_csv('mattress_firm_products.csv', index=False)

#     print(f"Scraped {len(all_products)} products and saved to mattress_firm_products.csv")

#     # Close the browser
#     driver.quit()


def get_product_urls(category_url):
    driver.get(category_url)
    time.sleep(4)  # Wait for the page to load

    # Handle popup
    handle_popup(driver)

    # Click the "Show more" button to load more products (click only once)
    try:
        show_more_button = driver.find_element(By.CSS_SELECTOR, "button[data-qa-testid='show_more_button']")
        driver.execute_script("arguments[0].click();", show_more_button)
        time.sleep(5)  # Wait for the products to load after clicking the button
    except Exception as e:
        print("Error clicking 'Show more' button or no button available:", str(e))

    # Now gather all the product URLs
    product_urls = []
    product_elements = driver.find_elements(By.CSS_SELECTOR, "div.productCard_cardImage__rux2L a")

    for element in product_elements:  # Collect all product links
        url = element.get_attribute('href')
        if url:
            product_urls.append(url)

    return product_urls  # Return the full list of product URLs


def extract_size_from_url(url):
    """ Map product size based on the category URL. """
    url_size_mapping = {
        'king': 'King',
        'queen': 'Queen',
        'full': 'Full',
        'cal-king': 'California King',
        'twin': 'Twin',
        'twin-xl': 'Twin XL',
        'crib-toddler': 'Crib/Toddler',
    }

    for key, size in url_size_mapping.items():
        if key in url:
            return size
    return 'Unknown' 

if __name__ == "__main__":
    # List of category URLs (replace with actual URLs)
    categories = [
         "https://www.mattressfirm.com/mattresses/king/5637147600.c?page=9",
        "https://www.mattressfirm.com/mattresses/queen/5637147600.c?page=9",
        "https://www.mattressfirm.com/mattresses/full/5637147600.c?page=9",
        "https://www.mattressfirm.com/mattresses/cal-king/5637147600.c?page=9",
        "https://www.mattressfirm.com/mattresses/twin/5637147600.c?page=9",
        "https://www.mattressfirm.com/mattresses/twin-xl/5637147600.c?page=9",
        "https://www.mattressfirm.com/baby-kids/crib-toddler-mattresses/5637147583.c?page=9"
    ]


    all_products = []

    for category_url in categories:
        try:
            # product_urls = get_product_urls(category_url)
            product_urls = get_product_urls(category_url)  # Assuming this gets product URLs from the 
            product_size = extract_size_from_url(category_url)  
            
            for url in product_urls:
                try:
                    product_details = extract_product_details(url,product_size)
                    all_products.append(product_details)
                    print(f"Scraped product: {product_details['name']}")
                except Exception as e:
                    print(f"Error extracting details from {url}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error processing category {category_url}: {str(e)}")
            continue

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(all_products)
    df.to_csv('mattress_firm.csv', index=False)

    print(f"Scraped {len(all_products)} products and saved to mattress_firm_products.csv")

    # Close the browser
    driver.quit()
