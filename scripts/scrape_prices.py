from playwright.sync_api import sync_playwright
from utils.comparajogos import comparaJogosUrl
from pages.game_page import GamePage
from pages.home_page import HomePage


with sync_playwright() as p:
    option = int(input("Qual tipo de execução você deseja?\n1 - Headed\n2 - Headless\n"))
    while (option != 1 and option != 2):
        print("Opção inválida")
        option = int(input("Qual tipo de execução você deseja?\n1 - Headed\n2 - Headless\n"))

    runOption = True
    if option == 1:
        runOption = False
    
    browser = p.chromium.launch(
        headless=runOption
    )
    page = browser.new_page()
    page.goto(comparaJogosUrl)
    #
    # 
    # 0. Encontrar a seção de Populares da Semana
    homePage = HomePage(page)
    for i in range(homePage.get_cards().count()):
        card = homePage.get_cards().nth(i)
        link = card.locator("a")
        # 1.1 Extraia o nome dele 
        homePage.get_game_name(card)
        # 1.2 Entre na página dele
        p = browser.new_page(base_url=comparaJogosUrl)
        url = link.get_attribute("href")
        if url is None:
            p.close()
        p.goto(url)
        #
        #
        gamePage = GamePage(p)
        # 1.3 Extraia valores de produtos novos
        gamePage.new_price_values()
        # 1.4 Extraia valores de produtos usados
        gamePage.used_price_values()
        print("================")
        p.close()
    browser.close()
