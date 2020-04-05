from datetime import datetime as dt
import numpy as np
import os
import pandas as pd
from uszipcode import SearchEngine

class DataLoader(object):
    
    def __init__(self):
        
        pass        

    def load_local_dir(self):

        dfs = {}
        path = '../../data/'
        
        for file in os.listdir(path):
            full_path = f'{path}{file}'
            ext = file.split('.')[-1]
            if ext == "csv":
                dfs[file.split(".")[0]] = pd.read_csv(full_path)
                
        self.zip = dfs["tests-by-zcta"]
        self.df_zip = self._process_zip_df()
        
        return dfs


    def fetch_virus_data(self):

        virus_ds_path = '../../data/'
        download_root = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/'
        endpoints = ['boro.csv','by-age.csv','by-sex.csv', 
                         'case-hosp-death.csv', 'tests-by-zcta.csv']

        urls = {"-".join(endpoint.split('.')[:-1]): download_root + endpoint 
                for endpoint in endpoints}

        date = dt.now().date()
        date_folder_path = "../../data/" + str(date) + "/"
        dfs = {k: pd.read_csv(v) 
               for k, v  in urls.items()}

        if os.path.exists(date_folder_path):
            [df.to_csv(date_folder_path + k + '.csv') 
             for k, df  in dfs.items()]
        else:
            os.mkdir(date_folder_path)
            [df.to_csv(date_folder_path + k + '.csv') 
             for k, df  in dfs.items()]

        self.dfs = dfs
        self.zip = dfs["tests-by-zcta"]
        self.df_zip = self._process_zip_df()
        
        return dfs
    

    def _get_lat_lng(self, zip_code):

        try: 
            search = SearchEngine(simple_zipcode=True)
            zipcode = search.by_zipcode(str(int(zip_code)))
            zip_code_dict = zipcode.to_dict()
            lat = zip_code_dict['lat']
            lng = zip_code_dict['lng']

            return [lat, lng]
        except:
            return [0, 0]    
        
    def _get_coords(self):
        coords = {}
        for code in self.zip.MODZCTA:
            if np.isnan(code):
                continue
            code = str(int(code))
            coords[code] = self._get_lat_lng(code)
        return coords
    
    def _process_zip_df(self):
        
        coords = self._get_coords()
        data = self.zip.drop(index=0)
        self.zip['zip_code'] = data.MODZCTA.astype(int).astype(str)
        cases_by_zip = {}
        for k, coord in coords.items():

            lat = coord[0]
            lng = coord[1]

            total_ref = self.zip.Total.loc[self.zip['zip_code'] == k]
            total = total_ref.values[0]
            positive = self.zip.Positive.loc[self.zip['zip_code'] == k].values[0]
            cases_by_zip[k] = [total, positive]

        df_zip = pd.DataFrame(cases_by_zip).T
        df_zip.rename(columns={0: 'tests', 1: 'positives'}, inplace=True)
        df_zip.index.rename('zip', inplace=True)
        df_zip['zip'] = df_zip.index
        df_zip['percents'] = df_zip.positives / df_zip.tests
        df_zip['test_density'] = df_zip.tests / df_zip.tests.max()
        df_zip['weighted_positivity'] = df_zip.percents * df_zip['test_density']
        df_zip.index = np.arange(len(df_zip))
        return df_zip