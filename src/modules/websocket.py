import asyncio
import websockets


# WebSocket接続時の処理を定義
async def on_connect(websocket, path):
    print(f"クライアントが接続しました: {websocket.remote_address}")
    try:
        while True:
            message = await websocket.recv()
            print(f"受信したメッセージ: {message}")
            await websocket.send(f"サーバーからの応答: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"クライアントが切断しました: {websocket.remote_address}")


# WebSocketサーバーを作成
start_server = websockets.serve(on_connect, "192.168.10.106", 8765)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
