
def train_xgb(df, XGBconf, OutDir=""):
    # save the results to pickle file
    import numpy as np
    import xgboost as xgb
    import multiprocessing
    import pickle as pk
    from sklearn.model_selection import cross_val_score, GridSearchCV
    
    df.loc[(df["Category"] == "DYJets"), "isSignal"] = int(0)
    df.loc[(df["Category"] == "HZg") | (df["Category"] == "SMZg"), "isSignal"] = int(1)
    # barrel
    X_train = df.loc[(df["Dataset"] == "Train")
                    & (df["region"] == "barrel"), XGBconf["features"]["barrel"]]
    Y_train = df.loc[(df["Dataset"] == "Train")
                    & (df["region"] == "barrel"), "isSignal"]
    Wt_train = df.loc[(df["Dataset"] == "Train")
                    & (df["region"] == "barrel"),"NewWt"]

    X_test = df.loc[(df["Dataset"] == "Test")
                    & (df["region"] == "barrel"), XGBconf["features"]["barrel"]]
    Y_test = df.loc[(df["Dataset"] == "Test")
                    & (df["region"] == "barrel"), "isSignal"]
    Wt_test = df.loc[(df["Dataset"] == "Test")
                    & (df["region"] == "barrel"),"NewWt"]
    eval_s = [(X_train, Y_train),(X_test,Y_test)]
    
    if XGBconf["useGPU"]:
        xgb_model = xgb.XGBClassifier(objective="binary:logistic",
            tree_method = "gpu_hist")
    else:
        xgb_model = xgb.XGBClassifier(objective="binary:logistic")
    
    if XGBconf["multiCore"]:
        cv_barrel = GridSearchCV(xgb_model, XGBconf["XGBGridSearch"],
                            scoring='neg_log_loss',cv=3,verbose=1,n_jobs=multiprocessing.cpu_count())#multiprocessing.cpu_count())
    else:
        cv_barrel = GridSearchCV(xgb_model, XGBconf["XGBGridSearch"],
                            scoring='neg_log_loss',cv=3,verbose=1)
    print("start fit (barrel)")
    search_barrel = cv_barrel.fit(X_train, Y_train, sample_weight=Wt_train, verbose=0, eval_set=eval_s)
    pk.dump(cv_barrel, open(OutDir+"barrel_modelXGB.pk", "wb"))
    print("Trainning results in barrel:")
    print("Expected neg log loss of XGB model = "+str((np.round(np.average(search_barrel.best_score_),3))*100)+'%')
    print("Expected accuracy of XGB model = "+str((np.average(search_barrel.best_score_))*100)+'%')
    print("XGB Best Parameters")
    print(str(search_barrel.best_params_))
    
    # endcap
    X_train = df.loc[(df["Dataset"] == "Train")
                    & (df["region"] == "endcap"), XGBconf["features"]["endcap"]]
    Y_train = df.loc[(df["Dataset"] == "Train")
                    & (df["region"] == "endcap"), "isSignal"]
    Wt_train = df.loc[(df["Dataset"] == "Train")
                    & (df["region"] == "endcap"),"NewWt"]

    X_test = df.loc[(df["Dataset"] == "Test")
                    & (df["region"] == "endcap"), XGBconf["features"]["endcap"]]
    Y_test = df.loc[(df["Dataset"] == "Test")
                    & (df["region"] == "endcap"), "isSignal"]
    Wt_test = df.loc[(df["Dataset"] == "Test")
                    & (df["region"] == "endcap"),"NewWt"]
    eval_s = [(X_train, Y_train),(X_test,Y_test)]
    
    if XGBconf["useGPU"]:
        xgb_model = xgb.XGBClassifier(objective="binary:logistic",
            tree_method = "gpu_hist")
    else:
        xgb_model = xgb.XGBClassifier(objective="binary:logistic")
    
    if XGBconf["multiCore"]:
        cv_endcap = GridSearchCV(xgb_model, XGBconf["XGBGridSearch"],
                            scoring='neg_log_loss',cv=3,verbose=1,n_jobs=multiprocessing.cpu_count())#multiprocessing.cpu_count())
    else:
        cv_endcap = GridSearchCV(xgb_model, XGBconf["XGBGridSearch"],
                            scoring='neg_log_loss',cv=3,verbose=1)
    print("start fit (endcap)")
    search_endcap = cv_endcap.fit(X_train, Y_train, sample_weight=Wt_train,verbose=0,eval_set=eval_s)
    pk.dump(cv_endcap, open(OutDir+"endcap_modelXGB.pk", "wb"))
    print("Trainning results in endcap:")
    print("Expected neg log loss of XGB model = "+str((np.round(np.average(search_endcap.best_score_),3))*100)+'%')
    print("Expected accuracy of XGB model = "+str((np.average(search_endcap.best_score_))*100)+'%')
    print("XGB Best Parameters")
    print(str(search_endcap.best_params_))
    return [search_barrel, search_endcap]