from playwright.sync_api import Page
import time
class GamePage:

    def __init__(self, page: Page):
        self.page = page
        self.offersTitle = page.locator("span", has_text="Ofertas")
        self.offersSection = self.offersTitle.locator("xpath=ancestor::div[contains(@class,'py-5') and contains(@class,'scroll-mt-14')]").first
        self.offersCards = self.offersSection.locator("div.relative.rounded-lg.my-2.p-1.bg-sidebar-accent")
        self.buttons = self.offersSection.locator("button")
    
    def get_offers_cards(self):
        return self.offersCards

    def check_view_more(self):
        viewMoreButton = self.offersSection.locator("button.cursor-pointer")
        if viewMoreButton.is_visible():
            viewMoreButton.click()
            time.sleep(2)
        return
    
    def get_store_name(self, offerCard):
        storeName = offerCard.locator("div[title]").first.get_attribute("title")
        print(storeName)
        return storeName
    
    def get_credit_offer(self, offerCard):
        # Extrair o valor no cartão
        credit = offerCard.locator("div.pb-1.text-green-800")
        cardValue = credit.locator("div.inline-block.w-14").inner_text()
        installmentValue = credit.locator("small.ml-2.text-gray-500").inner_text()
        if installmentValue == "cartão": # Tratamento de dado caso não aceite dividir em parcelas
            installmentValue = f'1 x {cardValue}'
        print("Cartão:", cardValue, "  Parcela:", installmentValue)
        return (cardValue, installmentValue)
    
    def get_pix_offer(self, offerCard):
        pixValue = "Não aceita" # Deixar vazio como padrão para lojas que não aceitam
        offers = offerCard.locator("div.text-green-800")
        credit = offerCard.locator("div.pb-1.text-green-800")
        if offers.count() > credit.count(): # Isso significa que tem a opção de pix
            pixLocator = offerCard.locator("small", has_text="pix")
            pixSection = pixLocator.locator("xpath=ancestor::div[contains(@class, 'text-green-800')]")
            pixValue = pixSection.locator("div.inline-block.w-14").inner_text()
        print("Pix: ", pixValue)
        return pixValue

    def click_used_tab(self):
        usedTab = self.offersSection.locator("button[tabindex='-1']")
        usedTab.click()
        time.sleep(1)
        return
    
    def click_new_tab(self):
        newTab = self.offersSection.locator("button[tabindex='0']")
        newTab.click()
        time.sleep(1)
        return
    
    def scrape_prices(self):
        self.check_view_more()
        prices = []
        for j in range (self.get_offers_cards().count()):
            offerCard = self.get_offers_cards().nth(j)
            if offerCard.is_visible():
                name = self.get_store_name(offerCard) # Printa nome da loja 
                card, installment = self.get_credit_offer(offerCard) # Printa valor no crédito
                pix = self.get_pix_offer(offerCard) # Printa valor no pix
                priceObject = {name: {"card": card, "installment": installment, "pix": pix}}
                prices.append(priceObject)
        return prices
    
    def new_price_values(self):
        print("---Novos---")
        self.click_new_tab()
        prices = self.scrape_prices()
        return prices

    def used_price_values(self):
        print("---Usados---")
        self.click_used_tab()
        prices = self.scrape_prices()
        return prices