import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(0, num_users):
            self.add_user(f"User {i+1}")

        # Create friendships
        possible_friendships = []

        # all unique friendship pairs (lower id, higher)
        for user_id in self.users:
            for friend_id in range(user_id+1, self.last_id+1):
                possible_friendships.append((user_id, friend_id))

        random.shuffle(possible_friendships)

        # ensure average number of friends is correct
        for i in range(num_users * avg_friendships  // 2):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

            # alternate friendship generation:
            # trades guaranteed O(n^2) for veeeery small chance of infinite loop
            # produces essentially the same stats below as standard algo

            # friend1 = random.randint(1, num_users)
            # friend2 = random.randint(1, num_users)
            # while friend1 in self.friendships[friend2] or friend1 == friend2:
            #     friend1 = random.randint(0, num_users-1)
            #     friend2 = random.randint(0, num_users-1)
            # self.add_friendship(friend1, friend2)
            


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        qq = Queue()
        qq.enqueue([user_id])
        # get neighbors is self.friendships[id]
        while qq.size() > 0:
            path = qq.dequeue()
            if path[-1] not in visited:
                visited[path[-1]] = path
                for next_friend in self.friendships[path[-1]]:
                    new_path = path + [next_friend]
                    qq.enqueue(new_path)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    # print(sg.friendships)
    # percentage of users in a particular user's extended social network?
    extended_network_size = []
    # average degree of separation between a user and those in extended network?
    avg_network_length = []
    for i in range(1, 1001):
        connections = sg.get_all_social_paths(i)
        extended_network_size.append(len(connections))
        my_lengths = []
        for j in connections:
            my_lengths.append(len(connections[j]))
        my_average = sum(my_lengths) / len(my_lengths)
        avg_network_length.append(my_average)

    print("average percentage of users in a particular user's extended social network:")
    ENS_avg = sum(extended_network_size) / len(extended_network_size)
    ENS_percent = ENS_avg / 1000
    print(ENS_percent, "\n")
    print("average degree of separation between a user and those in extended network")
    ANL_avg = sum(avg_network_length) / len(avg_network_length)
    print(ANL_avg)
