import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

class script(object):
    START_TXT = environ.get("START_TXT", '''<b>Hello 👋🏻 {} ♥️,\nI'm an Star Movies Tamil's Official <a href=https://t.me/Star_Moviess_Bot><b>Star Movies Bot</b></a> (Movie Search Bot) Maintained by <a href=https://t.me/Star_Moviess_Tamil><b></b>Star Movies Tamil</a>. We are Providing All Languages. 🌍 Languages :- Tamil, Telugu, Hindi, Malayalam, Kannada, English and Extra... Keep me Join to Our Official Channel to Receive 🎥 Movie Updates in <a href=https://t.me/Star_Moviess_Tamil><b></b>Star Movies Tamil</a>. And Also Keep me Join to Our Official Bot Channel to Receive 🤖 Bot Updates in <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a>. Check "😁 About" Button.</b>''')
    HELP_TXT = """<b>Hello 👋🏻 {} ♥️,
I have that Features.
Create One Link This :-
» I will Create For One Bot You. But Paid
» Contact Me <a href=https://t.me/TG_Karthik><b>Karthik</b></a></b>"""
    ABOUT_TXT = """<b><i>🤖 My Name :- <a href=https://t.me/Star_Moviess_Bot><b>Star Movies Bot</b></a>\n
🧑🏻‍💻 Developer :- <a href=https://t.me/TG_Karthik><b>Karthik</b></a>\n
📝 Language :- Python3\n
📚 Framework :- Pyrogram\n
📡 Hosted on :- VPS\n
🎥 Movie Updates :- <a href=https://t.me/Star_Moviess_Tamil><b></b>Star Movies Tamil</a>\n
🤖 Bot Channel :- <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a>\n
🌟 Version :- 4.4</b></i>"""
    SOURCE_TXT = """<b>Create One Like This :-</b>
<b>» I will Create One Bot For You. But Paid
» Contact Me</b> <a href=https://t.me/TG_Karthik><b>Karthik</b></a>"""

    STATUS_TXT = """<b>👩🏻‍💻 Total Users :-</b> <code>{}</code> <b>Users</b>\n
<b>💾 Used Storage :-</b> <code>{}</code>\n
<b>🆓 Free Storage :-</b> <code>{}</code>"""

    LOG_TEXT_P = """<b>#New_User</b>
    
<b>᚛› ID ⪼ <code>{}</code></b>
<b>᚛› Name ⪼ {}</b>
<b>᚛› From Bot ⪼ <a href=https://t.me/Star_Moviess_Bot>Star Movies Bot</a></b>
"""
