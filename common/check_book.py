# -*- coding: utf-8 -*-
# +-------------------------------------------------------------------
# | Date: 2022/11/29
# +-------------------------------------------------------------------
# | Author: Pluto <i@aoaostar.com>
# +-------------------------------------------------------------------
import urllib.parse

from common import async_util


async def check_book(book_rule: dict):
    return await check_book_by_search(book_rule)
    # return await check_book_by_tcp_ping(book_rule)


async def check_book_by_search(book_rule: dict):
    from LegadoParser2.RuleCompile import compileBookSource
    from common.legado_parse.search import search
    for keywords in ["我的", "系统", "老", "我", "的", "修", "在"]:
        try:
            compiledBookSource = compileBookSource(book_rule)
            searchResult = await search(compiledBookSource, keywords)
            if len(searchResult) > 0:
                return True, f"[{keywords}] 搜索结果数: {len(searchResult)}"
            else:
                continue
        except Exception as e:
            # raise e
            return False, e.__str__()

    return False, f"搜索结果数: {len(searchResult)}"


async def check_book_by_tcp_ping(book_rule: dict):
    urlparse = urllib.parse.urlparse(book_rule['bookSourceUrl'])
    hostname = urlparse.hostname
    port = urlparse.port
    if hostname is None and 'searchUrl' in book_rule:
        urlparse2 = urllib.parse.urlparse(book_rule['searchUrl'])
        if urlparse2.hostname is not None:
            hostname = urlparse2.hostname
            port = urlparse2.port
    if hostname is None:
        return True, '无法获取到hostname'
    try:
        ping = await async_tcp_ping(host=hostname, port=port or 80, timeout=10)
        return True, f'{hostname} %.f ms' % ping
    except Exception as e:
        return False, f"{hostname} {e}"


async def async_tcp_ping(host, port, timeout=10):
    import asyncio
    import async_timeout
    from timeit import default_timer as timer
    time_start = timer()
    num = 3
    for i in range(num):
        try:
            async with async_timeout.timeout(delay=timeout):
                await asyncio.open_connection(host, port)
            break
        except Exception as e:
            if i == num:
                raise e
    time_end = timer()
    time_cost_milliseconds = (time_end - time_start) * 1000.0
    return time_cost_milliseconds


if __name__ == '__main__':
    print(async_util.run(check_book({
        "bookSourceComment": "",
        "bookSourceGroup": "Namo",
        "bookSourceName": "斋 书 苑",
        "bookSourceType": 0,
        "bookSourceUrl": "https://www.zhaishuyuan.org#",
        "bookUrlPattern": "",
        "concurrentRate": "",
        "customOrder": 1,
        "enabled": True,
        "enabledExplore": False,
        "exploreUrl": "玄幻::/category/xuanhuan_{{page}}.html\n修真::/category/xiuzhen_{{"
                      "page}}.html\n都市::/category/dushi_{{page}}.html\n穿越::/category/chuanyue_{{"
                      "page}}.html\n网游::/category/wangyou_{{page}}.html\n科幻::/category/kehuan_{{"
                      "page}}.html\n其他::/category/qita_{{page}}.html",
        "header": "",
        "lastUpdateTime": 1638335360694,
        "loginCheckJs": "",
        "loginUi": "",
        "loginUrl": "",
        "respondTime": 180000,
        "ruleBookInfo": {
            "author": "[property=\"og:novel:author\"]@content",
            "coverUrl": "[property=\"og:image\"]@content",
            "intro": "id.bookintro@html",
            "kind": "[property=\"og:novel:category\"]@content&&[property=\"og:novel:status\"]@content&&["
                    "property=\"og:novel:update_time\"]@content##小说|\\s.*",
            "lastChapter": "[property=\"og:novel:latest_chapter_name\"]@content",
            "name": "[property=\"og:novel:book_name\"]@content",
            "wordCount": ".count@tag.span.-1@text"
        },
        "ruleContent": {
            "content": "id.content@html",
            "imageStyle": "0",
            "nextContentUrl": "id.next_url@href",
            "replaceRegex": "##感谢.*打赏.*|\\【看书福利.*|\\（未完待续\\）|无弹窗.*|\\【加入书签.*|\\（本章未完，请翻页\\）|\\（本章完\\）"
        },
        "ruleExplore": {
            "author": "tag.a.2@text",
            "bookList": ".shulist ul",
            "bookUrl": "tag.a.0@href",
            "coverUrl": "tag.a.0@href##.+\\D((\\d+)\\d{3})\\D##https://img.zhaishuyuan.org/$2/$1/$1s.jpg###",
            "kind": "tag.li.1@text&&tag.li.5@text##\\[|小说.*",
            "lastChapter": "tag.a.1@text",
            "name": "tag.a.0@text",
            "wordCount": "tag.li.4@text"
        },
        "ruleSearch": {
            "author": "tag.a.2@text",
            "bookList": "#sitembox dl",
            "bookUrl": "tag.a.1@href",
            "coverUrl": "tag.img@src",
            "intro": "tag.dd.2@text##\\s",
            "kind": "tag.span.2@text&&tag.span.3@text&&tag.span.5@text##小说|\\s.*",
            "lastChapter": "class.book_other.1@text##最新章节.| 更新时间.",
            "name": "tag.a.1@text",
            "wordCount": "tag.span.4@text"
        },
        "ruleToc": {
            "chapterList": "#readerlist li",
            "chapterName": "tag.a@text##-",
            "chapterUrl": "tag.a@href"
        },
        "searchUrl": "https://www.zhaishuyuan.org/search/?searchkey={{key}}",
        "weight": 0
    })))
