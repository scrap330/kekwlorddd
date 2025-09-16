import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import os

async def scrape_whentocop():
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i in range(1, 45):  # pages 1 à 44
            url = f"https://www.whentocop.fr/sneakers?page={i}"
            print(f"Scraping page {i} -> {url}")
            await page.goto(url, timeout=60000)

            sneaker_links = await page.locator(".sc-22e416f9-1 img").evaluate_all(
                "els => els.map(el => el.closest('a').href)"
            )

            for link in sneaker_links:
                try:
                    await page.goto(link, timeout=60000)
                    nom = await page.locator("h1").text_content()
                    indice = await page.locator("div.sc-7afd25b5-1:nth-of-type(1) p.cBQJCA").text_content()
                    prix = await page.locator("div.sc-7afd25b5-1:nth-of-type(2) p.cBQJCA").text_content()

                    data.append({
                        "nom": nom.strip() if nom else "",
                        "indice": indice.strip() if indice else "",
                        "prix": prix.strip() if prix else "",
                        "url": link
                    })
                except Exception as e:
                    print(f"Erreur sur {link} : {e}")

        await browser.close()

    # Chemin de sortie forcé
    output_path = r"C:\Users\abap0\Documents\Files\programmes\projet-scrap\sneakers.csv"
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("✅ Données sauvegardées dans :", output_path)

if __name__ == "__main__":
    asyncio.run(scrape_whentocop())
