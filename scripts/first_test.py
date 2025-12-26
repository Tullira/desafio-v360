from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False
    )
    page = browser.new_page()
    page.goto("https://www.comparajogos.com.br/")
    #
    # 
    # 1. Para cada jogo em Populares da Semana
    # 1.1 Extraia o nome dele
    # 1.2 Entre na página dele
    # 1.3 Para preço do jogo na listagem:
    # 1.3.1 Extraia o valor no cartão
    # 1.3.2 Extraia o valor no pix
    # 2. Armazenar valores em uma planilha ou json
    browser.close()
