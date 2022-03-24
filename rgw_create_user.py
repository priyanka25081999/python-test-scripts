# Script to create a normal user using rados admin API
# use of rgwadmin python library

from rgwadmin import RGWAdmin

# establish a connection
rgw = RGWAdmin(access_key='__YOUR_ACCESS_KEY__', secret_key='__YOUR_SECRET_KEY__', server='10.230.245.6:8000', secure=False, verify=False)

# create a user
rgw.create_user(
    uid='prog-user',
    display_name='program user')
print("User created successfully")

# get users
print("Users :\n", rgw.get_users())

# remove the user
rgw.remove_user(uid=user.get('user_id'))
print("\n", user_id, " : User removed successfully")
