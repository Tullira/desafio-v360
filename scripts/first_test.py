from playwright.sync_api import sync_playwright
from utils.comparajogos import comparaJogosUrl
from pages.view_game import GamePage


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
    title = page.locator("span", has_text="Populares da Semana") # Localiza o título de Populares da Semana
    section = title.locator("xpath=ancestor::div[contains(@class,'col-span')]").first # Localiza a div em que esse título se encontra
    # 1. Para cada jogo em Populares da Semana
    cards = section.locator("div.min-w-44.flex.flex-col.rounded-md.shadow-lg") # Localizando o card de jogo
    for i in range(cards.count()):
        card = cards.nth(i)
        link = card.locator("a")
        # 1.1 Extraia o nome dele 
        element = card.locator(".vertical-wrap")
        name = element.text_content().strip()
        print(name)
        # 1.2 Entre na página dele
        p = browser.new_page(base_url=comparaJogosUrl)
        url = link.get_attribute("href")
        if url is None:
            p.close()
        p.goto(url)
        #
        #
        gamePage = GamePage(p)
        gamePage.new_price_values()
        gamePage.used_price_values()
        print("================")
        p.close()
    browser.close()
