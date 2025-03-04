# THIS IS CRAP CODE!

import httpx
import asyncio
import random
import logging
from colorama import Fore, Style
import shutil
import os
import threading
import time

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
    center("   / _` |/ _ \\| __|  _| | '_ \\ \\ / /")
    center("  | (_| | (_) | |_| |___| | | \\ V / ")
    center(" (_)__,_|\\___/ \\__|_____|_| |_|\\_/  ", newline=True)

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


async def main(urls, sem_value) -> int:
    semaphore = asyncio.Semaphore(sem_value)
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(send_request(client, semaphore, url)) for url in urls]
        await asyncio.gather(*tasks)

def generateIps(num):
    ips = []
    for _ in range(num):
        ips.append("http://" + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "."  + str(random.randint(0,255)) + "/.env")
    return ips

def getBatches(ips, th):
	k, m = divmod(len(ips), th)
	result = []
	start = 0
	for i in range(th):
		end = start + k + (1 if i < m else 0)
		result.append(ips[start:end])
		start = end
	return result

if __name__ == "__main__":
    sem_value = 100
    header()
    num = int(input("[?] How many IPs do you want to generate: "))
    threads = int(input("[?] How many threads: "))
    print("[>] Generating " + str(num) + " IPs")
    ips = generateIps(num)
    batches = getBatches(ips, threads)
    print(f"[>] IPs divided in {len(batches)} batches")
    print("[>] Scanning...")
    threads = []
    start_time = time.perf_counter()
    for batch in batches:
        coroutine = main(batch, sem_value)
        t = threading.Thread(target=asyncio.run, args=(coroutine,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"Tempo di esecuzione: {elapsed:.2f} secondi")
