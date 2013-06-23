"""

Reddit Subscription Sync v1.0 by /u/james-turner

"A script to sync one account's subscriptions to another"

https://github.com/jamesturner/reddit-subscription-sync
http://jamesturner.im

"""

import praw

user_agent = "Reddit Subscription Sync - A script to sync one account's subscriptions to another v1.0 by /u/james-turner"
r = praw.Reddit(user_agent=user_agent)


def login(username, password):
    r.login(username=username, password=password)


# Return a list of the user's subscriptions in a list
def getSubreddits():
    subreddits = r.get_my_subreddits(limit="none")
    subreddit_list = []

    for sub in subreddits:
        subreddit_list.append(sub.display_name)

    return subreddit_list

# Get the username and password for the account to transfer from.
input_username = raw_input("User to sync subscriptions from: ")
input_password = raw_input("Password: ")

# Get the username and password for the account to transfer to.
output_username = raw_input("User to sync subscriptions to: ")
output_password = raw_input("Password: ")

# Prompt whether to unsubscribe from any subs already subscribed to on the output account.
remove_previous = raw_input("Remove any previous subscriptions on the output account? (Y/N): ").lower()
remove_previous = True if remove_previous in ["y", "yes"] else False

print "Preparing to sync subscriptions from /u/{0} to /u/{1}...".format(input_username, output_username)

# Log into the account to transfer the subscriptions from.
login(input_username, input_password)

# Get the subscribed subreddits (the ones we're transferring).
new_subs = getSubreddits()

# Log into the account we're going to transfer the subscriptions to.
login(output_username, output_password)

# Get the subreddits that are already subscribed to.
old_subs = getSubreddits()
subs_to_unsub = old_subs[:]

# Remove any subreddits that exist in both selections.
for subreddit in old_subs:
    if subreddit in new_subs:
        subs_to_unsub.remove(subreddit)
        new_subs.remove(subreddit)

unsub_total = len(subs_to_unsub)
sub_total = len(new_subs)

# Remove any pre-existing subscriptions on the account we're transferring to.
if remove_previous:
    for i in range(0, len(subs_to_unsub)):
        subreddit = subs_to_unsub[i]
        print "Unsubscribing from /r/{0} ({1} of {2})".format(subreddit, i + 1, unsub_total)
        r.unsubscribe(subreddit)

# Subscribe to the new subreddits.
for i in range(0, len(new_subs)):
    subreddit = new_subs[i]
    print "Subscribing to /r/{0} ({1} of {2})".format(subreddit, i + 1, sub_total)
    r.subscribe(subreddit)

print "Sync completed."
