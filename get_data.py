import requests
import pandas as pd

def get_data(cep):
    endpoint = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(endpoint)
    cep_info = response.json()
    return cep_info


users_path = '01-bronze-raw/users.csv'
users_df = pd.read_csv(users_path)

cep_list = users_df['cep'].tolist() # to list é uma função que transforma o dataframe em uma lista

cep_info_list = []

for cep in cep_list:
   cep_clean = cep.replace('-', '')
   cep_info = get_data(cep_clean)
   print(cep_info)
   # Se conter erro, pular para a próxima iteração
   if 'erro' in cep_info:
      continue
   cep_info_list.append(cep_info) 

cep_info_df = pd.DataFrame(cep_info_list)
cep_info_df.to_csv('01-bronze-raw/cep_info.csv', index=False)