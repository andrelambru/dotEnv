# THIS IS CRAP CODE!

import httpx
import asyncio
import random
import logging
from colorama import Fore, Style
import shutil
import os


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def center(str, filling=" ", newline=False):
    print(str.center(shutil.get_terminal_size().columns, filling))
    if newline:
        print("\n")


def header():
    clear()
    center(f"{Fore.BLUE}_       _   _____")
    center("    __| | ___ | |_| ____|_ ____   __")
    center("   / _` |/ _ \| __|  _| | '_ \ \ / /")
    center("  | (_| | (_) | |_| |___| | | \ V / ")
    center(" (_)__,_|\___/ \__|_____|_| |_|\_/  ", newline=True)

    center(f"{Fore.CYAN}      [> https://github.com/andrelambru <]", newline=True)
    center(f"{Fore.RED}      [!] THIS TOOL IS NOT MEANT FOR ANY BAD USE!")
    center(f"      [!] I DO NOT HAVE ANY RESPONSABILITY FOR ITS USE.{Style.RESET_ALL}", newline=True)


async def send_request(client: httpx.AsyncClient, semaphore: asyncio.Semaphore, url) -> int:
    async with semaphore:
        try:
            response = await client.get(url, timeout=1)
            status = response.status_code
            #print(url + " | " + str(status))
            if status == 200:
                print(url, file=open("good.txt", "a"))
                print(Fore.LIGHTGREEN_EX + url + Style.RESET_ALL)

        except Exception as e:
            status = -1

    return status, url


async def main(urls) -> int:
    global semaphore
    semaphore = asyncio.Semaphore(semaphore)
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(send_request(client, semaphore, url)) for url in urls]
        await asyncio.gather(*tasks)

def generateIps(num):
    ips = []
    for _ in range(num):
        ips.append("http://" + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "."  + str(random.randint(0,255)) + "/.env")
    return ips

if __name__ == "__main__":
    semaphore = 100
    header()
    num = int(input("[?] How many IPs do you want to generate: "))
    print("[>] Generating " + str(num) + " IPs")
    ips = generateIps(num)
    print("[>] Scanning...")
    asyncio.run(main(ips))