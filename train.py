#%%
import pandas as pd
import h5py

# %%

def read_hdf5(filename, label: str = "right"):
    f = h5py.File(filename, 'r')
    df = pd.DataFrame(columns=[str(x) for x in range(250)])
    for key in f.keys():
        line = [x for x in f[key]]
        df.loc[len(df.index)] = line
    df['label'] = label
    
    return df


def create_dataframe():
    df_right = read_hdf5(filename="data/right_label.hdf5", label="right")
    df_left = read_hdf5(filename="data/left_label.hdf5", label="left")
    df_rest = read_hdf5(filename="data/none_label.hdf5", label="rest")
    frame = [df_right, df_left, df_rest]
    df = pd.concat(frame)
    
    return df

df = create_dataframe()

# %%
from sklearn.model_selection import train_test_split

Y = df['label']
X = df.drop(columns="label")
print(type(X))

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size =1, random_state = 0)


# %%
from sklearn import svm
classifier = svm.SVC(decision_function_shape='ovo')
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

# Classification metrics
from sklearn.metrics import accuracy_score, classification_report
classification_report = classification_report(y_test, y_pred)

print('\n Accuracy: ', accuracy_score(y_test, y_pred))
print('\nClassification Report Pour un SVM')
print('======================================================')
print('\n', classification_report)

# %%

pred = classifier.predict(X_test[0:1])

import pickle


pickle.dump(classifier, open('model.save', 'wb'))


# %%

model = pickle.load(open("model.save", "rb"))
test = model.predict(X_test[0:1])


# %%