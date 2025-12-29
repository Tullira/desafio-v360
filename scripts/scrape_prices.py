from playwright.sync_api import sync_playwright
from utils.urls import comparaJogosUrl
from utils.cli_helpers import ask_running_option
from pages.game_page import GamePage
from pages.home_page import HomePage
import json

with sync_playwright() as p:
    runOption = ask_running_option()
    browser = p.chromium.launch(
        headless=runOption
    ) # Headed ou Headless dependendo da opção escolhida

    page = browser.new_page()
    page.goto(comparaJogosUrl)
    homePage = HomePage(page) # 0. Encontrar a seção de Populares da Semana
    games = []
    for i in range(homePage.get_cards().count()):
        card = homePage.get_cards().nth(i)
        url = homePage.get_card_url(card)
        gameName = homePage.get_game_name(card) # 1. Extraia o nome do jogo
        p = browser.new_page(base_url=comparaJogosUrl)
        if url is None:
            p.close()
        p.goto(url)  # 2. Visite a página do jogo
        
        gamePage = GamePage(p)
        newValues = gamePage.new_price_values() # 3. Extraia valores (pix e crédito) do jogo novo 
        usedValues = gamePage.used_price_values() # 4. Extraia valores (pix e crédito) do jogo usado
        gamePrices = {"game": gameName, "new_values": newValues, "used_values": usedValues}
        games.append(gamePrices)
        print("================")
        p.close()
    with open('reports/games.json', 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=4)
    browser.close()
