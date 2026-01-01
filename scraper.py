import asyncio import aiohttp from bs4 import BeautifulSoup import pandas as pd

BASE_URL = "https://ambient-website.com/leads?page=" TOTAL_PAGES = 936

async def fetch_page(session, page_num): url = f"{BASE_URL}{page_num}" async with session.get(url) as response: if response.status == 200: html = await response.text() return parse_page(html) return []

def parse_page(html): soup = BeautifulSoup(html, 'html.parser') contacts = [] # Assuming standard lead list structure items = soup.find_all('div', class_='contact-card') for item in items: name = item.find('h2').text.strip() title = item.find('p', class_='job-title').text.strip() contacts.append({'Name': name, 'Title': title}) return contacts

async def main(): async with aiohttp.ClientSession() as session: tasks = [] for i in range(1, TOTAL_PAGES + 1): tasks.append(fetch_page(session, i))

    results = await asyncio.gather(*tasks)
    # Flatten list of lists
    flat_results = [item for sublist in results for item in sublist]
    
    df = pd.DataFrame(flat_results)
    df.to_csv('extracted_contacts.csv', index=False)
    print(f"Successfully extracted {len(df)} contacts.")


if name == "main": asyncio.run(main())