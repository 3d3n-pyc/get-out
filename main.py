import os
import ctypes
import json
import requests
import random
import asyncio

import discord
import discord.ext.commands as commands


if os.name == 'nt': ctypes.windll.kernel32.SetConsoleTitleW('Get out !') 


class colors:
    light_red = '\033[91m'
    light_green = '\033[92m'
    light_gray = '\033[37m'
    tan = '\033[93m'
    red = '\033[31m'
    orange = '\033[33m'
    white = '\033[97m'
    reset = '\033[0m'


class client(commands.Bot):
    
    def __init__(self, config:dict):
        super().__init__(
            command_prefix='dontchangeit',
            intents = discord.Intents.all(),
            application_id = config['login']["app_id"]
        )
        self.config = config
        self.space = ' ' * 10
    
    async def setup_hook(self):
        await self.tree.sync()

    async def ban_member(self, member:discord.Member, sentance:str, amount:dict):
        try:
            await member.ban(reason=sentance)
            print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) Banned {colors.light_gray}{member.name}{colors.reset}')
            amount['banned'] += 1
        except discord.errors.Forbidden:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Missing permissions to ban {colors.light_gray}{member.name}{colors.reset}')
            amount['failed'] += 1
        except discord.errors.HTTPException:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Rate limited, waiting for {colors.light_gray}{self.config["settings"]["timePerBan"]}{colors.white} seconds{colors.reset}')
            await asyncio.sleep(10)
            await self.ban_member(member, sentance, amount)
    
    async def on_ready(self):
        print(f'\n{ui.space}{colors.white}( {colors.light_green}⚡{colors.white}) Bot is ready{colors.reset}')
        
        guid:int = self.config['settings']['guildID']
        guild = self.get_guild(guid)
        
        if not guild:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Invalid guild with id {colors.light_gray}{guid}{colors.reset}')
            await self.close()
        
        print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) Guild found named {colors.light_gray}{guild.name}{colors.reset}')
        
        sentances = [
            'Get better',
            'Permision denied',
            'You are banned',
            'You are not allowed here',
            'You are not welcome here',
            'Get out',
            'We do not want you here',
            'Error 404',
            'Don\'t come back',
            'Return to sender'
        ]
        
        amount = {
            'banned': 0,
            'failed': 0
        }
        
        for member in guild.members:
            if member.id == self.user.id:
                continue
            
            sentance = random.choice(sentances)
            await self.ban_member(member, sentance, amount)
            await asyncio.sleep(self.config['settings']['timePerBan'])

        banned = amount['banned']
        total = banned + amount['failed']
        print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) Banned {colors.light_red}{banned} {colors.white}/ {colors.light_red}{total} {colors.white}members{colors.reset}')
        await self.close()


class utils:
    def get_config() -> dict:
        with open('config.json', 'r') as file:
            return json.load(file)
    
    def set_key(key:str, value:str) -> None:
        with open('config.json', 'r') as file:
            data = json.load(file)
        
        data[key] = value
        
        with open('config.json', 'w') as file:
            json.dump(data, file, indent=4)


class requestsManager:
    def botTokenValid(token:str, id:int):
        headers = {
            "Authorization": f"Bot {token}"
        }
        
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        
        if response.status_code == 200:
            if response.json()['id'] == id:
                return True
            else:
                return 'id_mismatch'
        
        return False
    
    def guildExists(token:str, id:int):
        headers = {
            'Authorization': f'Bot {token}'
        }
        
        response = requests.get(f'https://discord.com/api/v9/guilds/{id}', headers=headers)
        
        if response.status_code == 200:
            return True
        
        return False


class uiClass:
    def __init__(self):
        self.space = ' ' * 10
    
    
    def base(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print('\n' +
            f'\n{self.space}{colors.light_red}┏┓┏┓┏┳┓  ┏┓┳┳┏┳┓  ╻{colors.reset}',
            f'\n{self.space}{colors.light_red}┃┓┣  ┃   ┃┃┃┃ ┃   ┃{colors.reset}',
            f'\n{self.space}{colors.light_red}┗┛┗┛ ┻   ┗┛┗┛ ┻   •{colors.reset}',
            f'\n',
            f'\n{self.space}{colors.light_red}⚡{colors.white}Developed by {colors.light_red}@3D3N{colors.reset}',
            f'\n{self.space}{colors.light_red}⚡{colors.white}Version: {colors.light_red}1.0{colors.reset}'
        )
        
        
    def menu(self):
        self.base()
        return input(
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}1{colors.white}) Start bot'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}2{colors.white}) Configuration'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}3{colors.white}) Exit'
            f'\n{self.space}{colors.light_red}└─ • {colors.white}'
        )
    
    
    def configuration(self):
        self.base()
        return input(
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}1{colors.white}) Change login'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}2{colors.white}) Change settings'
            f'\n{self.space}{colors.light_red}• {colors.white}({colors.light_red}3{colors.white}) Back'
            f'\n{self.space}{colors.light_red}└─ • {colors.white}'
        )
    
    
    def login(self):
        self.base()
        
        while True:
            while True:
                app_id = input(
                    f'\n{self.space}{colors.light_red}• {colors.white}Application ID: '
                )
                
                if app_id == '':
                    return

                try:
                    int(app_id)
                    break
                except ValueError:
                    print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Invalid input{colors.reset}')
            
            token = input(
                f'\n{self.space}{colors.light_red}• {colors.white}Token: '
            )
            
            if token == '':
                return
            
            response = requestsManager.botTokenValid(token, app_id)
            
            if response == True:
                break
            elif response == 'id_mismatch':
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) ID mismatch{colors.reset}')
            else:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Invalid token{colors.reset}')
        
        utils.set_key('login', {
            'app_id': int(app_id),
            'token': token
        })
        
        print(f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) Token and ID has been set{colors.reset}')
        
        input(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) Press Enter To Return To Menu:{colors.reset}')
    
    
    def settings(self):
        self.base()
        
        while True:
            timePerBan = input(
                f'\n{self.space}{colors.light_red}• {colors.white}Time per ban: '
            )
            
            if timePerBan == '':
                return
            
            try:
                timePerBan = float(timePerBan)
                break
            except ValueError:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Invalid input{colors.reset}')

        while True:
            guildID = input(
                f'\n{self.space}{colors.light_red}• {colors.white}Guild ID: '
            )
            
            if guildID == '':
                return
            
            try:
                guildID = int(guildID)
                break
            except ValueError:
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Invalid input{colors.reset}')
            
            if not requestsManager.guildExists(utils.get_config()['login']['token'], guildID):
                print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Guild not found{colors.reset}')
                continue
            
            break
        
        utils.set_key('settings', {
            'timePerBan': timePerBan,
            'guildID': guildID
        })
        
        input(
            f'\n{self.space}{colors.white}( {colors.light_green}⚡{colors.white}) Settings has been set{colors.reset}'
            f'\n'
            f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) Press Enter To Return To Menu:{colors.reset}'
        )
    
      
    def start(self):
        self.base()
        
        print(f'\n{self.space}{colors.white}( {colors.light_red}⚡{colors.white}) Starting bot{colors.reset}')
        config = utils.get_config()
        
        try:
            bot = client(config); bot.run(config['login']["token"], log_handler=None)
        except discord.errors.LoginFailure:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Invalid token{colors.reset}')
        except discord.errors.HTTPException:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) HTTP Exception{colors.reset}')
        except discord.errors.GatewayNotFound:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Gateway not found{colors.reset}')
        except discord.errors.ConnectionClosed:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Connection closed{colors.reset}')
        except discord.errors.PrivilegedIntentsRequired:
            print(f'\n{self.space}{colors.white}( {colors.red}⚡{colors.white}) Privileged intents are required for the bot to function properly{colors.reset}')
        
        input(f'\n{self.space}{colors.white}( {colors.tan}⚡{colors.white}) Press Enter To Return To Menu:{colors.reset}')

ui = uiClass()


while True:
    response = ui.menu()
    
    try:
        int(response)
    except ValueError:
        print(
            f'\n{ui.space}{colors.red}• {colors.white}Invalid input'
        )
        continue
    
    if response == '1':
        ui.start()
    elif response == '2':
        while True:
            response = ui.configuration()
            if response == '1':
                ui.login()
            elif response == '2':
                ui.settings()
            elif response == '3':
                break
            else:
                print(
                    f'\n{ui.space}{colors.red}• {colors.white}Invalid input'
                )
    elif response == '3':
        break
    else:
        print(
            f'\n{ui.space}{colors.red}• {colors.white}Invalid input'
        )