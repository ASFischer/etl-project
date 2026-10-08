import os  
import pandas as pd

input_dir = '01-bronze-raw' # Ler arquivos da pasta bronze
output_dir = '02-silver-validated' # Salvar com parquet

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    input_path = os.path.join(input_dir, file)
    name, extension = os.path.splitext(file)
    output_path = os.path.join(output_dir, f'{name}.parquet')

    if extension.lower() == '.csv':
        df = pd.read_csv(input_path)
    elif extension.lower() == '.json': 
        try:
            df = pd.read_json(input_path)
        except ValueError:
            df = pd.read_json(input_path, lines=True)
    else:
        print(f'Arquivo {file} não suportado')
        continue


    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)
    
    df = df.drop_duplicates().reset_index(drop=True)

    # Salvar arquivo
    df.to_parquet(output_path, index=False)     
    print(f'Arquivo {file} salvo com sucesso como {output_path}')