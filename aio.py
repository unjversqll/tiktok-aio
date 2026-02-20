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
import uuid
import json
import base64

init(autoreset=True)

class Utils:
    def TikTok_username_generator():
        charz = 'abcdefghijklmnopqrstuvwxyz'
        length = rnd.randint(4, 6)
        username = ''
        for i in range(length):
            username += rnd.choice(charz)
        return username

    def auto_make_files():
        if not o.path.exists('tiktok'):
            o.mkdir('tiktok')
        
        success_path = o.path.join('tiktok/usernames', 'success.txt')
        failed_path = o.path.join('tiktok/usernames', 'failed.txt')
        
        if not o.path.exists(success_path):
            with open(success_path, 'w') as f:
                f.write('')
        
        if not o.path.exists(failed_path):
            with open(failed_path, 'w') as f:
                f.write('')

class TikTok:
    def username_checker():
        Utils.auto_make_files()
        

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

    def extract_vid_data():
        pass
        
class Discord:
    def files():
        if not o.path.exists('discord'):
            o.mkdir('discord')

        if not o.path.exists('discord/nitro codes'):
            o.mkdir('discord/nitro codes')
        
        success_path = o.path.join('discord/nitro codes', 'success.txt')
        failed_path = o.path.join('discord/nitro codes', 'failed.txt')
        
        if not o.path.exists(success_path):
            with open(success_path, 'w') as f:
                f.write('')
        
        if not o.path.exists(failed_path):
            with open(failed_path, 'w') as f:
                f.write('')

    def nitro_generator():
        charz = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        code = ""
        length = 13 #this may be wrong change it if yk the correct length bc idk it im 90% sure its this tho

        for _ in range(length):
            code += rnd.choice(charz)
        
        return code
        
    def Checker():
        thread_count = 25
        generated_count = 0
        success_count = 0
        failed_count = 0
        
        Discord.files()
        
        success_path = o.path.join('discord/nitro codes', 'success.txt')
        failed_path = o.path.join('discord/nitro codes', 'failed.txt')
        
        try:
            with open(success_path, "r") as f:
                content = f.read().strip()
                success_count = len(content.split('\n')) if content else 0
        except:
            success_count = 0
            
        try:
            with open(failed_path, "r") as f:
                content = f.read().strip()
                failed_count = len(content.split('\n')) if content else 0
        except:
            failed_count = 0

        generated_count = success_count + failed_count

        def check_nitro():
            nonlocal generated_count, success_count, failed_count
            code = Discord.nitro_generator()
            nitro = f'https://discord.gift/{code}'
            generated_count += 1

            base_url = "https://discordapp.com/api/v9/entitlements/gift-codes/" + nitro + "?with_application=false&with_subscription_plan=true"
            
            try:
                r = req.get(base_url, timeout=5)
                if r.status_code == 200:
                    success_count += 1
                    with open(success_path, "a") as success_file:
                        success_file.write(nitro + "\n")
                else:
                    failed_count += 1
                    with open(failed_path, "a") as failed_file:
                        failed_file.write(nitro + "\n")
            except:
                failed_count += 1
                with open(failed_path, "a") as failed_file:
                    failed_file.write(nitro + "\n")

        o.system('cls')

        discord_bnr = r"""
████████▄   ▄█     ▄████████  ▄████████  ▄██████▄     ▄████████ ████████▄  
███   ▀███ ███    ███    ███ ███    ███ ███    ███   ███    ███ ███   ▀███ 
███    ███ ███▌   ███    █▀  ███    █▀  ███    ███   ███    ███ ███    ███ 
███    ███ ███▌   ███        ███        ███    ███  ▄███▄▄▄▄██▀ ███    ███ 
███    ███ ███▌ ▀███████████ ███        ███    ███ ▀▀███▀▀▀▀▀   ███    ███ 
███    ███ ███           ███ ███    █▄  ███    ███ ▀███████████ ███    ███ 
███   ▄███ ███     ▄█    ███ ███    ███ ███    ███   ███    ███ ███   ▄███ 
████████▀  █▀    ▄████████▀  ████████▀   ▀██████▀    ███    ███ ████████▀  
                                                     ███    ███            
        """

        print(Colorate.Horizontal(Colors.red_to_blue, discord_bnr, 2))

        while True:
            thread_list = []
            for _ in range(thread_count):
                thread = threads.Thread(target=check_nitro)
                thread_list.append(thread)
                thread.start()

            for thread in thread_list:
                thread.join()

            print(f" {Fore.CYAN} \rgenerated: {generated_count} {Fore.RESET} {Fore.YELLOW} | {Fore.RESET} {Fore.GREEN} success: {success_count} {Fore.RESET} {Fore.YELLOW} | {Fore.RESET} {Fore.RED} failed: {failed_count} {Fore.RESET} {Fore.YELLOW} | {Fore.RESET} {Fore.MAGENTA} made by unjversql / Lucas {Fore.RESET} ", end='', flush=True)

    def username_generator():
        charz = 'abcdefghijklmnopqrstuvwxyz'
        length = rnd.randint(3, 6)
        username = ''
        for i in range(length):
            username += rnd.choice(charz)
        return username     

    def x_super_properties():
        props = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-GB",
            "has_client_mods": False,
            "browser_user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "browser_version": "120.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": rnd.randint(400_000, 500_000),
            "client_event_source": None,
            "client_launch_id": str(uuid.uuid4()),
            "client_app_state": "unfocused"
        }
        compact = json.dumps(props, separators=(",", ":")).encode("utf-8")
        return base64.b64encode(compact).decode("utf-8")

    def x_fingerprint():
        x_super_properties = Discord.x_super_properties()

        url = "https://discord.com/api/v9/experiments?with_guild_experiments=true"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "discord.com",
            "Referer": "https://discord.com/register",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
            "X-Context-Properties": "eyJsb2NhdGlvbiI6IlJlZ2lzdGVyIn0=",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-GB",
            "X-Discord-Timezone": "Europe/Amsterdam",
            "X-Super-Properties": x_super_properties
        }
        resp = req.get(url, headers=headers, timeout=10)
        return resp.json().get("fingerprint", "")

    def username_files():
        if not o.path.exists('discord'):
            o.mkdir('discord')

        if not o.path.exists('discord/usernames'):
            o.mkdir('discord/usernames')
        
        success_path = o.path.join('discord/usernames', 'success.txt')
        failed_path = o.path.join('discord/usernames', 'failed.txt')
        
        if not o.path.exists(success_path):
            with open(success_path, 'w') as f:
                f.write('')
        
        if not o.path.exists(failed_path):
            with open(failed_path, 'w') as f:
                f.write('')

    def check_users(uzr, headers):
        r = req.get(f"https://discord.com/api/v9/unique-username/username-suggestions-unauthed?global_name={uzr}", headers=headers)
        print(r.json())

        response_data = r.json()
        response_username = response_data.get('username', '')

        if response_username == uzr:
            print(f"{Fore.GREEN}username > {uzr} available (saved to success.txt){Fore.RESET}")
            with open("discord/usernames/success.txt", "a") as f:
                f.write(f"{uzr}\n")
        else:
            print(f"{Fore.RED}username > {uzr} taken (saved to failed.txt){Fore.RESET}")
            with open("discord/usernames/failed.txt", "a") as f:
                f.write(f"{uzr}\n")

    def check_users2():
        files = Discord.username_files()

        o.system("cls")

        bnr = r"""
████████▄   ▄█     ▄████████  ▄████████  ▄██████▄     ▄████████ ████████▄  
███   ▀███ ███    ███    ███ ███    ███ ███    ███   ███    ███ ███   ▀███ 
███    ███ ███▌   ███    █▀  ███    █▀  ███    ███   ███    ███ ███    ███ 
███    ███ ███▌   ███        ███        ███    ███  ▄███▄▄▄▄██▀ ███    ███ 
███    ███ ███           ███ ███    █▄  ███    ███ ▀███████████ ███    ███ 
███   ▄███ ███     ▄█    ███ ███    ███ ███    ███   ███    ███ ███   ▄███ 
████████▀  █▀    ▄████████▀  ████████▀   ▀██████▀    ███    ███ ████████▀  
                                                     ███    ███        
        """

        print(Colorate.Horizontal(Colors.blue_to_cyan, bnr, 2))

        while True:
            uzr = Discord.username_generator()
            fingerprint = Discord.x_fingerprint()

            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Connection": "keep-alive",
                "Host": "discord.com",
                "Referer": "https://discord.com/register",
                "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
                "X-Context-Properties": "eyJsb2NhdGlvbiI6IlJlZ2lzdGVyIn0=",
                "X-Debug-Options": "bugReporterEnabled",
                "X-Discord-Locale": "en-GB",
                "X-Discord-Timezone": "Europe/Amsterdam",
                "X-Super-Properties": Discord.x_super_properties(),
                "X-Fingerprint": fingerprint
            }

            try:
                r = req.get(f"https://discord.com/api/v9/unique-username/username-suggestions-unauthed?global_name={uzr}", headers=headers, timeout=10)
                
                if r.status_code == 429:
                    retry_after = r.json().get('retry_after', 5)
                    print(f"{Fore.YELLOW}rate limited waiting {retry_after:.1f} seconds...{Fore.RESET}")
                    t.sleep(retry_after)
                    continue
                
                response_data = r.json()
                response_username = response_data.get('username', '')

                if response_username == uzr:
                    print(f"{Fore.GREEN}username > {uzr} available (saved to success.txt){Fore.RESET}")
                    with open("discord/usernames/success.txt", "a") as f:
                        f.write(f"{uzr}\n")
                else:
                    print(f"{Fore.RED}username > {uzr} taken (saved to failed.txt){Fore.RESET}")
                    with open("discord/usernames/failed.txt", "a") as f:
                        f.write(f"{uzr}\n")
                        
            except Exception as e:
                print(f"{Fore.RED}Error checking {uzr}: {e}{Fore.RESET}")
                with open("discord/usernames/failed.txt", "a") as f:
                    f.write(f"{uzr}\n")
            
            t.sleep(1.35)

class main:
    def main():
        o.system('cls')

        o.system('title aio tool made by unjversql / Lucas')

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
            [3.] > TikTok Video Data Extractor (coming soon myb next update)
            [4.] > Discord Nitro Generator + Checker
            [5.] > Discord Username Gen + Checker
            [6.] > Exit
            """,
            Colors.red_to_yellow,
        )
        
        choice = Write.Input("\n[>] choice >> ", Colors.green_to_cyan)

        if choice == '1':
            TikTok.username_checker()
        elif choice == '2':
            TikTok.scrape_info()
        elif choice == '3':
            TikTok.extract_vid_data()
        elif choice == '4':
            Discord.Checker()
        elif choice == '5':
            Discord.check_users2()
        elif choice == '6':
            Write.Print('exiting come back soon ig?', Colors.red)
            t.sleep(5)
            exit()
        else:
            Write.Print('invalid choice returning to main menu', Colors.red)
            t.sleep(3)
            main.main()

if __name__ == '__main__':
    main.main()
