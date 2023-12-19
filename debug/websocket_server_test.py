import asyncio
import os

import BlynkLib

queue = asyncio.Queue()


async def coroutine1(queue):
    print("Coroutine 1 is starting")
    message = "Hello from Coroutine 1"
    await asyncio.sleep(10)
    # await queue.put(message)
    print("Coroutine 1 is ending")


async def coroutine2(queue):
    await asyncio.sleep(10)
    print("Coroutine 2 is starting")
    message = await queue.get()
    print(f"Received message in Coroutine 2: {message}")
    await asyncio.sleep(10)
    print("Coroutine 2 is ending")


async def coroutine_blynk(queue):
    blynk = BlynkLib.Blynk(os.environ.get("BLYNK_TOKEN"), **{"server": "blynk.cloud"})

    @blynk.VIRTUAL_WRITE(3)
    async def virtual_3(value):
        """
        暖房 OFF/温度指定
        :param value:
        :return:
        """
        print("v3", value)
        await queue.put(value)

    for i in range(100):
        blynk.run()
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(coroutine1(queue))
    task2 = asyncio.create_task(coroutine2(queue))
    task_blynk = asyncio.create_task(coroutine_blynk(queue))

    await task1
    await task2
    await task_blynk


if __name__ == "__main__":
    asyncio.run(main())
