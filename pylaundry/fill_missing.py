import numpy as np
import pandas as pd


def fill_missing(X_train, X_test, column_dict, num_imp, cat_imp):
    """
    Fill missing values in the dataframe based on user input.

    Arguments
    ---------     
    X_train: pandas.core.frame.DataFrame
        The training set, will be used for calculating and inputing values
    X_test: pandas.core.frame.DataFrame
        The test set, will be used for inputing values only.
    column_dict: dictionary
        A dictionary with keys = 'numeric','categorical',
        and values = a list of columns that fall into
        each respective category.
    num_imp -- string(default -"mean")
        imputation method for numeric features, options are "mean", "median"
    cat_imp -- list
        imputation method for categorical features, options are "mode"

    Returns
    -------
    dictionary 
        A dictionary with keys "X_train" and "X_test",
        and the modified dataframes as values.
    
    """

    # Check input types are as specified
    assert isinstance(X_train, pd.DataFrame), "X_train must be a Pandas DF"
    assert isinstance(X_test, pd.DataFrame), "X_test must be a Pandas DF"
    assert isinstance(column_dict, dict), "column_dict must be a dictionary"
    assert isinstance(num_imp, str), "num_imp should be a string"
    assert isinstance(cat_imp, str), "cat_imp should be a string"

    # Check train set and test set columns are the same
    assert np.array_equal(X_train.columns, X_test.columns), "X_train and X_test must have the same columns"

    # Check dictionary keys are numeric and categorical
    for key in column_dict.keys():
        assert key == 'numeric' or key == 'categorical', \
            "column_dict keys can be only 'numeric' and 'categorical'"

    # Check all the columns listed in dictionary are in the df
    for keys, values in column_dict.items():
        for column in values:
            assert column in X_train.columns, "columns in dictionary must be in dataframe"

    # Check that numerical imputation method is one of the two options 
    assert num_imp == "mean" or num_imp == "median", \
        "numerical imputation method can only be mean or median"

    # Check that categorical imputation method is the only option
    assert cat_imp == "mode", "cat_imp can only take 'mode' as argument value"

    # Check all columns contain numeric columns
    assert X_train.select_dtypes(include=["float", 'int']).shape[1] == X_train.shape[1], \
        "column values must be all numeric, must encode categorical variables as integers"

    # Imputation methods for numerical transforms
    for column in column_dict['numeric']:
        # get column mean or median
        if num_imp == "mean":
            col_imp = X_train[column].mean()
        if num_imp == "median":
            col_imp = X_train[column].median()

        # Get index of NaN values in train columns
        # Todo: If these are empty (no Nan) is that fine
        index_train = X_train[column].index[X_train[column].apply(np.isnan)]
        index_test = X_test[column].index[X_test[column].apply(np.isnan)]

        # Use impute value on train set
        X_train.loc[index_train, column] = col_imp
        # Use same impute value on test set
        X_test.loc[index_test, column] = col_imp

    # Imputation methods for categorical transforms 
    for column in column_dict['categorical']:
        # Note:  If mode is a tie, pandas picks lower value pick the lower value!
        col_imp = X_train[column].mode()[0]

        # Get index of NaN values in train columns
        index_train = X_train[column].index[X_train[column].isnull()]
        index_test = X_test[column].index[X_test[column].isnull()]

        # Use impute value on train set
        X_train.loc[index_train, column] = col_imp
        # Use same impute value on test set
        X_test.loc[index_test, column] = col_imp

    return {"X_train": X_train, "X_test": X_test}
