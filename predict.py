import websockets
import pickle
import asyncio

async def query_sock():
    df = []
    model = pickle.load(open("model.save", "rb"))
    async with websockets.connect("ws://localhost:8000/ws?uuid=") as websocket:
        await websocket.send('{"command": "subscribe", "payload": "raw"}')
        while True:
            data = await websocket.recv()
            df = parse(df, data)
            if len(df) == 250:
                pred = model.predict(df)
                print(pred)


def parse(df, data):
    last_time = None
    payload = data['payload']['data']
    if not last_time:
        last_time = list(payload.keys())[0]
    for key in payload.keys():
        if int(key) >= int(last_time) + 10:
            df.append(payload[key]['Fpz'])
            last_time = key
    if len(df) > 250:
        return df[-250:]
    return df

if __name__ == '__main__':
    asyncio.run(query_sock())