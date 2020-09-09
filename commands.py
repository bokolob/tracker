from settings import get_property,set_property

COMMANDS = {
    "auth": auth_user,
    "password": set_password,
    "inet":inet,
}

def run_cmd(phone, words):
    if len(words) == 0 or words[0] not in COMMANDS:
        raise ValueError("Bad command")

    if words[0] != "auth" and  words[0] != "password" and not check_admin_number(phone):
        return None

    return COMMANDS[words[0]](phone, words[1:])

def check_admin_number(phone):
    return phone in get_property("admin_numbers")

def inet(phone, args):
    if len(args) != 3:
        return "Wrong format, should be - apn login password"

    set_property("apn", args[0])
    set_property("login", args[1])
    set_property("password", args[1])

    return "Ok"

#TODO uniqueness
def add_admin(phone, args):
    get_property("admin_numbers").append(phone)

def set_password(phone, words):
    if len(args) > 0 :
        password = get_property("admin_password")

        #Пароль был задан, значит менять его может только админ
        if password is not None and password != "":
            if not check_admin_number(phone):
                return None

        set_property("admin_password", args[1])
        #TODO save()
        return "Password was set to " + args[1];

    return None

def auth_user(phone, args):
    if len(args) > 0 :
        password = get_property("admin_password")

        if password is None or password == "":
            return "Password must be defined before"

        if args[0] == get_property("admin_password"):
            add_admin(phone)
            return "Ok"

    return None


