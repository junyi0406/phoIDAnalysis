


def save_scalar(df, features, scalar, OutDir=""):
    import os
    import pickle as pk
    from sklearn.preprocessing import MinMaxScaler
    
    if scalar == "MinMaxScaler":
        sc_barrel = MinMaxScaler()

    X_train = df.loc[(df["Dataset"] == "Train") & (df["region"] == "barrel"), features["barrel"]]
    X_test = df.loc[(df["Dataset"] == "Test") & (df["region"] == "barrel"), features["barrel"]]

    X_train = sc_barrel.fit_transform(X_train)
    X_test = sc_barrel.transform(X_test)
    pk.dump(sc_barrel, open(OutDir+"barrel.pk", "wb"))
    
    if scalar == "MinMaxScaler":
        sc_endcap = MinMaxScaler()
    X_train = df.loc[(df["Dataset"] == "Train") & (df["region"] == "endcap"),features["endcap"]]

    X_test = df.loc[(df["Dataset"] == "Test") & (df["region"] == "endcap"), features["endcap"]]

    X_train = sc_endcap.fit_transform(X_train)
    X_test = sc_endcap.transform(X_test)
    pk.dump(sc_endcap, open(OutDir+"endcap.pk", "wb"))

    return [sc_barrel, sc_endcap]