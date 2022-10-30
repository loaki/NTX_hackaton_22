import websockets
import pickle
import asyncio
import json
import pandas as pd
import warnings
from sklearn.model_selection import train_test_split
from pynput.keyboard import Key, Controller


keyboard = Controller()

async def query_sock():
    df = []
    model = pickle.load(open("model.save", "rb"))
    async with websockets.connect("ws://localhost:8000/ws?uuid=") as websocket:
        await websocket.send('{"command": "subscribe", "payload": "filtered"}')
        while True:
            data = await websocket.recv()
            index, df = parse(df, json.loads(data))
            # print(len(df))
            if len(df) == 500:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    pred_proba = model.predict_proba([df[index:index+250]])[0]
                    if max(pred_proba) >= 0.7:
                        pred = model.predict([df[index:index+250]])
                        print(pred, max(pred_proba))
                        if pred[0] == 'right' and max(pred_proba) >= 0.9:
                            print('right')
                            keyboard.press('a')
                            keyboard.release('a')
                        if pred[0] == 'left':
                            print('left')
                            keyboard.press('d')
                            keyboard.release('d')
                        if pred[0] == 'rest':
                            print('rest')
                            # keyboard.press(Key.space)
                            # keyboard.release(Key.space)


def parse(df, data):
    last_time = None
    try:
        payload = data['payload']['data']
    except:
        return 0, []
    if not last_time:
        last_time = list(payload.keys())[0]
    for key in payload.keys():
        if int(key) >= int(last_time) + 10:
            df.append(payload[key]['Fpz'])
            last_time = key
    if len(df) > 500:
        df = df[-500:]
    df_sort = sorted(df)
    # print(df[0], df[-1], df[int(len(df) / 2)])
    for i in range(len(df)):
        if df[i] > 0.7 * df_sort[0] or df[i] < 0.7 * df_sort[-1]:
            if i + 200 > len(df):
                return 250, df
            if i < 50:
                return 0, df
            return i-50, df
    return 250, df

if __name__ == '__main__':
    asyncio.run(query_sock())
