from playwright.sync_api import sync_playwright
from ..utils.comparajogos import comparaJogosUrl

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )
    page = browser.new_page()
    page.goto(comparaJogosUrl)
    #
    # 
    # 0. Encontrar a seção de Populares da Semana
    title = page.locator("span", has_text="Populares da Semana") # Localiza o título de Populares da Semana
    section = title.locator("xpath=ancestor::div[contains(@class,'col-span')]").first # Localiza a div em que esse título se encontra
    #
    #
    # 1. Para cada jogo em Populares da Semana
    cards = section.locator("div.min-w-44.flex.flex-col.rounded-md.shadow-lg") # Localizando o card de jogo
    print("Contagem de cards: ", cards.count())
    for i in range(cards.count()):
        card = cards.nth(i)
        links = card.locator("a")
        print(links.nth(0).get_attribute("href"))
    #
    #
    # 1.1 Entre na página dele

    # 1.2 Extraia o nome dele 
    # 1.3 Para preço do jogo na listagem:
    # 1.3.1 Extraia o valor no cartão
    # 1.3.2 Extraia o valor no pix
    # 2. Armazenar valores em uma planilha ou json
    browser.close()
