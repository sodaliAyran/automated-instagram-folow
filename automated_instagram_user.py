from api.api import API

class AutomatedInstagramUser:
    __user_id = None
    __instagram_api =None
    def __init__(self):
        self.__instagram_api = API()
        
    def login(self, username, password):
        if self.__instagram_api.login(username=username, password=password):
            self.__user_id = self.get_user_id_from_username(username)
                
    def __initialize_with_user(self, user_id):
        return user_id if user_id else self.__user_id
        
    def get_user_id_from_username(self, username):
        self.__instagram_api.searchUsername(username)
        return self.__instagram_api.LastJson["user"]["pk"]
    
    def logout(self):
        self.__instagram_api.logout()
        
    def get_followers(self, user_id=None):
        user_id = self.__initialize_with_user(user_id)
        return self.__instagram_api.getTotalFollowers(user_id)

    def get_followings(self, user_id=None):
        user_id = self.__initialize_with_user(user_id)
        return self.__instagram_api.getTotalFollowings(user_id)

    def get_difference_between_followings_and_followers(self, user_id=None):
        user_id = self.__initialize_with_user(user_id)
        followers = [user["username"] for user in self.get_followers(user_id=user_id)]
        followings = [user["username"] for user in self.get_followings(user_id=user_id)]
        return list(set(followings) - set(followers))
        
    def unfollow(self, username):
        user_id = self.get_user_id_from_username(username)
        return self.__instagram_api.unfollow(user_id)
    
    def follow(self, username):
        user_id = self.get_user_id_from_username(username)
        return self.__instagram_api.follow(user_id)
