import websockets
import pickle
import asyncio
import json
import pandas as pd
from sklearn.model_selection import train_test_split

async def query_sock():
    df = []
    model = pickle.load(open("model.save", "rb"))
    async with websockets.connect("ws://localhost:8000/ws?uuid=") as websocket:
        await websocket.send('{"command": "subscribe", "payload": "raw"}')
        while True:
            data = await websocket.recv()
            df = parse(df, json.loads(data))
            print(len(df))
            if len(df) == 250:
                print(df)
                return
                Y = 'test'
                X = df 
                X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0,random_state=0)
                # pred_data = pd.DataFrame({'A':df})
                # for index, d in enumerate(df):
                #     pred_data.append({f'index':d})
                pred = model.predict(X_test)
                print(pred)
                break


def parse(df, data):
    last_time = None
    try:
        payload = data['payload']['data']
    except:
        return []
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