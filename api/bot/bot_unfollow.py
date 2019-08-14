from tqdm import tqdm

from . import limits
from . import delay


def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if self.check_user(user_id):
        return True  # whitelisted user
    if limits.check_if_bot_can_unfollow(self):
        delay.unfollow_delay(self)
        if super(self.__class__, self).unfollow(user_id):
            self.total_unfollowed += 1
            return True
    else:
        self.logger.info("Out of unfollows for today.")
    return False


def unfollow_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to unfollow %d users." % len(user_ids))
    for user_id in tqdm(user_ids):
        if not self.unfollow(user_id):
            delay.error_delay(self)
            broken_items.append(user_id)
    self.logger.info("DONE: Total unfollowed %d users. " %
                     self.total_unfollowed)
    return broken_items


def unfollow_everyone(self):
    your_following = self.get_user_following(self.user_id)
    self.unfollow_users(your_following)
