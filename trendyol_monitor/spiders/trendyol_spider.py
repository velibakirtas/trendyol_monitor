import scrapy
import json 
import re
from trendyol_monitor.items import TrendyolMonitorItem
from datetime import datetime


class TrendyolSpider(scrapy.Spider):
    # HİBRİT MİMARİ
    name = "trendyol_spider"
    allowed_domains = ["www.trendyol.com"]
    start_urls = ["https://www.trendyol.com/sr?q=gaming%20laptop&qt=gaming%20laptop&st=gaming%20laptop&os=1"]

    def start_requests(self):
        for url in self.start_urls:
            # ---- Aşama 1: Playwright -----
            yield scrapy.Request(
                url=url,
                meta = {
                    'playwright': True,
                    'playwright_include_page':True, # Burayı kullanmazsak playwright sayfayı açar, HTML'i indirir ve tarayıcıyı hemen kapatır. parse_list fonksiyonuna geldiğimizde elimizde kaydırabileceğimiz bir sayfa kalmaz.
                },
                callback=self.parse_list
            )
             
    async def parse_list(self,response):
        # -------- Aşama 2: Kaydırma ---------
        page = response.meta['playwright_page']

        print("Sayfa Kaydırılıyor...")

        for _ in range(5):
            await page.evaluate("window.scrollBy(0,1000)")
            await page.wait_for_timeout(2000)

        content = await page.content()

        from scrapy.selector import Selector
        selector = Selector(text=content) # render edilmiş içerikten çekileceği için content değişkenini gönderdik

        product_links = selector.css("a[data-testid='product-card']::attr(href)").getall()
        print(f"Bulunan ürün sayısı: {len(product_links)}")

        for link in product_links:
            full_url = response.urljoin(link)

            # ---- Aşama 3: Standart Request -------
            # Detay sayfasına Playwright ile gitmiyoruz.
            yield scrapy.Request(full_url, callback=self.parse_detail)

        await page.close()

    def parse_detail(self, response):
        # ----- Aşama 4: JSON Parsing ------
        target_variable = "__envoy__PROPS"
        script_content = response.xpath(f"//script[contains(text(),'{target_variable}')]/text()").get()


        if script_content:
            pattern = r'window\s*\[\s*["\']' + re.escape(target_variable) + r'["\']\s*\]\s*=\s*(\{.+)'
            match = re.search(pattern, script_content, re.DOTALL)
            if match:
                json_str = match.group(1)
                json_str = json_str.strip()
                if json_str.endswith(';'):
                    json_str = json_str[:-1]

                try:
                    data = json.loads(json_str)
                    p_data = data.get('product', {})

                    # Güvenli Zincirleme (biri eksikse hata vermez None döner)
                    merchant_listing = p_data.get('merchantListing') or {}
                    winner_variant = merchant_listing.get('winnerVariant') or {}
                    price_info = winner_variant.get('price') or {}
                    selling_price = price_info.get('sellingPrice') or {}

                    # Item Oluşturma
                    item = TrendyolMonitorItem()
                    item['url'] = response.url
                    item['title'] = p_data.get('name')
                    item['price'] = selling_price.get('value')
                    item['stock_status'] = p_data.get('stockStatus', False) # varsayılan False
                    item['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                    print(f"Veri Çekildi: {item['title'][:30]}... {item['price']} TL")
                    yield item
                except json.JSONDecodeError:
                    print("❌ Hata: JSON ayrıştırılamadı.")
            else:
                self.logger.warning("Regex deseni eşleşmedi. Script yapısı farklı olabilir.")
        else:
            self.logger.warning("Sayfada bu değişkeni içeren script bulunamadı.")

        



                
                
        #         # Dosyaya kaydediyoruz
        #             with open('trendyol_dump.json', 'w', encoding='utf-8') as f:
        #                 json.dump(data, f, ensure_ascii=False, indent=4)
                    
        #             print("\n✅ BAŞARILI! 'trendyol_dump.json' dosyası oluşturuldu.")
        #             print("Şimdi bu dosyayı açıp Fiyat ve İsim bilgisinin yolunu bulabilirsin.")
                
        #         except json.JSONDecodeError:
        #             print("❌ Hata: JSON ayrıştırılamadı.")
        #             with open('bozuk_veri.txt', 'w', encoding='utf-8') as f:
        #                 f.write(json_str)
        #             print("Bozuk veri 'bozuk_veri.txt' dosyasına kaydedildi, incele.")
        #     else:
        #         print("❌ Hata: Regex deseni eşleşmedi. Script yapısı farklı olabilir.")
        #         with open('raw_script.txt', 'w', encoding='utf-8') as f:
        #             f.write(script_content)
        #         print("Ham script 'raw_script.txt' dosyasına kaydedildi.")
        # else:
        #     print("❌ Hata: Sayfada bu değişkeni içeren script bulunamadı.")

