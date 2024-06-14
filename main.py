import asyncio
from utils.logger import logger
from utils.coingecko import CoinGecko

async def retry_funcion(func, thread, *args, **kwargs):
    while True:
        result = await func(*args, **kwargs)
        return result

async def Gecko(thread, filepath: str):
    logger.info(f"Thread {thread} | Starts")
    while True:
        with open(filepath, 'r') as file:
            for line in file:
                email = line.split(" ")[0]
                password = line.split(" ")[1]

        gecko = CoinGecko(email, password, "Login:Password@Address:Port")

        if await retry_funcion(gecko.login, thread):
            await gecko.login()
            print("login")
        await asyncio.sleep(5000)



async def main():
    thread_count = int(input("Enter threads number: "))
    filepath = "./data/accounts.txt"
    tasks=[]
    for thread in range(0, thread_count):
        tasks.append(asyncio.create_task(Gecko(thread, filepath)))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())