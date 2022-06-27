from library import Multilogin, GoLogin
from config import MULTILOGIN_TOKEN, MULTILOGIN_PORT, GOLOGIN_TOKEN

multilogin = Multilogin(MULTILOGIN_TOKEN, MULTILOGIN_PORT)
multilogin_profiles = multilogin.get_profiles()

for profile in multilogin_profiles:
    multilogin_profile_data_dict = multilogin.get_profile_info(profile['uuid'])
    gologin = GoLogin(GOLOGIN_TOKEN)
    response = gologin.create_profile(multilogin_profile_data_dict)
    
    if response.status_code == 201:
        print('Profile', multilogin_profile_data_dict.get('name'), 'successfully created')
    else:
        print('Profile', multilogin_profile_data_dict.get('name'), 'Error!')

print('Migration process completed')
print(response)
