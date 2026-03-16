import os
import pandas as pd



from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def run_l1_logistic(cancelled_df, delayed_df, test_size=0.2, random_state=42):

    cols = [
        "origin_tavg",
        "origin_tmin",
        "origin_tmax",
        "origin_prcp",
        "origin_snow",
        "origin_wspd",
        "origin_pres",
    ]

    cancelled_X = cancelled_df[cols].dropna().reset_index(drop=True)
    delayed_X = delayed_df[cols].dropna().reset_index(drop=True)

    X = pd.concat([delayed_X, cancelled_X], ignore_index=True)
    # labels: delayed -> 1, cancelled -> 2
    y = np.array([1] * len(delayed_X) + [2] * len(cancelled_X))
    y_bin = (y == 1).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_bin, test_size=test_size, random_state=random_state, stratify=y_bin
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    clf = LogisticRegression(penalty="l1", solver="liblinear", random_state=random_state)
    clf.fit(X_train_s, y_train)

    acc = clf.score(X_test_s, y_test)
    print("Test accuracy:", round(acc, 4))

    coef = clf.coef_.ravel()
    for name, c in zip(cols, coef):
        print(f"{name}: {c:.4f}")

    return clf, scaler

def main():

    cancelled_flight = pd.read_csv("flight_cancelled.csv")
    delayed_complete = pd.read_csv("flight_delayed_complete.csv")

    n_cancelled = len(cancelled_flight)

    delayed_flight = delayed_complete.sample(n=n_cancelled, random_state=42).reset_index(drop=True)
    
    print(f"Number of cancelled flights: {len(cancelled_flight)}")
    print(f"Number of delayed flights: {len(delayed_flight)}")

    # save downsampled delayed if desired
    delayed_flight.to_csv("flight_delayed_downsampled.csv", index=False)

    # run L1 (lasso) logistic regression
    model, search = run_l1_logistic(cancelled_flight, delayed_flight)





    return


if __name__ == "__main__":
    main()


