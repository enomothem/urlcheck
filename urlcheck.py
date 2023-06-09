import argparse
import asyncio
import aiohttp
import time
from art import *

# ANSI转义序列
GREEN = '\033[92m'  # 绿色
RED = '\033[91m'  # 红色
END = '\033[0m'  # 结束


async def check_url(url, alive_urls, timeout):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    print(GREEN + '[+] ' + url + " is alive" + END)
                    alive_urls.add(url)
                else:
                    print(RED + '[-] ' + url + " is not alive" + END)
    except:
        print(RED + '[-] ' + url + " is not alive" + END)


def main():
    my_text = "URLCHECK"
    my_art = text2art(my_text, font="starwars")
    print(my_art)
    parser = argparse.ArgumentParser(description='欢迎使用urlcheck  作者：月影')
    parser.add_argument('-f', '--file', type=str, help='指定文件批量探测')
    parser.add_argument('-u', '--url', type=str, help='指定一个URL进行探测')
    parser.add_argument('-t', '--timeout', type=int, default=20, help='设置超时时间，默认为30秒，建议50秒')
    parser.add_argument('-k', '--key-file', type=str, default='key.txt', help='指定字典文件，默认为key.txt')
    parser.add_argument('-H', '--help-info', action='help', help='显示所有参数及描述\n\n')

    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            urls = f.read().splitlines()
    elif args.url:
        urls = [args.url]
    else:
        parser.print_help()
        return

    urls = ['http://' + url + '/' if not url.startswith(('http://', 'https://')) else url + '/' for url in urls]

    with open(args.key_file) as f:
        keys = f.read().splitlines()

    urls_with_keys = [url + key for url in urls for key in keys]

    start_time = time.time()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    alive_urls = set()
    count = 0
    tasks = [loop.create_task(check_url(url, alive_urls, args.timeout)) for url in urls_with_keys]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    end_time = time.time()

    for url in alive_urls:
        count += 1
    print("存活的URL数量为: %d" % count)
    print("扫描完毕，总耗时: %.2f 秒" % (end_time - start_time))


    with open('alive.txt', 'w') as f:
        for url in alive_urls:
            f.write(url + '\n')


if __name__ == '__main__':
    main()
