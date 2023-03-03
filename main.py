# ЯНДЕКС ПОЛИГОН ----  y0_AgAAAABhMxEEAADLWwAAAADcmzWG_XgBzmXBRaSd_ei34nygBZAZY9o
# ВК АПИ ------  id=
# access_token=vk1.a.HfXzgdhp_Sewd5HDyvV__Si74vkTKzME2Nk0fmkBqrA6DiH4_a9ERsgYke9dLWtDYIb2O-gA1VhenIjd1jtqfHPylhb0xx--Og4t2dgIzL5kCXNmDwfsjSCggcGGsbWs7bq8v2Sf4mxOxYa9WIouBBCEsZU747NaCFUr0ctYUS2t-ODhUUSA2xly7vLfdztr_wq0g7UjzzylTIRybY05cg&expires_in=0&
# user_id=646055837

import requests
import os
import json
import time
from pprint import pprint
from progress.bar import Bar

id = ''
token_vk = ''


class DownloadsPhoto:

    def __init__(self, user_id: str, token_vk: str):
        self.user_id = user_id
        self.token_vk = token_vk
        self.direct = r'X:\PhotoVk'

    def downloads_photo_from_vk(self):
        # os.mkdir(self.direct)
        os.chdir(self.direct)
        url_vk = 'https://api.vk.com/method/photos.get'
        params_vk = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': '1',
            'access_token': self.token_vk,
            'v': '5.131'
        }
        res = requests.get(url_vk, params=params_vk)
        bar = Bar('Скачивание фото', max=len(res.json()['response']['items']))
        list_name_fils_by_likes = []
        list_name_fils_by_date = []
        for i in res.json()['response']['items']:
            list_name_fils_by_likes.append(i['likes']['count'])
            list_name_fils_by_date.append(i['date'])
            url_photo = i['sizes'][-1]['url']
            self.size = i['sizes'][-1]['type']
            new_list_name = []
            for i, char in enumerate(list_name_fils_by_likes):
                if char not in new_list_name:
                    new_list_name.append(char)
                else:
                    list_name_fils_by_likes[i] = list_name_fils_by_date[i]
            response = requests.get(url_photo)
            for name in list_name_fils_by_likes:
                continue
            with open(f"{name}.jpg", "wb") as f:
                f.write(response.content)
                bar.next()
                time.sleep(1)
            logs_list = []
            download_log = {'file_name': name, 'size': self.size}
            logs_list.append(download_log)
            with open(f'{self.direct}/log.json', 'a') as file:
                json.dump(logs_list, file, indent=2)


if __name__ == '__main__':
    user1 = DownloadsPhoto(id, token_vk)
    user1.downloads_photo_from_vk()

token_yandex = ''


class UploadPhoto:

    def __init__(self, token_yandex: str):
        self.token_yandex = token_yandex
        self.direct = r'X:\PhotoVk'
        self.number_of_files_to_send = 5

    def uploading_files_to_yandex_disk(self, path):
        os.chdir(self.direct)
        files_list = [name for name in os.listdir(self.direct) if name.endswith(".jpg")]
        bar = Bar('Отправление файлов на Я.диск', max=len(files_list))
        count = 0
        number_of_sent = 0
        for name_file in files_list:
            count += 1
            while count <= self.number_of_files_to_send:
                number_of_sent += 1
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'OAuth {self.token_yandex}'
                }
                params = {
                    'path': f'{path}/{name_file}',
                    'overwrite': True
                }
                upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
                response = requests.get(upload_url, headers=headers, params=params)
                href = response.json().get("href", "")
                response = requests.api.put(href, data=open(name_file, 'rb'), headers=headers)
                bar.next()
                time.sleep(0.5)
                break
        if number_of_sent in range(2, 5):
            print(f'\nНа Я.диск отправлено: {number_of_sent} файла')
        elif number_of_sent in range(5, 21) or number_of_sent == 0:
            print(f'\nНа Я.диск отправлено: {number_of_sent} файлов')
        elif number_of_sent == 1 or number_of_sent == 21:
            print(f'\nНа Я.диск отправлен: {number_of_sent} файл')

    def creating_a_new_folder_on_yandex_disk(self, name_folder: str):
        headers = {
            "Accept": 'application/json',
            'Authorization': f'OAuth {self.token_yandex}'
        }
        params = {
            'path': f'/{name_folder}',
        }
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        requests.put(upload_url, headers=headers, params=params)
        return name_folder


if __name__ == '__main__':
    user1 = UploadPhoto(token_yandex)
    user1.uploading_files_to_yandex_disk(user1.creating_a_new_folder_on_yandex_disk('Фотки с Vk'))
