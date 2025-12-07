跨电商平台商品价格追踪与波动分析系统
1️⃣ 项目概述（Project Overview）
|
| 描述 | 内容 |
| 项目名称 | 跨电商平台商品价格追踪与波动分析系统 |
| 所选题目 | 建立简易系统，爬取至少 3 个不同电商平台上相同商品的价格数据，对比价格差异与波动。 |
| 核心追踪产品 | Razer Viper V3 Pro Wireless Esports Gaming Mouse |
| 追踪平台 | 亚马逊 (Amazon)，来赞达 (Lazada) |
| 失败平台 | 虾皮 (Shopee)，特姆 (Temu)，易贝 (eBay)（因硬性反爬机制被移除） |
系统的功能是什么？
数据抓取 (Scraping): 自动访问 Amazon 和 Lazada 的商品详情页，提取商品名称、当前价格和商品 URL。
数据持久化 (Persistence): 将抓取到的价格、时间戳和平台信息保存到本地 price_history.csv 文件中，形成历史价格数据库。
结果输出 (Reporting): 在控制台打印本次运行的抓取摘要，并显示成功和失败平台的数量。
整体架构说明
本项目采用了典型的客户端/脚本架构 (Script-Based Architecture)，重点在于稳定地执行 I/O 密集型任务（网络请求和文件操作）。



Getty Images
核心流程:
配置层 (config.py): 定义目标 URL、选择器和货币符号。
主控层 (main.py): 读取配置，串行调用抓取函数。
抓取层 (scraper.py): 核心工作区，利用 Playwright 启动无头浏览器，执行页面导航、反爬优化、数据提取。
数据层 (data_storage.py): 处理数据清理、格式化和持久化（写入 CSV）。
2️⃣ 规划过程（Planning）
7 天开发安排
| 阶段 | 天数 | 任务重点 | 结果 |
| I. 核心 MVP | Day 1-2 | 环境搭建，安装依赖 (Playwright)，实现 clean_price，完成 Amazon 稳定抓取。 | 成功从 Amazon 提取标题和价格。 |
| II. 动态抓取 | Day 3 | 引入 Lazada，解决 Playwright 动态加载和 JS 渲染问题，引入长等待策略。 | Lazada 基础抓取成功，但易失败。 |
| III. 持久化 | Day 4 | 实现 data_storage.py，完成 price_history.csv 的读写，确保数据持久化。 | 所有成功抓取的数据能够保存为历史记录。 |
| IV. 反爬挑战 | Day 5 | 应对 Shopee/Temu/eBay 的反爬失败，引入滚动模拟和 aria-label 特殊抓取逻辑。 | 确认 Shopee/Temu/eBay 无法在当前环境稳定抓取，决定移除。 |
| V. 报告整合 | Day 6-7 | 最终代码结构清理，main.py 整合，实现结果摘要输出，撰写项目报告。 | 系统稳定运行于 Amazon 和 Lazada，报告文件完成。 |
你的 MVP 是什么？
MVP (Minimum Viable Product) 是：能够成功从 Amazon (第一个平台) 抓取一个指定商品的名称和价格，并将结果打印到控制台。
哪些功能你优先、哪些你延后？为什么？
| 优先级 | 功能 | 原因 |
| 高 | Playwright 稳定启动与关闭 | Playwright 底层依赖异步事件循环，启动和关闭必须正确，否则整个系统崩溃 (Event loop is closed! 错误)。这是系统的地基。 |
| 中 | 引入 Lazada (动态加载) | 验证 Playwright 处理现代电商网站的能力，它是比 Amazon 更具挑战性的目标。 |
| 中 | 数据持久化 (CSV) | 满足项目对“对比价格差异与波动”的基本要求。 |
| 低 | 每日定时更新 | 依赖外部库 schedule 或系统定时任务，属于非核心功能。 |
| 低 | 价格波动趋势图 | 属于数据分析和展示层，可在数据稳定后实现。 |
3️⃣ 设计说明（Design）
如何处理不同平台的结构差异？
核心设计思想是配置驱动 (Configuration-Driven)。
差异封装： 所有平台特定的差异（URL、选择器、货币符号）都封装在 config.py 中。scraper.py 只负责读取配置，并使用通用的 Playwright 命令去执行。
通用工具： 使用 Playwright 的 CSS Selectors 和 XPath 来定位元素，这两种方式是业界最通用的。
动态加载处理：
Amazon (较稳定): 使用 wait_until("domcontentloaded")，仅等待 DOM 结构加载。
Lazada (动态JS): 使用更严格的 wait_until("networkidle")（等待网络请求平静），并给予长达 150 秒的超时时间。
如何避免爬虫失败？
主要通过四层防御来避免：
错误处理层 (Try-Except): 将所有网络请求和元素查找包装在 try...except 块中，确保单个平台失败不会导致整个程序崩溃。
生命周期管理层 (Finally): 在 scraper.py 中，使用 try...finally 结构，确保在任何错误发生后，浏览器实例 (browser) 都会被安全关闭，防止资源泄露或 Event loop is closed! 错误。
伪装与行为模拟层: 设置 User-Agent，并对 Lazada 进行页面滚动 (page.mouse.wheel) 和悬停 (page.hover("body")) 等操作，以模拟真实用户行为。
内容检查层: 在 Temu 等极难处理的平台上，我们使用 page.wait_for_function 强制等待元素的 aria-label 属性中包含长度大于 5 的字符串，确保抓取到的是实际价格而非空白占位符。
如何存储数据与历史价格？
我们选择了最轻量、最容易实现的方案：
数据结构: 每次抓取的结果以 Python 字典 (dict) 格式返回，包含平台、价格、标题、时间戳等键值对。
存储机制: 使用 Python 内置的 csv 模块将字典数据追加写入到 price_history.csv 文件。
优势: CSV 文件结构清晰，方便直接用 Pandas 读取进行后续的数据分析（如生成趋势图）。
4️⃣ 技术栈说明（Tech Stack）
| 类别 | 使用的技术/语言 | 解释和原因 |
| 核心语言 | Python 3.x | 强大的生态系统，丰富的库支持，如 Pandas 和 Playwright。 |
| 爬虫框架 | Playwright (Sync API) | 相比 Selenium 更现代，原生支持无头模式 (Headless)，且在应对 JavaScript 渲染和反爬方面比传统库 (如 Requests/BS4) 强大得多。 |
| 数据处理 | Pandas, csv 模块 | csv 负责文件的读写和格式化；Pandas (虽然目前未完全用于报告，但已导入) 方便进行数据清洗和未来的历史价格分析。 |
| 定时任务 | schedule (可选) | 提供了一个简单易用的 Python 接口来安排每天的定时任务。 |
为什么选它们？有什么替代方案？为什么不用？
替代爬虫方案： Scrapy 或 Requests/BeautifulSoup。
弃用原因: Requests/BS4 无法执行 JavaScript，无法抓取 Lazada、Temu 等动态网站。Scrapy 虽然强大，但学习曲线较陡，且在处理浏览器自动化时不如 Playwright 简洁高效。
替代自动化方案： Selenium。
弃用原因: Playwright 性能更高，API 更简洁，原生支持多种浏览器，且在绕过部分浏览器指纹检测方面表现更优。
替代存储方案： SQLite 或 MongoDB。
弃用原因: 针对 MVP，使用本地 CSV 文件足以满足数据持久化和历史追踪的基本需求，无需引入数据库的复杂性。
5️⃣ 开发过程记录（Development Process）
遇到什么问题？
核心错误：Event loop is closed! Is Playwright already stopped?
这是在多次调用 fetch_product_data 时，Playwright 异步事件循环被提前或重复关闭导致的。
解决尝试: 通过在 scraper.py 中精确地将 browser.close() 移入 try...finally 块，并确保其在 with sync_playwright() as p: 的外部被安全地检查和调用，从而彻底解决了该生命周期错误。
最大的困难：电商平台的反爬机制 (Shopee/Temu/eBay)。
即使使用 Playwright 和长等待时间，这些平台仍会重定向到验证码页或登录页，或隐藏价格数据。
解决尝试:
Lazada: 通过 page.mouse.wheel() 滚动和 networkidle 成功解决。
Temu: 发现价格被分散在带有 aria-hidden="true" 属性的 span 中，并成功引入了 element.get_attribute('aria-label') 的特殊逻辑来抓取隐藏数据。
Shopee/eBay: 最终确定为 IP/指纹级别的硬性阻断，在当前环境下无法绕过，故决定移除出追踪列表。
你如何确定你的解决方法是正确的？
错误解决 (如 Event loop is closed!): 运行单元测试（即多次调用 fetch_product_data），直到错误不再出现，且程序能够稳定、无警告地运行完成。
抓取成功 (如 Lazada/Temu): 验证 data["price"] 不为 None，且控制台打印的货币符号和数值与预期一致。对于 Temu 的 aria-label 解决方案，通过在 Playwright 有头模式下观察确认 aria-label 属性中确实包含了完整的价格信息。
6️⃣ 测试（Testing）
你的测试方法
我们主要采用集成测试 (Integration Testing) 的方式，即运行 main.py 来测试整个流程：从网络抓取到数据存储。同时，我们对关键函数如 clean_price 进行单元测试。
5 个测试案例（输入 & 预期输出）
| # | 测试案例 (输入) | 预期输出 (Expected Output) | 实际输出 (Actual Output) |
| 1 | Amazon (Razer Mouse) | 成功抓取，价格 $XXX.XX，price_history.csv 记录一行数据。 | ✅ 成功 |
| 2 | Lazada (Razer Mouse) | 成功抓取，价格 RMXXX.XX，price_history.csv 记录一行数据。 | ✅ 成功 |
| 3 | 无效 URL | fetch_product_data 抛出超时或导航错误，返回 price=None，main.py 报告失败。 | ✅ 失败处理正确 |
| 4 | clean_price("RM1,299.50", "RM") | 返回浮点数 1299.50。 | ✅ 1299.50 |
| 5 | 抓取 Shopee (硬反爬) | 警告: 价格元素等待超时，返回 price=None，程序继续运行下一平台。 | ✅ 失败处理正确 |
如何确保系统稳定运行？
依赖锁定制: 使用虚拟环境，确保所有依赖版本兼容。
资源管理: 每次抓取完成后立即安全关闭浏览器 (browser.close() 在 finally 块中)，防止资源耗尽。
网络隔离: 在每次抓取之间使用 time.sleep(2) 进行礼貌性延迟，避免被服务器禁止访问。
7️⃣ 运行方式（How to Run）
环境需求
操作系统: Windows / macOS / Linux
环境: Python 3.8+
依赖: Playwright, Pandas, Schedule (可选)
安装方式
创建和激活虚拟环境:
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate




安装 Python 依赖:
(venv) pip install playwright pandas jinja2 schedule




安装 Playwright 浏览器驱动:
(venv) playwright install chromium




启动方式与示例
在已激活的虚拟环境中，进入项目根目录，运行主脚本：
(venv) python main.py




示例输出 (控制台):
>> 启动价格追踪程序...
✅ 创建历史文件: price_history.csv
正在尝试抓取: Amazon - [https://www.amazon.com/](https://www.amazon.com/)...
成功: Amazon 价格为 $535.06
✅ 成功保存数据到 price_history.csv: Amazon - 535.06
正在尝试抓取: Lazada (Demo Link) - [https://www.lazada.com.my/](https://www.lazada.com.my/)...
尝试 Lazada (Demo Link)：模拟滚动和悬停...
成功: Lazada (Demo Link) 价格为 RM678.00
✅ 成功保存数据到 price_history.csv: Lazada (Demo Link) - 678.0
==================================================
         商品价格追踪报告         
==================================================

[Amazon]
  商品: Razer Viper V3 Pro Wireless Esports Gaming Mouse ...
  价格: $535.06
  状态: ✅ 成功抓取并已保存历史记录

[Lazada (Demo Link)]
  商品: Razer Viper V3 Pro Wireless Esports Gaming Mouse ...
  价格: RM678.00
  状态: ✅ 成功抓取并已保存历史记录

==================================================
总计尝试: 2 | 成功: 2 | 失败: 0
价格历史记录已保存在 price_history.csv 文件中。
==================================================




8️⃣ 学习内容（What You Learned）
| 学习领域 | 具体内容 |
| Playwright 进阶 | 掌握了 context 和 browser 的生命周期管理，使用 try...finally 结构避免了关键的 Event loop is closed! 错误。 |
| 反爬虫技术 | 深入理解了电商平台如何使用 DOM 混淆（动态类名）和 内容隐藏 (aria-hidden) 来防御爬虫。 |
| 突破隐藏数据 | 学习并实践了利用元素的 aria-label 属性来抓取视觉上隐藏但为了无障碍访问而保留的完整价格数据，这是解决 Temu 问题的关键。 |
| 代码结构优化 | 实现了配置驱动的架构，将所有平台特定的抓取逻辑从核心代码中抽象出来，提高了可维护性和可扩展性。 |
9️⃣ 如果有更多时间，你会如何优化？（Mandatory）
如何优化性能？
异步爬虫 (Async/Await): 将同步的 playwright.sync_api 切换到 playwright.async_api，并在 main.py 中使用 Python 的 asyncio。这将允许程序同时发起多个网络请求，而不是串行等待，大幅缩短抓取时间。
禁用资源加载: 在 Playwright 启动时，禁用图片、CSS 和字体文件的加载，这可以节省大量带宽和渲染时间。
如何提升架构？
数据库持久化: 将数据存储从 CSV 切换到 SQLite 或 PostgreSQL。这将使查询历史价格、执行复杂聚合（如计算波动率）和并发写入更加稳定和高效。
服务化: 将爬虫打包成一个简单的 API 服务（如使用 Flask 或 FastAPI），而不是一个纯粹的脚本，方便其他应用调用。
如何提高稳定性？
代理池集成: 集成一个付费的住宅代理 IP 池。这是解决 Shopee、Temu 等平台 IP 封锁问题的唯一有效方法。
Headful 模式增强: 仅在抓取 Lazada/Temu 时，使用 Playwright 的 launch_persistent_context 启用有头模式，并注入 JS 代码来绕过特定的指纹检测。
如何扩展功能？
货币自动转换: 集成外部 API (如 Fixer.io) 来实时获取汇率，将所有平台的价格统一转换为一个标准货币 (如 RM 或 USD)，实现真正的价格对比。
价格波动图表: 使用 Plotly 或 Matplotlib 库，基于历史 CSV 数据，生成并嵌入到 HTML 报告中的价格波动趋势图。
AI 总结: 集成 Gemini API，自动生成“目前最低价为 XX，建议从 YY 购买”的一句话结论。
下一步你会做什么？
我的下一步将是实现货币自动转换。因为目前 Amazon 的价格是美元 ($)，而 Lazada 的价格是马币 (RM)，直接对比没有意义。实现货币转换是实现“对比价格差异”这一核心要求的关键步骤。
