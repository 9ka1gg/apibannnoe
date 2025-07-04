import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def shorten_link(vk_token, link):
    url = f'https://api.vk.ru/method/utils.getShortLink'
    payload = {'v': 5.199, 'url': link}
    headers = {'Authorization': f'Bearer {vk_token}'}
    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(vk_token, link):
    link = urlparse(link).path.replace('/', '')
    url = f'https://api.vk.ru/method/utils.getLinkStats'
    payload = {'v': 5.199, 'key': link, 'interval': 'forever', 'extended': 0}
    headers = {'Authorization': f'Bearer {vk_token}'}
    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['response']['stats'][0]['views']
    if clicks_count == None:
        return 0 
    return clicks_count


def is_shorten_link(vk_token, link):
    url = f'https://api.vk.ru/method/utils.getLinkStats'
    key = urlparse(link).path.replace('/', '')
    payload = {'v': 5.199, 'key': key}
    headers = {'Authorization': f'Bearer {vk_token}'}
    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()
    return 'error' not in response.json()  


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description='Программа для сокращения ссылок')
    parser.add_argument('--link', help='Обрабатываемая ссылка')
    args = parser.parse_args()
    parsed_url = urlparse(args.link)
    vk_token = os.getenv("VK_TOKEN")
    try:
        if is_shorten_link(vk_token, args.link):
            print('Количество переходов:', count_clicks(vk_token, parsed_url.path.replace('/', '')))
        else:
            print('Сокращённая ссылка:', shorten_link(vk_token, args.link))
    except requests.HTTPError:
        print('Ошибка при обработке. Проверьте вашу ссылку и токен.')


if __name__ == '__main__':
    main()