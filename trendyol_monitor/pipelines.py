# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class TrendyolMonitorPipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('trendyol.db')
        self.c = self.conn.cursor()
        
        # Tablo oluşturma
        self.c.execute('''
                       CREATE TABLE IF NOT EXISTS products (
                       url TEXT PRIMARY KEY,
                       title TEXT,
                       price REAL,
                       stock_status BOOLEAN,
                       last_updated TEXT)
                       ''')
        self.conn.commit()


    def process_item(self, item, spider):
        # UPSERT
        try:
            self.c.execute('''
                            INSERT INTO products (url, title, price, stock_status, last_updated)
                            VALUES (?, ?, ?, ?, ?)
                            ON CONFLICT(url) DO UPDATE SET
                            price = excluded.price,
                            stock_status = excluded.stock_status,
                            last_updated = excluded.last_updated
                           ''',(
                               item['url'],
                               item['title'],
                               item['price'],
                               item['stock_status'],
                               item['last_updated']
                           ))
            self.conn.commit()
            '''
            url sütununu PRIMARY KEY yaparak benzersiz kıldık
            Botun her gün çalıştırıldığını varsayalım. Böylece aynı ürün veritabanında defalarca alt alta eklenmez.
            Ürün varsa sadece fiyatı ve tarihi güncellenir. Böylece veritabanı çöp dolmaz
            '''
        except Exception as e:
            print(f"Veritabanı Hatası: {e}")
        return item 
        '''
        birden fazla pipeline olsaydı, return item demezsek veri orada ölür ve bir sonraki pipeline'a geçmezdi.
        '''


    def close_spider(self, spider):
        self.conn.close()

