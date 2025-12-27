from playwright.sync_api import Page, expect
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
        if self.buttons.count() > 3:
            viewMoreButton = self.offersSection.locator("button.cursor-pointer")
            viewMoreButton.click()
            time.sleep(2)
        return
    
    def get_store_name(offerCard):
        storeName = offerCard.locator("div[title]").first.get_attribute("title")
        print(storeName)
        return
    
    def get_credit_offer(offerCard):
        # Extrair o valor no cartão
        credit = offerCard.locator("div.pb-1.text-green-800")
        cardValue = credit.locator("div.inline-block.w-14").inner_text()
        installmentValue = credit.locator("small.ml-2.text-gray-500").inner_text()
        if installmentValue == "cartão": # Tratamento de dado caso não aceite dividir em parcelas
            installmentValue = f'1 x {cardValue}'
        print("Cartão:", cardValue, "  Parcela:", installmentValue)
        return 
    
    def get_pix_offer(offerCard):
        pixValue = "Não aceita" # Deixar vazio como padrão para lojas que não aceitam
        offers = offerCard.locator("div.text-green-800")
        credit = offerCard.locator("div.pb-1.text-green-800")
        if offers.count() > credit.count(): # Isso significa que tem a opção de pix
            pixLocator = offerCard.locator("small", has_text="pix")
            pixSection = pixLocator.locator("xpath=ancestor::div[contains(@class, 'text-green-800')]")
            pixValue = pixSection.locator("div.inline-block.w-14").inner_text()
        print("Pix: ", pixValue)
        return