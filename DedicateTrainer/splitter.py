

def spit_promptPho(df, test_size, rand_state):
    from sklearn.model_selection import train_test_split
    TrainIndices=[]
    TestIndices=[]
    index = df.index
    for isPrompt in [0,1]:
        condition = df["_phoIsPrompt"] == isPrompt
        Indices = index[condition].values.tolist()
        myclassTrainIndices, myclassTestIndices = train_test_split(
            Indices, 
            test_size=test_size,
            random_state=rand_state, 
            shuffle=True
        )
        TrainIndices=TrainIndices + myclassTrainIndices
        TestIndices=TestIndices + myclassTestIndices
    df.loc[TrainIndices,'Dataset'] = "Train"
    df.loc[TestIndices,'Dataset'] = "Test"

    df.loc[TrainIndices,'TrainDataset'] = 1
    df.loc[TestIndices,'TrainDataset'] = 0
    return (TestIndices, TrainIndices)