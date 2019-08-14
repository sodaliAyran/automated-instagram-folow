from tqdm import tqdm

from . import limits
from . import delay

def follow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if not self.check_user(user_id):
        return True
    if self.following == []:
        self.following = self.get_user_following(self.user_id)
    if user_id in self.following:
        return True # already following
    if limits.check_if_bot_can_follow(self):
        delay.follow_delay(self)
        if super(self.__class__, self).follow(user_id):
            self.logger.info("Follow user: %d" % user_id)
            self.total_followed += 1
            return True
    else:
        self.logger.info("Out of follows for today.")
    return False

def follow_users(self, user_ids):
    self.logger.info("Going to follow %d users." % len(user_ids))
    for user_id in tqdm(user_ids):
        if not self.follow(user_id):
            delay.error_delay(self)
            while not self.follow(user_id):
                delay.error_delay(self)
    self.logger.info("DONE: Total followed %d users." % self.total_followed)
    return True

def follow_followers(self, user_id, nfollows=None):
    self.logger.info("Follow followers of: %s" % user_id)
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id)
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        self.follow_users(follower_ids[:nfollows])
