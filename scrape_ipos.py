import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {"User-Agent": "Mozilla/5.0"}
all_data = []

years = [2019, 2020, 2021, 2022, 2023]

for year in years:
    url = f"https://stockanalysis.com/ipos/{year}/"
    print(f"Scraping {year}...")
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table")
    if not table:
        print(f"  No table found for {year}")
        continue
    
    rows = table.find_all("tr")[1:]  # skip header
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 5:
            all_data.append({
                "ipo_date": cols[0].text.strip(),
                "ticker": cols[1].text.strip(),
                "company": cols[2].text.strip(),
                "ipo_price": cols[3].text.strip(),
                "return": cols[5].text.strip() if len(cols) > 5 else None
            })
    
    time.sleep(1)

df = pd.DataFrame(all_data)
print(f"\nTotal rows: {len(df)}")
print(df.head())
df.to_csv("dataraw/ipo_scraped.csv", index=False)
print("Saved to dataraw/ipo_scraped.csv")