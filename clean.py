import pandas as pd

def clean_data(df, youtube_channel_name,error_df):
    print('------------------------------------------')
    print('Cleaning data.....')

    # Drop column 'Unnamed: 0' if the dataframe has one
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)
    
    # error_df = df[df.Time=='0']
    # error_df.to_csv(f'{youtube_channel_name}_error.csv', encoding='utf-8-sig', index=False)

    # df.drop(df[df.Time=='0'].index, inplace=True)
    # Format Time column
    df.loc[:, 'Time'] = df.Time.apply(lambda x: round(float(x.split(':')[0]) + (float(x.split(':')[1])/60), 2))
    
    # Format Date column
    df.loc[:, 'Date'] = df.Date.apply(lambda x: x.replace('Streamed live on ', ''))
    df.loc[:, 'Date'] = df.Date.apply(lambda x: x.replace('Premiered ', ''))
    df.Date = pd.to_datetime(df.Date)

    # Format View column
    df.View = pd.to_numeric(df.View.str.replace(',', ''))

    
    # Use try-expect because if the column doesn't have that format it wouldn't cause errors
    try:
        df.Like = df.Like.apply(lambda x: x.replace('K', '00') if '.' in x else x.replace('K', '000'))
        df.Like = df.Like.apply(lambda x: x.replace('.', '')).astype('int64')
    except:
        pass
    try:
        df.Like = df.Like.apply(lambda x: x.replace('M', '00000') if '.' in x else x.replace('K', '000000'))
        df.Like = df.Like.apply(lambda x: x.replace('.', '')).astype('int64')
    except:
        pass

    # Format Dislike column
    try:
        df.Dislike = df.Dislike.apply(lambda x: x.replace('K', '00') if '.' in x else x.replace('K', '000'))
        df.Dislike = df.Dislike.apply(lambda x: x.replace('.', '')).astype('int64')
    except:
        pass
    try:
        df.Dislike = df.Dislike.apply(lambda x: x.replace('M', '00000') if '.' in x else x.replace('K', '000000'))
        df.Dislike = df.Dislike.apply(lambda x: x.replace('.', '')).astype('int64')
    except:
        pass

    if str(df.Comment.dtype) == 'object':
        df.Comment = pd.to_numeric(df.Comment.str.replace(',', ''))

    df.to_csv(f'{youtube_channel_name}_full.csv', encoding='utf-8-sig', index=False)
    
