from playwright.sync_api import sync_playwright
# from ..utils.comparajogos import comparaJogosUrl
from pages.view_game import GamePage
import time
comparaJogosUrl = "https://www.comparajogos.com.br"
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
        gamePage.check_view_more()
        #
        #
        # 1.3 Para cada preço do jogo na listagem:
        for j in range (gamePage.get_offers_cards().count()):
            offerCard = gamePage.get_offers_cards().nth(j)
            # 1.3.1 Extraia o nome da loja
            storeName = offerCard.locator("div[title]").first.get_attribute("title")
            print(storeName)
            offers = offerCard.locator("div.text-green-800")
            # 1.3.2 Extraia o valor no cartão
            credit = offerCard.locator("div.pb-1.text-green-800")
            cardValue = credit.locator("div.inline-block.w-14").inner_text()
            installmentValue = credit.locator("small.ml-2.text-gray-500").inner_text()
            if installmentValue == "cartão": # Tratamento de dado caso não aceite dividir em parcelas
                installmentValue = f'1 x {cardValue}'
            print("Cartão:", cardValue, "  Parcela:", installmentValue)
            # 1.3.3 Extraia o valor no pix
            pixValue = "Não aceita" # Deixar vazio como padrão para lojas que não aceitam
            if offers.count() > credit.count(): # Isso significa que tem a opção de pix
                pixLocator = offerCard.locator("small", has_text="pix")
                pixSection = pixLocator.locator("xpath=ancestor::div[contains(@class, 'text-green-800')]")
                pixValue = pixSection.locator("div.inline-block.w-14").inner_text()
            print("Pix: ", pixValue)
            print("---")
        print("================")
        # TODO: Fazer mesma coisa para jogos USADOS
        # 2. Armazenar valores em uma planilha ou json
        p.close()
    browser.close()
