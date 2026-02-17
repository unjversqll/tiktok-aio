import requests as req
import json as js
import os as o
import re
import time as t
import threading as threads
from urllib.parse import urlencode as encoded
import SignerPy as SP
import random as rnd
from datetime import datetime
from colorama import *
from pystyle import *

init(autoreset=True)

class Utils:
    def username_generator():
        charz = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        length = rnd.randint(3, 6)
        username = ''
        for i in range(length):
            username += rnd.choice(charz)
        return username

    def auto_make_files():
        success = o.path.exists('success.txt')
        if not success:
            o.mkdir('success')

        failed = o.path.exists('failed.txt')
        if not failed:
            o.mkdir('failed')

class TikTok:
    def username_checker():
        pass

    def scrape_info():
        uzr = Write.Input("\n[>] enter tiktok username you wish to scrape info for >> ", Colors.blue_to_purple)
        tiktok = f'https://www.tiktok.com/@{uzr}'

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }

        try:
            r = req.get(tiktok, headers=headers)
            if r.status_code == 404:
                Write.Print(f"\n[!] user @{uzr} not found", Colors.red)
                input("\n[!] press enter to continue...")
                return

            match = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', r.text)
            if not match:
                Write.Print(f"\n[!] could not find user data in HTML (maybe you are rate limited?)", Colors.red)
                input("\n[!] press enter to continue...")
                return

            data = js.loads(match.group(1))
            
            default_scope = data.get('__DEFAULT_SCOPE__', {})
            
            user_detail = None
            if 'webapp.user-detail' in default_scope:
                user_detail = default_scope['webapp.user-detail']
            elif 'webapp.app-context' in default_scope:
                user_detail = default_scope['webapp.app-context']
            elif 'webapp.user-detail' in default_scope:
                user_detail = default_scope['webapp.user-detail']
            
            if not user_detail:
                for key, value in default_scope.items():
                    if 'user' in key.lower() and isinstance(value, dict):
                        user_detail = value
                        break
            
            if not user_detail:
                Write.Print(f"\n[!] could not find user data structure for @{uzr}", Colors.red)
                print(f"Available keys: {list(default_scope.keys())}")
                input("\n[!] press enter to continue...")
                return

            user_info = user_detail.get('userInfo', {})
            if not user_info:
                user_info = {'user': user_detail.get('user', {}), 'stats': user_detail.get('stats', {})}

            user = user_info.get('user', {})
            stats = user_info.get('stats', {})

            if not user:
                Write.Print(f"\n[!] could not extract user details for @{uzr}", Colors.red)
                print(f"User detail structure: {user_detail}")
                input("\n[!] press enter to continue...")
                return

            username = user.get('uniqueId') or user.get('unique_id')
            display_name = user.get('nickname') or user.get('nickName')
            user_id = user.get('id') or user.get('uid')
            sec_uid = user.get('secUid') or user.get('sec_uid')
            
            followers = stats.get('followerCount') or stats.get('follower_count', 0)
            following = stats.get('followingCount') or stats.get('following_count', 0)
            likes = stats.get('heartCount') or stats.get('heart_count', 0)
            videos = stats.get('videoCount') or stats.get('video_count', 0)
            
            verified = user.get('verified', False)
            
            create_time_raw = user.get('createTime') or user.get('create_time', '0')
            try:
                create_time_int = int(create_time_raw)
                if create_time_int == 0 and user_id:
                    create_time_int = int(user_id) >> 32
                
                if create_time_int > 0:
                    dt_object = datetime.fromtimestamp(create_time_int)
                    month_name = dt_object.strftime('%B').lower()
                    create_date = f"{dt_object.day} {month_name} {dt_object.year}"
                else:
                    create_date = "N/A"
            except:
                create_date = "N/A"

            print(f"{Fore.CYAN}Username        >> {username}")
            print(f"{Fore.CYAN}Display Name    >> {display_name}")
            print(f"{Fore.CYAN}User ID         >> {user_id}")
            print(f"{Fore.CYAN}Sec UID         >> {sec_uid}")
            print(f"{Fore.CYAN}Followers       >> {followers:,}")
            print(f"{Fore.CYAN}Following       >> {following:,}")
            print(f"{Fore.CYAN}Total Likes     >> {likes:,}")
            print(f"{Fore.CYAN}Videos Created  >> {videos:,}")
            print(f"{Fore.CYAN}Verified        >> {'Yes' if verified else 'No'}")
            print(f"{Fore.CYAN}Account Created >> {create_date}")

            input(f"\n{Fore.YELLOW}[!] press enter to return to menu...")
            main.main()

        except Exception as e:
            Write.Print(f"\n[!] error occurred: {e}", Colors.red)
            t.sleep(3)
        

class main:
    def main():
        o.system('cls')

        o.system('title tiktok aio tool made by unjversql / Lucas')

        main_bnr = r"""
██╗   ██╗███╗   ██╗     ██╗██╗   ██╗███████╗██████╗ ███████╗ ██████╗ ██╗     
██║   ██║████╗  ██║     ██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔═══██╗██║     
██║   ██║██╔██╗ ██║     ██║██║   ██║█████╗  ██████╔╝███████╗██║   ██║██║     
██║   ██║██║╚██╗██║██   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██║▄▄ ██║██║     
╚██████╔╝██║ ╚████║╚█████╔╝ ╚████╔╝ ███████╗██║  ██║███████║╚██████╔╝███████╗
 ╚═════╝ ╚═╝  ╚═══╝ ╚════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝ ╚══════╝
                    made by unjversql / Lucas"""

        print(Colorate.Diagonal(Colors.purple_to_blue, main_bnr, 1))

        options = Write.Print(
            """
            [1.] > TikTok Username Gen + Checker (maybe next update xd)
            [2.] > TikTok Username Info Scrapper
            [3.] > Exit
            """,
            Colors.red_to_yellow,
        )
        
        choice = Write.Input("\n[>] choice >> ", Colors.green_to_cyan)

        if choice == '1':
            TikTok.username_checker()
        elif choice == '2':
            TikTok.scrape_info()
        elif choice == '3':
            Write.Print('exiting come back soon ig?', Colors.red)
            t.sleep(5)
            exit()
        else:
            Write.Print('invalid choice', Colors.red)
            t.sleep(3)
            main.main()

if __name__ == '__main__':
    main.main()