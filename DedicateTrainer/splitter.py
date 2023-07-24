

def split_category(df, test_size, cates):
    from sklearn.model_selection import train_test_split
    index = df.index
    for region in ["barrel", "endcap"]:
        TrainIndices=[]
        TestIndices=[]
        for cate in cates:
            condition = (df["Category"] == cate) & (df["region"] == region)
            Indices = index[condition].values.tolist()
            myclassTrainIndices, myclassTestIndices = train_test_split(
                Indices, 
                test_size=test_size,
                # random_state=rand_state, 
                shuffle=True
            )
            TrainIndices=TrainIndices + myclassTrainIndices
            TestIndices=TestIndices + myclassTestIndices
        df.loc[TrainIndices,'Dataset'] = "Train"
        df.loc[TestIndices,'Dataset'] = "Test"

        df.loc[TrainIndices,'TrainDataset'] = 1
        df.loc[TestIndices,'TrainDataset'] = 0
    return df


def check_test_train_dataset(df, filename):
    import seaborn as sns
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 1, figsize=(10, 5))
    kplot=sns.countplot(x="Category", data=df, ax=axes,hue='Dataset',palette=['#432371',"#FAAE7B","black"])
    for p in kplot.patches:
        kplot.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points',size=8)
    axes.set_title("Number of samples")
    plt.savefig(filename)
    
def split_test_train_validate(df, region, cates, train_ratio, test_ratio, validation_ratio):
    from sklearn.model_selection import train_test_split
    
    index = df.index

    for cate in cates:
        condition =  (df["Category"] == cate) & (df["region"] == region)
        Indices = index[condition].values.tolist()
        # train is now 75% of the entire data set
        train_indices, remain_indices  = train_test_split(Indices,        test_size = (validation_ratio+test_ratio)/(train_ratio + test_ratio + validation_ratio))
        test_indices, validate_indices = train_test_split(remain_indices, test_size = validation_ratio/(validation_ratio+test_ratio))
        df.loc[train_indices,'Dataset'] = "Train"
        df.loc[test_indices,'Dataset'] = "Test"
        df.loc[validate_indices,'Dataset'] = "Validate"

        df.loc[train_indices,'TrainDataset'] = 1
        df.loc[test_indices,'TrainDataset'] = 0
        df.loc[validate_indices,'TrainDataset'] = 2
    return df