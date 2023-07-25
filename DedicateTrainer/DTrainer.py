

def PrepDataset(df, region, dataset, features, cat, weight):
    import numpy as np
    X = df.loc[(df["Dataset"] == dataset) & (df["region"] == region), features]
    Y = df.loc[(df["Dataset"] == dataset) & (df["region"] == region), cat]
    Wt = df.loc[(df["Dataset"] == dataset) & (df["region"] == region),weight]
    return np.asarray(X), np.asarray(Y), np.asarray(Wt)

def PrepDataset_dask(df, region, features, cat, weight):
    import numpy as np
    import dask.array
    X_train = df.loc[(df["Dataset"] == "Train") & (df["region"] == region), features]
    Y_train = df.loc[(df["Dataset"] == "Train") & (df["region"] == region), cat]
    Wt_train = df.loc[(df["Dataset"] == "Train") & (df["region"] == region),weight]

    X_test = df.loc[(df["Dataset"] == "Test") & (df["region"] == region), features]
    Y_test = df.loc[(df["Dataset"] == "Test") & (df["region"] == region), cat]
    Wt_test = df.loc[(df["Dataset"] == "Test") & (df["region"] == region), weight]
    
    X_train, Y_train, Wt_train = np.asarray(X_train), np.asarray(Y_train), np.asarray(Wt_train)
    X_test,  Y_test,  Wt_test  = np.asarray(X_test), np.asarray(Y_test), np.asarray(Wt_test)
    return dask.array.from_array(X_train, chunks = 5000), dask.array.from_array(Y_train, chunks = 5000), dask.array.from_array(Wt_train, chunks = 5000), dask.array.from_array(X_test, chunks = 5000), dask.array.from_array(Y_test, chunks = 5000), dask.array.from_array(Wt_test, chunks = 5000)


def train_xgb(df, region, XGBconf, OutDir=""):
    # save the results to pickle file
    import numpy as np
    import xgboost as xgb
    import multiprocessing
    import pickle as pk
    import sklearn.preprocessing
    import DedicateTrainer as dt
    df.loc[(df["Category"] == "DYJets"), "isSignal"] = int(0)
    df.loc[(df["Category"] == "HZg") , "isSignal"] = int(1)
    df.loc[(df["Category"] == "SMZg"), "isSignal"] = int(1)
    X_test, Y_test, Wt_test    = PrepDataset(df, region, "Validate", XGBconf["features"][region], "isSignal", "NewWt")
    X_train, Y_train, Wt_train = PrepDataset(df, region, "Train", XGBconf["features"][region], "isSignal", "NewWt")

    if XGBconf["tunOptParams"]:
        space = dt.json_to_space(XGBconf["params_space"])
        neval = XGBconf["hyopt_possibility"]# if hasattr(XGBconf, "hyopt_possibility") else 50
        best_params = dt.tunning_best_parameters(
            [X_train, Y_train, Wt_train, X_test, Y_test, Wt_test], 
            params_space = space,
            num_eval = neval,
            OutDir = OutDir+region
        )
        params = best_params
    else:
        try:
            params = pk.load(open(OutDir+region+"_best_params.pk", "rb"))
        except FileNotFoundError:
            params = XGBconf["XGBGridSearch"]
    if XGBconf["useScalar"]:
        sc = eval("sklearn.preprocessing."+XGBconf["Scalar"]+"()")
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        pk.dump(sc, open(OutDir+region+"_Scalar.pk", "wb"))
        eval_s = [(X_train, Y_train),(X_test,Y_test)]
    else:
        eval_s = [(X_train, Y_train),(X_test,Y_test)]
    # dtrain = xgb.DMatrix(X_train, label = Y_train, weight = Wt_train)
    # dtest = xgb.DMatrix(X_test, label = Y_test, weight = Wt_test)

    if XGBconf["useGPU"]:
        xgb_model = xgb.XGBClassifier(objective="binary:logistic", tree_method = "gpu_hist", n_jobs = multiprocessing.cpu_count())
    else:
        xgb_model = xgb.XGBClassifier(objective="binary:logistic")
    # if XGBconf["multiCore"]:
    #     cv = sklearn.model_selection.GridSearchCV(xgb_model, params, 
    #                         scoring='neg_log_loss',cv=3,verbose=1,n_jobs=multiprocessing.cpu_count())#multiprocessing.cpu_count())
    # else:
    #     cv = sklearn.model_selection.GridSearchCV(xgb_model, params,
    #                         scoring='neg_log_loss',cv=3,verbose=1)
    # search = cv.fit(X_train, Y_train,  sample_weight=Wt_train, verbose=0, eval_set=eval_s)
    for key, val in params.items():
        params[key] = val[0]
    
    print("start fit ("+region+")")
    params["n_estimators"] = 1500
    params["early_stopping_rounds"] = 20
    xgb_model.set_params(**params)
    bst = xgb_model.fit(X_train, Y_train, sample_weight=Wt_train, eval_set = eval_s, verbose=0)
    pk.dump(xgb_model, open(OutDir+region+"_modelXGB.pk", "wb"))
    print("Trainning results in "+region+":")
    print("Best number of Boosting rounds = "+str(bst.best_iteration))
    print("Expected neg log loss of XGB model = "+str((np.round(np.average(bst.best_score),3))*100)+'%')
    print("Expected accuracy of XGB model = "+str((np.average(bst.best_score))*100)+'%')
    print("XGB Best Parameters")
    print(str(bst.get_params()))
    
    

def predict(df, region, path_to_result, XGBConf):
    import sklearn
    import pickle as pk
    import DedicateTrainer as dt
    import tensorflow as tf
    with open(path_to_result+region+"_Scalar.pk", "rb") as f:
        sc = pk.load(f) 
 
    with open(path_to_result+region+"_modelXGB.pk", "rb") as f:
        cv = pk.load(f)
   
    df.loc[(df["Category"] == "DYJets"), "isSignal"] = int(0)
    df.loc[(df["Category"] == "HZg") , "isSignal"] = int(1)
    df.loc[(df["Category"] == "SMZg"), "isSignal"] = int(1)
    # barrel 
    X_validate, Y_validate, Wt_validate    = PrepDataset(df, region, "Validate", XGBConf["features"][region], "isSignal", "NewWt")
    X_train, Y_train, Wt_train = PrepDataset(df, region, "Train", XGBConf["features"][region], "isSignal", "NewWt")
    X_test, Y_test, Wt_test = PrepDataset(df, region, "Test", XGBConf["features"][region], "isSignal", "NewWt")

    if XGBConf["useScalar"] is True:
        X_test  = sc.transform(X_test)
        X_validate  = sc.transform(X_validate)
        X_train = sc.fit_transform(X_train)
    y_test_pred  = cv.predict_proba(X_test)
    y_validate_pred  = cv.predict_proba(X_validate)
    y_train_pred = cv.predict_proba(X_train)
    Y_train = tf.keras.utils.to_categorical(Y_train, num_classes= 2)
    Y_test = tf.keras.utils.to_categorical(Y_test, num_classes= 2)
    Y_validate = tf.keras.utils.to_categorical(Y_validate, num_classes= 2)
    df.loc[(df["Dataset"] == "Train") & (df["region"]==region), XGBConf["MVAtype"]+"_pred"] = y_train_pred[:,1]
    df.loc[(df["Dataset"] == "Test") & (df["region"]==region),  XGBConf["MVAtype"]+"_pred"] = y_test_pred[:,1]
    df.loc[(df["Dataset"] == "Validate") & (df["region"]==region),  XGBConf["MVAtype"]+"_pred"] = y_validate_pred[:,1]
    
    return df    


def dask_train_xgb_with_predict(df, XGBConf, OutDir=""):
    import dask
    import dask_cuda
    import dask.distributed
    import pickle as pk
    import xgboost as xgb
    
    X_train, Y_train, Wt_train, X_test, Y_test, Wt_test = PrepDataset_dask(df, "barrel", XGBConf["features"]["barrel"], "isSignal", "NewWt")
    with dask_cuda.LocalCUDACluster() as cluster:
        with dask.distributed.Client(cluster) as client:
            ds_train = xgb.dask.DaskDMatrix(client, X_train, Y_train, weight = Wt_train)
            ds_test  = xgb.dask.DaskDMatrix(client, X_test, Y_test, weight = Wt_test)
            
            bst = xgb.dask.train(
                client,
                {"verbosity":1, "tree_method":"gpu_hist", "objective": "binary:logistic"},
                ds_train,
                num_boost_round = XGBConf["num_boost_round"],
                early_stopping_rounds = XGBConf["early_stopping_rounds"],
                evals = [(ds_train, "Train"), (ds_test, "Test")]
            )
            y_train_pred = xgb.dask.predict(client, bst, ds_train)
            y_test_pred = xgb.dask.predict(client, bst, ds_test)
            pk.dump(bst, open(OutDir+"barrel_dask_modelXGB.json", "wb"))
            # bst.save_model(OutDir+"barrel_dask_modelXGB.json")
            # bst = xgb.Booster(model_file=OutDir+"barrel_dask_modelXGB.pk")
            Y_train, y_train_pred, Wt_train = dask.compute(Y_train, y_train_pred, Wt_train)
            Y_test, y_test_pred, Wt_test = dask.compute(Y_test, y_test_pred, Wt_test)
            df.loc[(df["Dataset"] == "Train") & (df["region"]=="barrel"), XGBConf["MVAtype"]+"_dask_pred"] = y_train_pred
            df.loc[(df["Dataset"] == "Test") & (df["region"]=="barrel"),  XGBConf["MVAtype"]+"_dask_pred"] = y_test_pred
    
    X_train, Y_train, Wt_train, X_test, Y_test, Wt_test = PrepDataset_dask(df, "endcap", XGBConf["features"]["endcap"], "isSignal", "NewWt")
    with dask_cuda.LocalCUDACluster() as cluster:
        with dask.distributed.Client(cluster) as client:
            ds_train = xgb.dask.DaskDMatrix(client, X_train, Y_train, weight = Wt_train)
            ds_test  = xgb.dask.DaskDMatrix(client, X_test, Y_test, weight = Wt_test)
            
            bst = xgb.dask.train(
                client,
                {"verbosity":1, "tree_method":"gpu_hist", "objective": "binary:logistic"},
                ds_train,
                num_boost_round = XGBConf["num_boost_round"],
                early_stopping_rounds = XGBConf["early_stopping_rounds"],
                evals = [(ds_train, "Train"), (ds_test, "Test")]
            )
            y_train_pred = xgb.dask.predict(client, bst, ds_train)
            y_test_pred = xgb.dask.predict(client, bst, ds_test)
            pk.dump(bst, open(OutDir+"endcap_dask_modelXGB.json", "wb"))
            # bst.save_model(OutDir+"endcap_dask_modelXGB.json")
            # bst = xgb.Booster(model_file=OutDir+"endcap_dask_modelXGB.pk")
            Y_train, y_train_pred, Wt_train = dask.compute(Y_train, y_train_pred, Wt_train)
            Y_test, y_test_pred, Wt_test = dask.compute(Y_test, y_test_pred, Wt_test)
            df.loc[(df["Dataset"] == "Train") & (df["region"]=="endcap"), XGBConf["MVAtype"]+"_dask_pred"] = y_train_pred
            df.loc[(df["Dataset"] == "Test") & (df["region"]=="endcap"),  XGBConf["MVAtype"]+"_dask_pred"] = y_test_pred
    return df