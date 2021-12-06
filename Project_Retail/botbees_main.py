from configobj import ConfigObj
from jproperties import Properties
import urllib.request
from datetime import date
from pathlib import Path
import pathlib
import os
import uuid
import UI_Constants


home = str(Path.home())
# print(home)
p = pathlib.Path(home+UI_Constants.BOTBEES_HOME).mkdir(parents=True, exist_ok=True)

botbees_license = home+UI_Constants.BOTBEES_HOME+"/__license__.properties"
# botbees_php = home+UI_Constants.BOTBEES_HOME + "/php_date.properties"

file_exists = os.path.exists(botbees_license)
print(file_exists)


# Mac_id = hex(uuid.getnode())
# print(len(Mac_id))
# config = ConfigObj(botbees_license)
# config['Mac_id'] = Mac_id
# config.write()
configs = Properties()
with open(botbees_license, 'rb') as read_prop:
    configs.load(read_prop)
prop_view = configs.__getitem__('Mac_id')
date_pro = prop_view.__getitem__(0)
# print(date_pro,"-----")


url = UI_Constants.PHP_URL
date_php = urllib.request.urlopen(url).read().decode('UTF-8')
# print(date_php)


configs = Properties()
with open(botbees_license, 'rb') as read_prop:
    configs.load(read_prop)
prop_view = configs.__getitem__('sub_date')
exp_date = prop_view.__getitem__(0)
prop_view2 = configs.__getitem__('sub_duration')
sub_dur = prop_view.__getitem__(0)
Exp_year = exp_date.split('-')[0]
Exp_month = exp_date.split('-')[1]
Exp_dates = exp_date.split('-')[2]


php_year = date_php.split('-')[0]
php_month = date_php.split('-')[1]
php_dates = date_php.split('-')[2]


date_Exp = date(int(Exp_year),int(Exp_month),int(Exp_dates))
date_php = date(int(php_year), int(php_month), int(php_dates))
date_diff = date_Exp - date_php
date_days = date_diff.days
# print(date_days)

if len(date_pro) == 0:
    print("the mac id does not exist")
    Mac_id = hex(uuid.getnode())
    # print(len(Mac_id))
    config = ConfigObj(botbees_license)
    config['Mac_id'] = Mac_id
    config.write()
    print("the mac id is created")
    if str(date_days) <= '0':
        print("your subscription is expired please contact Weeroda")
    else:
        Mac_id3 = hex(uuid.getnode())
        if Mac_id == Mac_id3:
            print("your subscription is running")
            import Main_bot
            Main_bot.Exercrise_duty()
        else:
            print("your license has been expired please contact Weeroda")
else:
    print("the mac id is in")
    if str(date_days) <= '0':
        print("your subscription is expired please contact Weeroda")
    else:
        Mac_id = hex(uuid.getnode())
        if date_pro == Mac_id:
            print("your subscription is running")
            import Main_bot
            Main_bot.Exercrise_duty()
        else:
            print("your license has been expired please contact Weeroda")

# if str(date_days) <= '0' :
#     print("your subscription is expired please contact Weeroda")
# else:
#     Mac_id = hex(uuid.getnode())
#     # print(Mac_prop2)
#     print(Mac_id)
#     if date_pro == Mac_id:
#         print("your subscription is running")
#         # import Main_bot
#         # Main_bot.Exercrise_duty()
#     else:
#         print("please subscribe for this system")

