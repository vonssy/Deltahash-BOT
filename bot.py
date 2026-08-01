from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    BasicAuth
)
from aiohttp_socks import ProxyConnector
from datetime import datetime
from colorama import *
import asyncio, random, sys, re, os

class DeltaHash:
    def __init__(self) -> None:
        self.API_URL = "https://portal.deltahash.ai"

        self.REF_CODE = "DELTA-D4459A" # U can change it with yours.

        self.USE_PROXY = False
        self.ROTATE_PROXY = False
        
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.accounts = {}

        self.USER_AGENTS = {
            "desktop": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.122 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.185 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.200 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.118 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.149 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.105 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36",
            ],
            "mobile": [
                "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.118 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.105 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 12; Redmi Note 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.178 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 11; vivo 1906) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.193 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; Mi 9T Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.194 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
            ]
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def print_message(self, idx, proxy, prefix, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {idx} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}{prefix}:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}DeltaHash {Fore.BLUE + Style.BRIGHT}Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_cookies(self):
        filename = "cookies.txt"
        try:
            with open(filename, 'r') as file:
                cookies = [line.strip() for line in file if line.strip()]
            return cookies
        except Exception as e:
            print(f"{Fore.RED + Style.BRIGHT}Failed To Load Cookies: {e}{Style.RESET_ALL}")
            return None

    def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"
    
    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
    
    def display_proxy(self, proxy_url=None):
        if not proxy_url: return "No Proxy"

        proxy_url = re.sub(r"^(http|https|socks4|socks5)://", "", proxy_url)

        if "@" in proxy_url:
            proxy_url = proxy_url.split("@", 1)[1]

        return proxy_url

    def extract_conncet_sid(self, idx: int):
        cookie = self.accounts[idx]["cookie"]
        if cookie.startswith("connect.sid"):
            cookie.removeprefix("connect.sid=")
        return {
            "connect.sid": cookie
        }
    
    def initialize_headers(self, idx: int):
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Origin": "https://portal.deltahash.ai",
            "Pragma": "no-cache",
            "Referer": "https://portal.deltahash.ai/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.accounts[idx]["user_agent"]
        }

        return headers.copy()
    
    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run Without Proxy{Style.RESET_ALL}")
                proxy_choice = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        "With" if proxy_choice == 1 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    self.USE_PROXY = True if proxy_choice == 1 else False
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

        if self.USE_PROXY:
            while True:
                rotate_proxy = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()
                if rotate_proxy in ["y", "n"]:
                    self.ROTATE_PROXY = True if rotate_proxy == "y" else False
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")
    
    async def ensure_ok(self, response):
        if response.status >= 400:
            error_text = await response.text()
            raise Exception(f"HTTP {response.status}: {error_text}")
    
    async def check_connection(self, idx: int, proxy_url=None):
        url = "https://api.ipify.org?format=json"

        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.get(url=url, proxy=proxy, proxy_auth=proxy_auth) as response:
                    await self.ensure_ok(response)
                    return True
        except (Exception, ClientResponseError) as e:
            self.print_message(
                idx, 
                self.display_proxy(proxy_url), 
                "Status",
                Fore.RED, 
                f"Connection Not 200 OK: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
            )
        
        return None
    
    async def auth_me(self, idx: int, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/auth/me"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                cookies = self.extract_conncet_sid(idx)

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, cookies=cookies, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Authenticate Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def apply_code(self, idx: int, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/referrals/apply"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                headers["Content-Type"] = "application/json"
                cookies = self.extract_conncet_sid(idx)
                payload = {
                    "code": self.REF_CODE
                }

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, cookies=cookies, json=payload, proxy=proxy, proxy_auth=proxy_auth) as response:
                        if response.status == 400: return None
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Apply Code Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def complete_social(self, idx: int, title: str, task_id: str, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/social/complete"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                headers["Content-Type"] = "application/json"
                cookies = self.extract_conncet_sid(idx)
                payload = {
                    "task": task_id
                }

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, cookies=cookies, json=payload, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Failed to Complete Task {title}: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def user_profile(self, idx: int, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/profile"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                cookies = self.extract_conncet_sid(idx)

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, cookies=cookies, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Failed to Fetch Device Id: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def devices_connect(self, idx: int, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/devices/connect"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                headers["Content-Type"] = "application/json"
                cookies = self.extract_conncet_sid(idx)

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, cookies=cookies, json={}, proxy=proxy, proxy_auth=proxy_auth) as response:
                        if response.status == 500:
                            self.accounts[idx]["user_agent"] = random.choice(self.USER_AGENTS["mobile"])
                            continue
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Failed to Registering New Device: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def mining_status(self, idx: int, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/mining/status"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                cookies = self.extract_conncet_sid(idx)

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, cookies=cookies, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Failed to Fetch Mining Status: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def mining_connect(self, idx: int, cloud_device_id=None, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/mining/connect"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                headers["Content-Type"] = "application/json"
                cookies = self.extract_conncet_sid(idx)
                if cloud_device_id:
                    payload = {
                        "cloudDeviceId": cloud_device_id
                    }
                else:
                    payload = {}

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, cookies=cookies, json=payload, proxy=proxy, proxy_auth=proxy_auth) as response:
                        if response.status == 400:
                            self.accounts[idx]["user_agent"] = random.choice(self.USER_AGENTS["mobile"])
                            continue
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Failed to Connect Device: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def mining_heartbeat(self, idx: int, proxy_url=None, retries=5):
        url = f"{self.API_URL}/api/mining/heartbeat"
        
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                headers = self.initialize_headers(idx)
                cookies = self.extract_conncet_sid(idx)

                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, cookies=cookies, proxy=proxy, proxy_auth=proxy_auth) as response:
                        await self.ensure_ok(response)
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(
                    idx, 
                    self.display_proxy(proxy_url), 
                    "Status",
                    Fore.RED, 
                    f"Failed to Sent Heartbeat: {Fore.YELLOW+Style.BRIGHT}{str(e)}"
                )

        return None
    
    async def process_check_connection(self, idx: int, proxy_url=None):
        while True:
            await asyncio.sleep(1)

            if self.USE_PROXY:
                proxy_url = self.get_next_proxy_for_account(idx)

            connection = await self.check_connection(idx, proxy_url)
            if connection: return True

            if self.ROTATE_PROXY:
                proxy_url = self.rotate_proxy_for_account(idx)

    async def process_auth_user(self, idx: int, proxy_url=None):
        while True:
            await asyncio.sleep(1)

            user = await self.auth_me(idx, proxy_url)
            if not user: continue

            user_data = user.get("user")
            if not user_data: return False

            username = user_data.get("username")
            balance = user_data.get("balance")

            self.print_message(
                idx,
                self.display_proxy(proxy_url),
                "Username",
                Fore.WHITE,
                f"{username} "
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Balance: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{balance} $DTH{Style.RESET_ALL}"
            )

            referred_by = user_data.get("referredBy")
            if referred_by is None: await self.apply_code(idx, proxy_url)

            x_followed = user_data.get("xFollowed")
            if not x_followed:
                complete = await self.complete_social(idx, "Follow X", "x_follow", proxy_url)
                if complete:
                    self.print_message(
                        idx,
                        self.display_proxy(proxy_url),
                        "Status",
                        Fore.GREEN,
                        f"Task Follow X Completed"
                    )

            tg_joined = user_data.get("tgJoined")
            if not tg_joined:
                complete = await self.complete_social(idx, "Join Telegram", "tg_join", proxy_url)
                if complete:
                    self.print_message(
                        idx,
                        self.display_proxy(proxy_url),
                        "Status",
                        Fore.GREEN,
                        f"Task Join Telegram Completed"
                    )

            return True

    async def process_mining_status(self, idx: int, proxy_url=None):
        while True:
            await asyncio.sleep(30)

            mining = await self.mining_status(idx, proxy_url)
            if not mining: continue

            epoch_number = mining.get("epoch", {}).get("number")
            is_mining = mining.get("isMining")
            balance = mining.get("balance")
            cloud_devices = mining.get("cloudDevices")

            if cloud_devices:
                cloud_device_id = cloud_devices[0]["id"]
            else:
                cloud_device_id = None

            self.print_message(
                idx,
                self.display_proxy(proxy_url),
                "Epoch",
                Fore.WHITE,
                f"{Fore.WHITE + Style.BRIGHT} {epoch_number} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Balance: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{balance} $DTH{Style.RESET_ALL}"
            )

            if not is_mining:
                await self.process_mining_connect(idx, cloud_device_id, proxy_url)

                if not cloud_device_id:
                    await self.process_mining_heartbeat(idx, proxy_url)

    async def process_handle_mining(self, idx: int, proxy_url=None):
        while True:
            await asyncio.sleep(1)

            profile = await self.user_profile(idx, proxy_url)
            if not profile: continue

            device_id = profile.get("deviceId")
            if device_id is None:
                self.print_message(
                    idx,
                    self.display_proxy(proxy_url),
                    "Status",
                    Fore.RED,
                    f"No Device Registered. "
                    f"{Fore.YELLOW + Style.BRIGHT}Registering New Devices...{Style.RESET_ALL}"
                )

                await self.process_devices_connect(idx, proxy_url)
                continue

            await self.process_mining_status(idx, proxy_url)

    async def process_devices_connect(self, idx: int, proxy_url=None):
        while True:
            await asyncio.sleep(1)

            connect = await self.devices_connect(idx, proxy_url)
            if not connect:
                continue

            device_id = connect.get("user", {}).get("deviceId")

            self.print_message(
                idx,
                self.display_proxy(proxy_url),
                "Status",
                Fore.GREEN,
                f"Registering New Device Success "
            )

            return device_id

    async def process_mining_connect(self, idx: int, cloud_device_id=None, proxy_url=None):
        while True:
            await asyncio.sleep(1)

            connect = await self.mining_connect(idx, cloud_device_id, proxy_url)
            if not connect: continue

            device_id = connect.get("session", {}).get("deviceId")

            self.print_message(
                idx,
                self.display_proxy(proxy_url),
                "Status",
                Fore.GREEN,
                f"Device Connected "
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Device Id: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{device_id}{Style.RESET_ALL}"
            )

            return True

    async def process_mining_heartbeat(self, idx: int, proxy_url=None):
        while True:
            await asyncio.sleep(30)

            heartbeat = await self.mining_heartbeat(idx, proxy_url)
            if not heartbeat:
                continue

            disconnected = heartbeat.get("disconnected")
            if disconnected:
                self.print_message(
                    idx,
                    self.display_proxy(proxy_url),
                    "Status",
                    Fore.RED,
                    f"Disconnected. "
                    f"{Fore.YELLOW + Style.BRIGHT}Curently Reconnecting...{Style.RESET_ALL}"
                )

                await self.process_mining_connect(idx, proxy_url)
                continue

            epoch_number = heartbeat.get("epochNumber")
            tokens_earned = heartbeat.get("tokensEarned")
            new_balance = heartbeat.get("newBalance")

            self.print_message(
                idx,
                self.display_proxy(proxy_url),
                "Status",
                Fore.GREEN,
                f"Heartbeat Sent "
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} Epoch: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{epoch_number}{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}Earned:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {tokens_earned} $DTH {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT} New Balance: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{new_balance} $DTH{Style.RESET_ALL}"
            )

    async def process_accounts(self, idx: int, proxy_url=None):
        if await self.process_check_connection(idx, proxy_url):

            if self.USE_PROXY:
                proxy_url = self.get_next_proxy_for_account(idx)

            await asyncio.gather(*[
                asyncio.create_task(self.process_auth_user(idx, proxy_url)),
                asyncio.create_task(self.process_handle_mining(idx, proxy_url))
            ])

    async def main(self):
        try:
            cookies = self.load_cookies()
            if not cookies:
                print(f"{Fore.RED+Style.BRIGHT}No Cookies Loaded.{Style.RESET_ALL}") 
                return

            self.print_question()
            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(cookies)}{Style.RESET_ALL}"
            )

            if self.USE_PROXY: self.load_proxies()

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*75)

            tasks = []
            for idx, cookie in enumerate(cookies, start=1):
                if idx not in self.accounts:
                    self.accounts[idx] = {
                        "cookie": cookie,
                        "user_agent": random.choice(self.USER_AGENTS["desktop"])
                    }
                    
                tasks.append(asyncio.create_task(self.process_accounts(idx)))

            await asyncio.gather(*tasks)

        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e
        except asyncio.CancelledError:
            raise

if __name__ == "__main__":
    try:
        bot = DeltaHash()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] DeltaHash - BOT{Style.RESET_ALL}                                       "                              
        )
    finally:
        sys.exit(0)