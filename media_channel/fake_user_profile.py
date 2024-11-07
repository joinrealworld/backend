import random

def get_robohash_avatar():
    seed = random.randint(1, 10000)
    return f"https://robohash.org/{seed}?size=200x200"

# Example usage:
print(get_robohash_avatar())