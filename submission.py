import glob, os
import numpy as np
import matplotlib.pyplot as plt
from image_prep import prep_image
from keras.models import load_model
import pandas as pd

X1 = []
idx1 = []
for f in glob.glob('test_stg1/*.jpg'):
    idx1.append(f[10:])
    X1.append(prep_image(plt.imread(f)))
    print f, 'complete'
X1 = np.array(X1)
print X1.shape[0], 'stage 1 samples'

np.save('stg1_prcssd.npy', X1)

X2 = []
idx2 = []
for f in glob.glob('test_stg2/*.jpg'):
    idx2.append(f[10:])
    X2.append(prep_image(plt.imread(f)))
    print f, 'complete'
X2 = np.array(X2)
print X2.shape[0], 'stage 2 samples'

np.save('stg2_prcssd.npy', X2)


model = load_model('models/ns_mod4.h5')

proba1 = model.predict_proba(X1)
proba2 = model.predict_proba(X2)

prob1 = pd.DataFrame(proba1)
prob2 = pd.DataFrame(proba2)

prob1['image'] = idx1
prob2['image'] = idx2

prob1.set_index('image', drop=True, inplace=True)
prob2.set_index('image', drop=True, inplace=True)

cols = ['ALB', 'BET', 'DOL', 'LAG', 'NoF', 'OTHER', 'SHARK', 'YFT']

prob1.columns = cols
prob2.columns = cols

prob1.to_csv('stage1.csv')
prob2.to_csv('stage2.csv')