import json
import requests
from pprint import pprint


class VKYDClient:
    API_BASE_URL = 'https://api.vk.com/method/'
    token = ('vk1.a.npc3PMXyA5_kjdIY94FI2UmHttNtzUjp4QqYtSzsL3nR0C-'
             'RKfaYM8l9bmXUcfWlyMIAQR4rtuvMsNkl6Uf5NcXFENW8XA2yYqU5NKe0t2RI9JI1pkLkgR-'
             'YMr_JOnRaLpdPDk_mpNlnE0wAEedMJ5Jn9YdXrKVTEUN3JPSvUQFPf1kbNbTmh9oKeWw7Z'
             'hRMvJw_n_LDhiRVHBodxn7qmg')

    def __init__(self, yd_token, user_id):
        self.yd_token = yd_token
        self.user_id = user_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.199'
        }

    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'

    def get_profile_photos(self):
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile',
                       'extended': '1'})
        response = requests.get(self._build_url('photos.get'), params=params)
        return response.json()

    def load_photos_to_yd(self, number_of_photos=5):
        url_for_dir = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {
            'path': 'VK-photos'
        }
        headers = {
            'Authorization': f'OAuth {self.yd_token}'
        }
        response = requests.put(url_for_dir,
                                headers=headers,
                                params=params)
        photos_info = self.get_profile_photos()['response']['items']
        likes = set()
        result = []
        for photo in photos_info[:number_of_photos]:
            likes_count = photo['likes']['count']
            file_name = f'{likes_count}.jpg'
            date = photo['date']
            if likes_count in likes:
                file_name = f'{likes_count}_{date}.jpg'
            likes.add(likes_count)
            file_url = photo['sizes'][-1]['url']
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            params = {
                'url': file_url,
                'path': f'VK-photos/{file_name}',
            }
            headers = {
                'Authorization': f'OAuth {self.yd_token}'
            }
            response = requests.post(url,
                                     headers=headers,
                                     params=params)
            result.append({'file_name': file_name, 'size': 'z'})
        with open("result.json", "w") as f:
            json.dump(result, f)
        return result


if __name__ == '__main__':
    vk_user_id = input('Введите VK_id пользователя: ')
    yd_user_token = input('Введите токен аккаунта Yandex: ')
    vkyd_client = VKYDClient(yd_user_token, vk_user_id)
    pprint(vkyd_client.load_photos_to_yd(2))