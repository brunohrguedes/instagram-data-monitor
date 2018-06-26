class Actor(object):
    """Define an actor of interest"""

    def __init__(self, name, fullname, posts=0, followers=0, following=0):
        self.name = name
        self.fullname = fullname
        self.posts = posts
        self.followers = followers
        self.following = following

    def __repr__(self):
        return (self.name, self.posts, self.followers, self.following, self.fullname)

    def  __str__(self):
        return str((self.name, self.posts, self.followers, self.following, self.fullname))
