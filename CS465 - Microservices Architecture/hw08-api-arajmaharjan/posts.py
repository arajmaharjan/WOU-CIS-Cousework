from datetime import datetime


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our new API
POSTS  = {
    "0": {
        "pet_id": 1,
        "petname": "kitty",
        "category": "cats",
        "breed": "ragdoll",
        "url": "http://www.example.com",
        "description": "ragdolls are pretty fiesty?",
        "timestamp": get_timestamp(),
    },
    "1": {
        "pet_id": 2,
        "petname": "doggy",
        "category": "dogs",
        "breed": "pomsky",
        "url": "http://www.example.com",
        "description": "pomsky are pretty subborn?",
        "timestamp": get_timestamp(),
    },
}


# Create a handler for our read (GET) posts
def read():
    """
    This function responds to a request for /api/posts
    with a list of posts
    :return:        sorted list of posts
    """
    # Create the list of posts from our data
    return [POSTS[key] for key in sorted(POSTS.keys())]