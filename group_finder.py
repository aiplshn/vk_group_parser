import requests
import time
import json
import os
#https://dev.vk.com/ru/method/groups.search
#https://dev.vk.com/ru/method/groups.getMembers
#https://vk.com/apps?act=manage

class FinderGroups():
    def __init__(self, token: str = '') -> None:
        self.USER_TOKEN = token

    def findGroupsId(self, keyword: str, count_members_filter: int = 3000):
        VERSION = '5.131' #версися api vk
        sort = 6 # по кол-ву участников

        result_url_groups = []
        groups_id = []

        offset = 0
        while True:
            try:
                response = requests.get('https://api.vk.com/method/groups.search',
                params={'access_token': self.USER_TOKEN,
                        'q': keyword,
                        'sort': sort,
                        'v': VERSION,
                        'offset': offset,
                        'count': 1000})
                count = int(response.json()['response']['count'])
                data = response.json()['response']['items']
                for item in data:
                    id = int(item['id'])
                    groups_id.append(id)
                offset += 1000
                if count == 0 or len(data) == 0:
                    break
                time.sleep(0.2)
            except Exception as e:
                print(response.text)
                break

        print('Find ' + str(len(groups_id)) + ' groups. Start filtered...')
        groups_id_filtered = []
        offset = -500
        while True:
            try:
                offset += 500
                if offset >= len(groups_id):
                    break
                time.sleep(0.2)
                response_members = requests.get('https://api.vk.com/method/groups.getById',
                                    params = {'access_token': self.USER_TOKEN,
                                    'group_ids': json.dumps(groups_id[offset:offset+500:]),
                                    'fields': 'members_count',
                                    'v': VERSION})
                groups = response_members.json()['response']
                for group in groups:
                    try:
                        if int(group['is_closed']) == 0 and \
                                int(group['members_count']) >= count_members_filter and \
                                'deactivated' not in group and \
                                (group['type'] == 'group' or group['type'] == 'page'):
                            result_url_groups.append('https://vk.com/club' + str(group['id']))
                            groups_id_filtered.append(int(group['id']))
                    except Exception as e:
                        print(e)
                        continue

            except Exception as e:
                print(response_members.text)

            print(f'Filter is done. Filtered {len(groups_id_filtered)} groups')
            return groups_id_filtered
