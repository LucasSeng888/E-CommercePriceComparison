# config.py

# 在这里填写你的 OpenAI API Key（如果没有可以留空，AI总结功能将跳过）
GEMINI_API_KEY = "AIzaSyCY1W7WWGzP_FdOgtIkb5rR9tTKyiAxUfA"

# 你要监控的商品列表。请确保不同平台的链接指向的是同一款商品。
# 注意：为了演示，这里选取了比较容易抓取的 Amazon 和另外两个假设的结构。
# 实际的 Shopee/Lazada 链接极易触发反爬，如果抓取失败，需要不断更新选择器。

PRODUCTS_TO_TRACK = [
    {
        "platform": "Amazon",
        # 示例链接：一个具体的鼠标
        "url": "https://www.amazon.com/Razer-Viper-Wireless-Esports-Gaming/dp/B0CW25XR5R/ref=sr_1_1?crid=VPA2W3SR644P&dib=eyJ2IjoiMSJ9.DfP8lRxLgzx9m9odUjrZnk3fod87QoaPYLVL92b59P6px6J_37JuBtmZlosgnw3Nb3ltrQd8kYnun-Qgl2se2j-kSbavgoJK4iPSfFVakOFHsSR8XqFnbMqvvvpyPFUun9hvqNmZFktAnmf6CJXIsZgCuJQ7k2q_jmxmvMhBF_M_LQo5EysYzwhVAf1WeEE_zA8h23WUFCxCtgww2QlCp7NhW2RI9w8_kwO2wI5KweE.gXlGZY4abhh0LnCevMfT9YWKM3Y2EsqVhzPiGOj13jQ&dib_tag=se&keywords=razer&qid=1764923596&sprefix=raze%2Caps%2C972&sr=8-1",
        # 不同平台的HTML结构不一样，需要指定价格和标题的CSS选择器
        "selectors": {
            "price": '.a-price .a-offscreen', # Amazon常见的价格隐藏元素
            "title": '#productTitle'
        },
        "currency_symbol": "RM"
    },
    #   {
    #     "platform": "Shopee (Demo Link)",
    #     # Use the latest URL you provided
    #     "url": "https://shopee.com.my/Razer-Viper-V3-Pro-Wireless-Esports-Gaming-Mouse-54g-Lightweight-35-000-DPI-Optical-Sensor-with-Advanced-Features-i.1529361917.43123715773?extraParams=%7B%22display_model_id%22%3A238160287849%2C%22model_selection_logic%22%3A3%7D&sp_atk=c22fd491-9992-483b-92e7-554ab3af3bd5&xptdk=c22fd491-9992-483b-92e7-554ab3af3bd5",
    #     "selectors": {
    #         # Shopee Price: Use more precise XPath finding parent section with aria-live="polite"
    #         "price": "xpath=//section[@aria-live='polite']//div[contains(text(), 'RM') or contains(text(), 'S$')]", 
            
    #         # Shopee Title: Use h1 tag
    #         "title": 'h1' 
    #     },
    #     "currency_symbol": "RM"
    # },
    # {
    #    "platform": "eBay",
    #     # Updated to the actual Malaysian URL
    #     "url": "https://www.ebay.com.my/itm/286904178553?_skw=Razer+Viper+V3+Pro+Wireless+Esports+Gaming+Mouse&itmmeta=01KBQE6AXJQTSMKK3DB6465151&hash=item42ccd25779:g:OLYAAeSwwmFpG7SE&itmprp=enc%3AAQAKAAABEFkggFvd1GGDu0w3yXCmi1eD2kUvRsdJLQ0mkHNtI8YU7%2FTHysJeoxHEygoUoOotoayntetUbVvbupkNglGfaOnRGG5zYK2%2FwJEvdWOn4%2B2d%2BHlg%2F3Ei3fN%2F0NEPCHl13Aa2r6%2BIuPjMwRwF5a6Oe50LAZlirox3mzQjG2hwWYtm6ndaKi%2F6YeLbZJyjDf1AH0UIsWyJAuYYLvJDZ16UyGECEYbNLcLcHja4cjlq2fud05X1epQrtmVO8foNBxbq9uLweiWHeAL9gpDPnUnvjonTK0%2FT7WN%2FMkQWtEkqptVzxYQNoH2mYDbjlERrVfMK3%2Bbc%2FpCaxOxIUsAed1kFS%2B7q8yJOX7EIeVs%2Fy6IC7Lix%7Ctkp%3ABFBM_q6Z7t1m",
    #     "selectors": {
    #         # Price selector: using data-testid + bold span (confirmed correct)
    #         "price": 'span[data-testid="ux-textual-display"] span.ux-textspans--BOLD', 
            
    #         # Title selector: using H1 tag and its internal bold span (confirmed correct)
    #         "title": 'h1.x-item-title__maintitle span.ux-textspans--BOLD' 
    #     },
    #     # Currency symbol: Set to Malaysian Ringgit (RM)
    #     "currency_symbol": "RM" 
    # },
     {
         "platform": "Temu",
        # 替换为您提供的实际马来西亚 Temu URL
        "url": "https://www.temu.com/my-en/---wireless-gaming-mouse-g-601099640454606.html?_oak_mp_inf=EM77rNSm1ogBGiA4NDg3OWMwZGMzZDI0YzhiOGZlZDg0MTBhZjZlNWZhOSDDrYWBrzM%3D&top_gallery_url=https%3A%2F%2Fimg.kwcdn.com%2Fproduct%2Ffancy%2Ffd045e07-ac51-45b8-a943-08190d60bdd3.jpg&spec_gallery_id=2334759315&refer_page_sn=10009&refer_source=0&freesia_scene=2&_oak_freesia_scene=2&_oak_rec_ext_1=NDc1NTE&_oak_gallery_order=385359402%2C779836408%2C2002303115%2C2025475164%2C1709299244&search_key=razer%20v3%20pro&refer_page_el_sn=200049&refer_page_name=search_result&refer_page_id=10009_1764965256926_3206ql7k6j&_x_sessn_id=skpjvnqdhk",
        "selectors": {
            # Temu 标题选择器：使用最简单的 H1 标签（根据截图是包含标题的标签）
            "title": 'h1', 
            
            # Temu 价格选择器：通过 Playwright 的 get_attribute('aria-label') 方法获取价格。
            # 我们只需要定位带有 aria-label 属性的父级 div 即可。
            "price": 'div[aria-label][role="text"]'
        },
        # 货币符号：根据您的截图，设置为马来西亚林吉特
        "currency_symbol": "RM" 
    },
    {
        "platform": "Lazada",
        "url": "https://www.lazada.com.my/products/pdp-i4426848765-s-24882409154.html?c=&channelParams=&key=2bgaming%252Bmouse%252Bnid%252B3A4426848765%252Bsrc%252BLazadaMainSrp%252BBrn%252B3A7F789dc8c5b87cf3d11bb53df585f18b%252Bredirect_id%252B3A300586176023%252Bsession_id%252B3A%252Bbiz_source%252B3Ah5_hp%252B3BsLot%252B3A0%252B3Butlog_bucket_id%252B3A3042786%252B3BtemplateInfo%252B3A107880_D_E%252523-1_A3_C%25252325231124_L%252523252325231124_L%252B3Bsearch&price=3A67800%2B3BdisplayPrice%3A67800%2B3BsinglePromotionId%3A3A7F789dc8c5b87cf3d11bb53df585f18b%2B3BoriginPrice%3A67800%2B3BdisplayPrice%3A67800%2B3BsinglePromotionId%3A3A7F789dc8c5b87cf3d11bb53df585f18b&review=42&sale=131&search=1&source=search&spm=a2o4k.searchlist.list.0&stock=1",
          "selectors": {
            # Lazada Price: Targeting the new precise class name
            "price": 'span.pdp-v2-product-price-content-salePrice-amount', 
            # Lazada Title: Targeting the new precise class name
            "title": 'h1.pdp-mod-product-badge-title-v2'
        },
        "currency_symbol": "RM"
    }
]

CSV_FILENAME = "price_history.csv"