# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.


import os
import numpy as np
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from azureml.core.run import Run
import joblib
from utils import mylib

try:
    from collections.abc import Iterator
except ImportError:
    from collections import Iterator


os.makedirs('./outputs', exist_ok=True)

X, y = load_diabetes(return_X_y=True)

run = Run.get_context()

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=0)
data = {"train": {"X": X_train, "y": y_train},
        "test": {"X": X_test, "y": y_test}}

# list of numbers from 0.0 to 1.0 with a 0.05 interval
alphas = np.arange(0.0, 1.0, 0.05)

for alpha in alphas:
    # Use Ridge algorithm to create a regression model
    reg = Ridge(alpha=alpha)
    reg.fit(data["train"]["X"], data["train"]["y"])

    preds = reg.predict(data["test"]["X"])
    mse = mean_squared_error(preds, data["test"]["y"])
    run.log('alpha', alpha)
    run.log('mse', mse)

    # Save model in the outputs folder so it automatically get uploaded when running on AML Compute
    model_file_name = 'ridge_{0:.2f}.pkl'.format(alpha)
    with open(model_file_name, "wb") as file:	
        joblib.dump(value=reg, filename=os.path.join('./outputs/',model_file_name))
    
    print('alpha is {0:.2f}, and mse is {1:0.2f}'.format(alpha, mse))

# opening the file
open_model = joblib.load('ridge_0.95.pkl')
# check prediction X=5000
check_pred = open_model.predict([[5000]])
print('PredictValue:'+ check_pred)