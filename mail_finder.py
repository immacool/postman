import re

import bs4
import click
import requests
from colorama import Fore, init
from requests.exceptions import MissingSchema
from json import dump

init()

BANNER = f'''
{Fore.RED}██████╗  ██████╗ ███████╗████████╗{Fore.BLUE}███╗   ███╗ █████╗ ███╗   ██╗
{Fore.RED}██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝{Fore.BLUE}████╗ ████║██╔══██╗████╗  ██║
{Fore.RED}██████╔╝██║   ██║███████╗   ██║   {Fore.BLUE}██╔████╔██║███████║██╔██╗ ██║    
{Fore.RED}██╔═══╝ ██║   ██║╚════██║   ██║   {Fore.BLUE}██║╚██╔╝██║██╔══██║██║╚██╗██║
{Fore.RED}██║     ╚██████╔╝███████║   ██║   {Fore.BLUE}██║ ╚═╝ ██║██║  ██║██║ ╚████║
{Fore.RED}╚═╝      ╚═════╝ ╚══════╝   ╚═╝   {Fore.BLUE}╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

           {Fore.RED}!только для образовательных целей!
      {Fore.BLUE}скрипт ищущий почты по регулярному выражению
                {Fore.GREEN}mail_finder.py {Fore.WHITE}<ссылка>
           {Fore.RED}!только для образовательных целей!{Fore.RESET}
'''

print(BANNER)


def request(url, *args, **kwargs):
    try:
        return requests.get(url, *args, **kwargs)
    except MissingSchema:
        return requests.get('http://' + url, *args, **kwargs)


def find_mails(url):
    text = request(url).text
    matches = re.findall(r'\w+@\w+\.\w+', text)
    return list(set(matches))


@click.command()
@click.argument('url', required=1)
@click.option('-D', '--debug', 'debug', is_flag=True)
@click.option('-d', '--depth', 'depth')
@click.option('-f', '--file', 'file')
@click.option('-j', '--json', 'json')
def main(url, debug, file, json, depth=1):
    mails = {}

    text = request(url).text
    s = bs4.BeautifulSoup(text, 'html.parser')
    outer_links = []
    for a in s.find_all('a'):
        a_href = a.get('href')
        if isinstance(a_href, str):
            if a_href.startswith('http'):
                outer_links.append(a_href)

    mails[url] = find_mails(url)
    for href in outer_links:
        try:
            mails[href] = find_mails(href)
        except Exception:
            pass

    tmp = []
    blank_hrefs = []
    for href, mails in mails.items():
        if not mails:
            blank_hrefs.append(href)
        else:
            tmp.append(href + '\n')
            for mail in mails:
                tmp.append(f'\t{mail}\n')
            tmp.append('\n')
    tmp.append('\nПо ссылкам идущим далее не найдено ни одной почты.\n')
    [tmp.append(f'{bh}\n') for bh in blank_hrefs]

    if file:
        with open(file, 'w', encoding='utf-8') as f_cursor:
            f_cursor.writelines(tmp)
    elif json:
        # не работает!
        with open(json, 'w', encoding='utf-8') as f_io:
            dump(mails, f_io)
    else:
        print(*tmp)


if __name__ == '__main__':
    main()
