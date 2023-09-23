import requests
import time
import json
import os
#https://dev.vk.com/ru/method/groups.search
#https://dev.vk.com/ru/method/groups.getMembers
#https://vk.com/apps?act=manage

CONFIG_NAME = 'config.txt'
TOKEN_USER = ''
result_folder = 'results'
break_condition = False
while not break_condition:
    COUNT_MEMBERS_FILTER = int(input("Count members filter: "))
    KEYWORD = str(input("Keyword: "))

    if os.path.exists(CONFIG_NAME):
        with open(CONFIG_NAME, 'r') as f:
            TOKEN_USER = f.readline()

    if TOKEN_USER == '':
        TOKEN_USER = input("Enter token: ")
        with open(CONFIG_NAME, 'w') as f:
            f.write(TOKEN_USER)

    # переменные 
    VERSION = '5.131' #версися api vk
    sort = 6 # по кол-ву участников

    result_url_groups = []
    groups_id = []

    offset = 0
    while True:
        try:
            response = requests.get('https://api.vk.com/method/groups.search',
            params={'access_token': TOKEN_USER,
                    'q': KEYWORD,
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
    offset = -500
    while True:
        try:
            offset += 500
            if offset >= len(groups_id):
                break
            time.sleep(0.2)
            response_members = requests.get('https://api.vk.com/method/groups.getById',
                                params = {'access_token': TOKEN_USER,
                                'group_ids': json.dumps(groups_id[offset:offset+500:]),
                                'fields': 'members_count',
                                'v': VERSION})
            groups = response_members.json()['response']
            for group in groups:
                try:
                    if int(group['is_closed']) == 0 and \
                            int(group['members_count']) >= COUNT_MEMBERS_FILTER and \
                            'deactivated' not in group and \
                            (group['type'] == 'group' or group['type'] == 'page'):
                        result_url_groups.append('https://vk.com/club' + str(group['id']))
                    # else:
                    #     print("Id: ", group['id'], "Closed: ", group['is_closed'], 'Member count: ', group['members_count'], "deactivated: ", 'deactivated' in group, 'Type: ', group['type'])
                except Exception as e:
                    print(e)
                    continue
            
        except Exception as e:
            print(response_members.text)


    isExist = os.path.exists(result_folder)
    if not isExist:
        os.makedirs(result_folder)
    res_path_file = os.path.join(result_folder, KEYWORD + '.txt')

    with open(res_path_file, 'w') as f:
        for group_url in result_url_groups:
            f.write(group_url + "\n")
    print("Find " + str(len(result_url_groups)) + " groups")
    answer = input("One more? (y/n): ")
    if answer == 'n':
        break_condition = True