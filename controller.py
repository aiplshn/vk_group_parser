from group_finder import *
from find_add_posts import *
import os

class Controller():
    def __init__(self) -> None:
        self.config_dir = 'config'
        self.config_name = 'token.txt'
        self.keywords_filename = 'keywords.txt'
        self.token = self.getToken()
        self.count_members_filter = self.getFilterMembersGroup()
        self.count_wall_posts = self.getCountWallPosts()
        self.keywords = self.getKeywords()

    def getToken(self) -> str:
        user_token = ''

        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        config_path = os.path.join(self.config_dir, self.config_name)
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_token = f.readline()

        if user_token == '':
            user_token = input("Enter token: ")
            with open(config_path, 'w') as f:
                f.write(user_token)
        return user_token

    def getCountWallPosts(self) -> int:
        while True:
            try:
                count_wall_post = int(input("Count wall posts (-1 - all): "))
                if count_wall_post < -1:
                    print('Try again')
                    continue
                return count_wall_post
            except Exception as e:
                print(e)
                continue

    def getFilterMembersGroup(self) -> int:
        while True:
            try:
                count_members = int(input("Count members filter (-1 - all): "))
                if count_members < -1:
                    print('Try again')
                    continue
                return count_members
            except Exception as e:
                print(e)
                continue

    def getKeywords(self) -> list:
        keywords = []

        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        keywords_path = os.path.join(self.config_dir, self.keywords_filename)
        if os.path.exists(keywords_path):
            with open(keywords_path, 'r', encoding='UTF-8') as f:
                for line in f:
                    keywords.append(line.rstrip())

        if len(keywords) == 0:
            while True:
                keywords.append(str(input("Enter keyword: ")))
                if str(input("One more? (y/n)")) == 'n':
                    break
        with open(keywords_path, 'w', encoding='UTF-8') as f:
            for key in keywords:
                f.write(key+'\n')
        return keywords

    def startParser(self) -> list:
        group_parser = FinderGroups(self.token)
        posts_parser = FinderAddPosts(self.token)
        groups_id_set = set()
        for keyword in self.keywords:
            groups_id = group_parser.findGroupsId(keyword, self.count_members_filter)
            for id in groups_id:
                groups_id_set.add(id)

        walls_url = []
        set_size = len(groups_id_set)
        for id, i in zip(groups_id_set, range(len(groups_id_set))):
            walls_id = posts_parser.findAdds(id, self.count_wall_posts)
            print(f'Process: {100.0*(i+1)/set_size}%')
            for wall_id in walls_id:
                walls_url.append(f'https://vk.com/public{id}?w=wall-{id}_{wall_id}')

        return walls_url
