from colorama import Fore, init
import click
import re
import requests
import bs4
from requests.exceptions import MissingSchema

BANNER = f'''
{Fore.RED}██████╗  ██████╗ ███████╗████████╗{Fore.BLUE}███╗   ███╗ █████╗ ███╗   ██╗
{Fore.RED}██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝{Fore.BLUE}████╗ ████║██╔══██╗████╗  ██║
{Fore.RED}██████╔╝██║   ██║███████╗   ██║   {Fore.BLUE}██╔████╔██║███████║██╔██╗ ██║    
{Fore.RED}██╔═══╝ ██║   ██║╚════██║   ██║   {Fore.BLUE}██║╚██╔╝██║██╔══██║██║╚██╗██║
{Fore.RED}██║     ╚██████╔╝███████║   ██║   {Fore.BLUE}██║ ╚═╝ ██║██║  ██║██║ ╚████║
{Fore.RED}╚═╝      ╚═════╝ ╚══════╝   ╚═╝   {Fore.BLUE}╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

           {Fore.RED}!только для образовательных целей!
      {Fore.BLUE}скрипт ищущий почты по регулярному выражению
          {Fore.GREEN}mail_finder.py {Fore.WHITE}<ссылка(с "http(s)")>
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
    return re.findall(r'\w+@\w+\.\w+', text)


@click.command()
@click.argument('url', required=1)
@click.option('-D', '--debug', 'debug', is_flag=True)
@click.option('-d', '--depth', 'depth')
@click.option('-f', '--file', 'file')
def main(url, debug, file, depth=1):
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

    if file:
        with open(file, 'w'):
            


if __name__ == '__main__':
    main()
