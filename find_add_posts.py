import requests
import time

class FinderAddPosts():
    def __init__(self, token: str = '') -> None:
        self.USER_TOKEN = token

    def findAdds(self, group_id: list, count_posts: int = -1) -> list:

        VERSION = '5.131'
        wall_ids = []
        offset = 0

        while True:
            if offset > count_posts and count_posts != -1:
                break
            try:
                response = requests.get('https://api.vk.com/method/wall.get',
                            params={'access_token': self.USER_TOKEN,
                                    'owner_id': -group_id,
                                    'v': VERSION,
                                    'offset': offset,
                                    'count': 100})
                count = int(response.json()['response']['count'])
                data = response.json()['response']['items']
                for item in data:
                    if int(item['marked_as_ads']) == 1:
                        wall_ids.append(int(item['id']))

                offset += 100
                if count == 0 or len(data) == 0:
                    break
                time.sleep(0.2)
            except Exception as e:
                print(e)
                break

        return wall_ids
