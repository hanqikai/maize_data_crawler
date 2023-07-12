# 说明
* 本项目一个基于Python + Selenium + WebDriver的自动化爬虫项目，爬取的网站是惠农网(https://www.cnhnb.com/xt/ask/794/)和中国农技推广信息服务平台(http://njtg.nercita.org.cn/tech/question/list.shtml?code=0),主要对网站中的针对玉米的病害问答数据进行爬取，爬取玉米图片，农户问题，以及网站上的专家对问题的解答，以便于后期进行玉米病害分类和问答系统的构建。
* 之所以使用Selenium + WebDriver的自动化测试工具进行爬取数据而不使用scrapy等其他爬虫工具，是为了解决网站的反爬机制（图片全部替换掉了真实的URL，且有的图片使用了base64编码）。使用自动化测试工具模拟真实用户行为，进而获得图片的真实地址，进行下载。
* 使用浏览器的无头模式进行爬取，爬取过程对于用户是透明的（不会对用户使用计算机造成影响。
* 配置好环境直接运行hnw.py即可对惠农网(https://www.cnhnb.com/xt/ask/794/)玉米病害问答数据进行下载。运行njtg.py即可对中国农技推广信息服务平台(http://njtg.nercita.org.cn/tech/question/list.shtml?code=0)进行子url的获取，再运行process_njtg.py即可对子url进行玉米病害问答数据进行下载。
* 环境配置
    1. python >= 3.7
    2. pip install -r requirements.txt -i http://pypi.douban.com/simple/
    3. Run any scripts what you want!
