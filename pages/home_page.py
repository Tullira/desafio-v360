from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.popularTitle = page.locator("span", has_text="Populares da Semana") # Localiza o título de Populares da Semana
        self.popularSection = self.popularTitle.locator("xpath=ancestor::div[contains(@class,'col-span')]").first # Localiza a div em que esse título se encontra
        self.popularCards = self.popularSection.locator("div.min-w-44.flex.flex-col.rounded-md.shadow-lg") # Localiza os cards de jogos

    def get_game_name(self, card):
        element = card.locator(".vertical-wrap")
        name = element.text_content().strip()
        print(name)
        return name
    
    def get_cards(self):
        return self.popularCards

    def get_card_url(self, card):
        link = card.locator("a")
        url = link.get_attribute("href")
        return url