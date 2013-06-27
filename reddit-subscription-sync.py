"""

Reddit Subscription Sync v1.0 by /u/james-turner

"A script to sync one account's subscriptions to another"

https://github.com/jamesturner/reddit-subscription-sync
http://jamesturner.im

"""

import praw

user_agent = "Reddit Subscription Sync - A script to sync one account's subscriptions to another v1.0 by /u/james-turner"
r = praw.Reddit(user_agent=user_agent)


class User(object):
    # Static var that holds the username of the user currently logged in.
    logged_in_user = ""

    username = ""
    password = ""
    authenticated = False
    reddit = None
    subreddits = []

    def __init__(self, reddit):
        self.reddit = reddit

    def login(self):
        self.username = raw_input("Username: ")
        self.password = raw_input("Password: ")

        # Tries to sign into the account and catches any invalid username/password exceptions.
        try:
            self.reddit.login(username=self.username, password=self.password)
        except praw.errors.InvalidUserPass:
            print "Invalid username or password."
            print
            return False

        self.authenticated = True
        User.logged_in_user = self.username
        return True

    # Creates and stores an array of subreddits that the user is subscribed to after.
    def requestSubreddits(self):
        subreddits = r.get_my_subreddits(limit="none")
        subreddit_list = []

        for sub in subreddits:
            subreddit_list.append(sub.display_name)
        self.subreddits = subreddit_list

    # Returns an array of of subreddits that the user is subscribed to after.
    def getSubreddits(self):
        if not self.subreddits:
            self.requestSubreddits()
        return self.subreddits

input_user = User(r)
output_user = User(r)

# Log into the account to sync the subscriptions from.
while input_user.authenticated is False:
    print "Log in to the account you wish to sync the subreddits from."
    input_user.login()

input_user.getSubreddits()

print

# Log into the account to sync the subscriptions to.
while output_user.authenticated is False:
    print "Log in to the account you wish to sync the subreddits to."
    output_user.login()

output_user.getSubreddits()

print

# Prompt whether to unsubscribe from any subs already subscribed to on the output account.
remove_previous = raw_input("Remove any previous subscriptions on the output account? (Y/N): ").lower()
remove_previous = True if remove_previous in ["y", "yes"] else False

print "Preparing to sync subscriptions from /u/{0} to /u/{1}...".format(input_user.username, output_user.username)

subscribe_to = input_user.getSubreddits()[:]
unsubscribe_from = output_user.getSubreddits()[:]

# Remove any subreddits that exist in both selections.
for subreddit in output_user.getSubreddits():
    if subreddit in subscribe_to:
        unsubscribe_from.remove(subreddit)
        subscribe_to.remove(subreddit)

unsub_total = len(unsubscribe_from)
sub_total = len(subscribe_to)

# Remove any pre-existing subscriptions on the account we're transferring to.
if remove_previous:
    for i in range(0, len(unsubscribe_from)):
        subreddit = unsubscribe_from[i]
        print "Unsubscribing from /r/{0} ({1} of {2})".format(subreddit, i + 1, unsub_total)
        r.unsubscribe(subreddit)

# Subscribe to the new subreddits.
for i in range(0, len(subscribe_to)):
    subreddit = subscribe_to[i]
    print "Subscribing to /r/{0} ({1} of {2})".format(subreddit, i + 1, sub_total)
    r.subscribe(subreddit)

print "Sync completed."
