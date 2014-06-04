from __future__ import print_function
from twitter import *
from time import sleep
import sys
import argparse

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Follow all users in a twitter list.')
    parser.add_argument('token', type=str,
                        help='oauth token')
    parser.add_argument('token_secret', type=str,
                        help='oauth token secret')
    parser.add_argument('key', type=str,
                        help='oauth consumer key')
    parser.add_argument('secret', type=str,
                        help='oauth consumer secret')
    parser.add_argument('username', type=str,
                        help='owner of the list')
    parser.add_argument('list', type=str,
                        help='list slug')
                  
    args = parser.parse_args()      
    oauth_token = args.token
    oauth_secret = args.token_secret
    consumer_key = args.key
    consumer_secret = args.secret
    username = args.username
    list_name = args.list
    
    # Create Twitter instance
    t = Twitter(auth=OAuth(
                oauth_token, oauth_secret,
                consumer_key, consumer_secret))

    print('Retrieving users from @%s/%s...' % (username, list_name))
    
    # Retrieve all users in the list
    (cursor, members) = (-1, [])
    first = True
    while cursor != 0:
        response = t.lists.members(owner_screen_name=username, slug=list_name, cursor=cursor)
        cursor = int(response['next_cursor'])
        if not first:
            members += response['users']
        first = False

    print('%d users retrieved.' % len(members))

    # Follow members
    for member in members:
        print('Following %s...' % member['screen_name'])
        t.friendships.create(user_id=member['id'])
        sleep(3)
        
    print('Followings imported successfully.')
    return 0
		
if __name__ == '__main__':
    sys.exit(main())