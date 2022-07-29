import pandas as pd
import os


def phone_fomat(phone: str):
    if phone == None or phone == '0' or phone == '無' or phone == '':
        return None
    else:
        if not isinstance(phone, str):
            return None
        phone = phone.replace('+886', '0').replace('-',
                                                   '').replace('(', '').replace(')', '')
        if not phone.startswith('0'):
            phone = '0'+phone
        return phone
    # phone_len = len(phone)
    # str_list = list(phone)
    # str_list.insert(0, ('('))
    # str_list.insert(3, ')')
    # if phone_len == 10:
    #     str_list.insert(8, '-')
    # else:
    #     str_list.insert(7, '-')
    # phone = ''.join(str_list)
    # return phone


def tidy_data(df: pd.DataFrame):
    # address process
    df['comp_address'].replace(
        to_replace="^\d+", value='', regex=True, inplace=True)
    df['comp_address'] = df['comp_address'].str.strip()
    df['fact_address'].replace(
        to_replace="^\d+", value='', regex=True, inplace=True)

    # number process
    df['comp_phone'] = df['comp_phone'].apply(phone_fomat)
    # .str.replace(
    #     "+886", '0', regex=False).str.replace('-', '').str.replace('(', '').str.replace(')', '').apply(phone_fomat)
    df['comp_fax'] = df['comp_fax'] .apply(phone_fomat)
    # .str.replace(
    #     "+886", '0', regex=False).str.replace('-', '').str.replace('(', '').str.replace(')', '').apply(phone_fomat)
    df['fact_phone'] = df['fact_phone'].apply(phone_fomat)
    # .str.replace(
    #     "+886", '0', regex=False).str.replace('-', '').str.replace('(', '').str.replace(')', '')
    df['fact_fax'] = df['fact_fax'].apply(phone_fomat)
    # .str.replace(
    #     "+886", '0', regex=False).str.replace('-', '').str.replace('(', '').str.replace(')', '')
    return df


if __name__ == '__main__':
    root = 'data/tw'
    tw_excel_paths = ['tami-tw.xlsx', 'tmba-tw.xlsx',
                      'twma_tw.xlsx', 'tfpma-tw.xlsx', 'pack-tw.xlsx']
    new_df = pd.DataFrame()
    for excel_path in tw_excel_paths:
        df = pd.read_excel(os.path.join(root, excel_path))
        df = tidy_data(df)
        new_df = new_df.append(df)
    new_df.to_excel('comp_list-tw.xlsx', index=False)
    root = 'data/en'
    tw_excel_paths = ['tami-en.xlsx', 'tmba-en.xlsx',
                      'twma_en.xlsx', 'tfpma-en.xlsx', 'pack-en.xlsx']
    new_df = pd.DataFrame()
    for excel_path in tw_excel_paths:
        df = pd.read_excel(os.path.join(root, excel_path))
        df = tidy_data(df)
        new_df = new_df.append(df)
    new_df.to_excel('comp_list-en.xlsx', index=False)
