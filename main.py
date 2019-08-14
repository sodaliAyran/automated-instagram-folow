from configurations import INSTAGRAM_PASSWORD, INSTAGRAM_USER_NAME
from automated_instagram_user import AutomatedInstagramUser
import time
import logging
import numpy as np
import random


def follow_users(user, split):
    for username in split:
        logger.info("Following user %s", username)
        user.follow(username)
        time.sleep(random.randint(5, 25))


def wait_for_follow_back(wait_time_in_seconds=30):
    logger.info("Waiting for users to follow back")
    time.sleep(wait_time_in_seconds)
    logger.info("Time's up let's check who followed us back.")


def check_follow_backs(user, split, non_followers, return_followers):
    followers = [u["username"] for u in user.get_followers()]
    for username in split:
        if username not in followers:
            non_followers.append(username)
            logger.info("%s didn't follow us back.", username)
            user.unfollow(username)
        elif username in split:
            return_followers.append(username)
            logger.info("FOLLOWED US BACK: %s followed us back", username)
    return non_followers, return_followers
    

def main(user_list):
    logger.info("Initializing user %s", INSTAGRAM_USER_NAME)
    user = AutomatedInstagramUser()
    user.login(username=INSTAGRAM_USER_NAME, password=INSTAGRAM_PASSWORD)

    non_followers = []
    return_followers = []
    splits = np.array_split(np.array(user_list), 5)
    
    for split in splits:
        follow_users(user, split)
        # Wait for 1 day before checking follow back
        wait_for_follow_back(15)
        non_followers, return_followers = check_follow_backs(user, split, non_followers, return_followers)
        logger.info("End of split, starting next one...")
        
    logger.info(f"FOLLOW BACK LIST: {return_followers}")
    logger.info(f"Here is the unfollower list {non_followers}")
    

# Setting Up Logging
logging.basicConfig(level=logging.INFO)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()

fileHandler = logging.FileHandler("automated_follow.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


with open("instagram_test_list.txt", "r") as f:
    USER_LIST = [x.strip() for x in f.readlines()]

main(user_list=USER_LIST)

