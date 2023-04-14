from models import user_dbs


user_collection = user_dbs['user']


def get_info(username):
    # return user info
    try:
        user_data = user_collection.find_one(
            {"_id": username}
        )
        if user_data:
            return user_data
    except Exception as e:
        print(f"Error/get_info: {e}")
    
    return False


def register(data):
    try:
        user_collection.insert_one(data)
        return True
    except Exception as e:
        print(f"Error/register: {e}")
        return False


def update_pass(username, new_pass):
    # update user's password
    try:
        user_collection.update_one(
            {"_id": username},
            {
                "$set": {"passwd": new_pass}
            }
        )
        return True
    except Exception as e:
        # TODO: log this
        print(f"Error/update_pass: {e}")
        return False


def update_form(username):
    try:
        user_collection.update_one(
            {"_id": username},
            {
                "$set": {"formFilled": True}
            }
        )
    except Exception as e:
        print(f"Error/update_form: {e}")
