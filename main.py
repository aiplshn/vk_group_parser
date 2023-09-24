from controller import *

if __name__ == '__main__':
    controller = Controller()
    posts_url = controller.startParser()
    with open('ad_walls.txt', 'w') as f:
        for post in posts_url:
            f.write(post+'\n')
    print('Done')
