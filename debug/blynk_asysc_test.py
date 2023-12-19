import asyncio
import os

import BlynkLib

# Blynkのインスタンスを作成
blynk = BlynkLib.Blynk(os.environ.get("BLYNK_TOKEN"), **{"server": "blynk.cloud"})

# asyncio.Queueを作成
value_queue = asyncio.Queue()


# Virtual Pinの設定
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    print("Received value:", value[0])
    # データをキューに追加
    value_queue.put_nowait(value[0])


async def coroutine1():
    print("Coroutine 1 started")
    await asyncio.sleep(30)
    # キューからデータを取得
    received_value = await value_queue.get()
    print("Coroutine 1 received value:", received_value)
    await asyncio.sleep(3)
    print("Coroutine 1 finished")


async def coroutine2():
    print("Coroutine 2 started")
    await asyncio.sleep(2)
    print("Coroutine 2 finished")


async def main():
    # Blynkのイベントループを非同期イベントループに組み込む
    loop = asyncio.get_event_loop()
    loop.create_task(blynk.run())

    # asyncio.gatherで複数のコルーチンを同時に実行
    await asyncio.gather(coroutine1(), coroutine2())


# イベントループを取得
loop = asyncio.get_event_loop()

# mainコルーチンを実行
loop.run_until_complete(main())

# イベントループを閉じる
loop.close()
