import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
import numpy as np


def transform_columns(X_train, X_test, column_dict,
                      cat_trans="onehot_encoding",
                      num_trans="standard_scaling"):
    """
    Transforms categorical and numerical features based on user input.

    Arguments
    ---------
    X_train: pandas.core.frame.DataFrame
        A pandas dataframe for training set
    X_test: pandas.core.frame.DataFrame
        A pandas dataframe for test set
    column_dict: dictionary
        A dictionary with keys = 'numeric','categorical' and
        values = a list of columns that fall into each respective category.
    cat_trans: list
        transformation method for categorical features(default - 'ohe')
    num_trans: list
        transformation method for numerical features
        (default - 'StandardScaler')

    Returns
    -------
    dict
        A python dictionary with transformed training and
        test set with keys X_train and X_test respectively
    Examples
    --------
    df_train = pd.DataFrame({'a':[1, 2, 3],
                             'b':[1.2, 3.4, 3.0],
                             'c':['A','B','C']})
    df_test = pd.DataFrame({'a':[6, 2],
                            'b':[0.5, 9.2],
                            'c':['B', 'B']})
    transform_columns(df_train, df_test, {'numeric':['a', 'b'],
    'categorical':['c']})
    """

    # checking user inputs

    # assertions for test and train set inputs
    assert isinstance(X_train, pd.DataFrame), "X_train should be a DataFrame"
    assert isinstance(X_test, pd.DataFrame), "X_test should be a DataFrame"
    assert not isinstance(X_train.columns, pd.RangeIndex), \
        "column names must be strings"
    assert not isinstance(X_test.columns, pd.RangeIndex), \
        "column names must be strings"

    # assertions for dictionary input
    assert isinstance(column_dict, dict),\
        "column_dict should be a python dictionary"
    assert len(column_dict) == 2, \
        "column_dict should have 2 keys - 'numeric' and 'categorical'"

    for key in column_dict.keys():
        assert key in ['numeric', 'categorical'],\
            "column_dict keys can be only 'numeric' and 'categorical'"

    # assertions for transformation inputs
    assert isinstance(num_trans, str), "num_trans should be a string"
    assert isinstance(cat_trans, str), "cat_trans should be a string"
    assert num_trans == "standard_scaling" or num_trans == "minmax_scaling",\
        "transformation method for numeric columns can only" \
        " be 'minmax_scaling' or 'standard_scaling'"
    assert cat_trans == "onehot_encoding" or cat_trans == "label_encoding",\
        "transformation method for categorical columns can only be" \
        " 'label_encoding' or 'onehot_encoding'"

    # Check train set and test set columns are the same
    assert np.array_equal(X_train.columns, X_test.columns),\
        "X_train and X_test must have the same columns"

    for key, values in column_dict.items():
        for column in values:
            assert column in X_train.columns,\
                "columns in dictionary must be in dataframe"

    numeric = column_dict['numeric']
    categorical = column_dict['categorical']

    if cat_trans == 'onehot_encoding':

        if num_trans == "standard_scaling":
            preprocessor = ColumnTransformer(transformers=[
                ("stand_scaler", StandardScaler(), numeric),
                ("ohe", OneHotEncoder(drop='first'), categorical)],
                sparse_threshold=0)

        if num_trans == "minmax_scaling":
            preprocessor = ColumnTransformer(transformers=[
                ("minmax_scaler", MinMaxScaler(), numeric),
                ("ohe", OneHotEncoder(drop='first'), categorical)],
                sparse_threshold=0)
            # print(2)

        # Applying transformations to training data set
        X_train = pd.DataFrame(preprocessor.fit_transform(X_train),
                               index=X_train.index,
                               columns=numeric + list(
            preprocessor.named_transformers_['ohe'].get_feature_names(
                                       categorical)))

        # applying transformations to test set
        X_test = pd.DataFrame(preprocessor.transform(X_test),
                              index=X_test.index,
                              columns=X_train.columns)

    if cat_trans == "label_encoding":

        if num_trans == "standard_scaling":
            preprocessor = ColumnTransformer(transformers=[
                ("stand_scaler", StandardScaler(), numeric),
                ("ordinal", OrdinalEncoder(), categorical)],
                sparse_threshold=0)
            # print(3)

        if num_trans == "minmax_scaling":
            preprocessor = ColumnTransformer(transformers=[
                ("minmax_scaler", MinMaxScaler(), numeric),
                ("ordinal", OrdinalEncoder(), categorical)],
                sparse_threshold=0)
            # print(4)

        # ## Applying transformations to training data set
        X_train = pd.DataFrame(preprocessor.fit_transform(X_train),
                               index=X_train.index,
                               columns=numeric + categorical)

        # applying transformations to test set
        X_test = pd.DataFrame(preprocessor.transform(X_test),
                              index=X_test.index,
                              columns=X_train.columns)

    transformed_dict = {'X_train': X_train,
                        'X_test': X_test}

    return transformed_dict
