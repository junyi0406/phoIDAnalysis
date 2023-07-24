def optimize(self):
    import hyperopt
    import pandas as pd
    """Function that performs bayesian optimization"""
    trials = hyperopt.Trials()

    self._best_result = hyperopt.fmin(fn=self._get_loss, space=self.search_space, trials=trials,
                                algo=hyperopt.tpe.suggest, max_evals=50)
    
    columns = list(self.search_space.keys())   
    results = pd.DataFrame(columns=['iteration'] + columns + ['loss'])
    
    for idx, trial in enumerate(trials.trials):
        row = [idx]
        translated_eval = hyperopt.space_eval(self.search_space, {k: v[0] for k, v in trial['misc']['vals'].items()})
        for k in columns:
            row.append(translated_eval[k])
        row.append(trial['result']['loss'])
        results.loc[idx] = row

    path = self.config_local.path_result / self.model_name
    path.mkdir(parents=True, exist_ok=True)
    results.to_csv(str(path / "trials.csv"), index=False)
    
    self._logger.info(results)
    self._logger.info('Found golden setting:')
    self._logger.info(hyperopt.space_eval(self.search_space, self._best_result)) 
    
def json_to_space(j):
    import hyperopt.hp as hp
    
    space = {}

    for key, value in j.items():
        if value[0] == 'quniform':
            space[key] = [hp.quniform(key, *value[1:])]
        elif value[0] == 'choice':
            space[key] = [hp.choice(key, *value[1:])]
        elif value[0] == 'uniform':
            space[key] = [hp.uniform(key, *value[1:])]
        # etc ...
    return space

def tunning_best_parameters(dataset, params_space, num_eval, OutDir):
    import sklearn
    import numpy as np
    import xgboost as xgb
    import multiprocessing
    import pickle as pk
    import hyperopt
    
    trials = hyperopt.Trials()
    def objective(params):
        sc = sklearn.preprocessing.MinMaxScaler()
        X_train, Y_train, Wt_train, X_test, Y_test, Wt_test = dataset
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        eval_s = [(X_train, Y_train),(X_test,Y_test)]
        xgb_model = xgb.XGBClassifier(objective="binary:logistic", tree_method = "gpu_hist")
        cv = sklearn.model_selection.GridSearchCV(xgb_model, params,  early_stopping_rounds = 20, n_estimators=1500,
                                scoring='neg_log_loss',cv=3,verbose=1,n_jobs=multiprocessing.cpu_count())
        search = cv.fit(X_train, Y_train,  sample_weight=Wt_train, verbose=0, eval_set=eval_s)
        return {"loss": np.average(search.best_score_), "status": hyperopt.STATUS_OK}
    best = hyperopt.fmin(
        fn = objective,
        space=params_space,
        algo=hyperopt.tpe.suggest,
        max_evals=num_eval,
        trials=trials
    )
    best_hyperparams = hyperopt.space_eval(params_space, best)
    pk.dump(best_hyperparams, open(OutDir+"_best_params.pk", "wb"))
    return best_hyperparams