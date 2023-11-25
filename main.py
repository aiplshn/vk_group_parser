from controller import *

if __name__ == '__main__':
    controller = Controller()
    posts_url, groups = controller.startParser()
    with open('ad_walls.txt', 'w') as f:
        for post in posts_url:
            f.write(post+'\n')
    with open('groups.txt', 'w') as f:
        for group in groups:
            f.write(group+'\n')
    print('Done')
