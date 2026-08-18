import pandas as pd
from pathlib import Path

def _read_single_bee(dir: Path, bee: str):
    df = pd.read_excel(dir / f"{bee}_infravermelho.xlsx")
    df = df.T.reset_index()

    columns = df.iloc[0].tolist()
    if bee == 'jatai':
        columns[0:3] = ['Collection_date', 'Bee', 'Producer_idx']
    elif bee == 'mandacaia':
        columns[0:3] = ['Bee', 'Collection_date', 'Producer_idx']
    else:
        raise ValueError(f"Unknown bee type: {bee}")

    df.columns = columns
    df = df[1:].copy()
    
    # Extrai o número e mantém como inteiro. Os scripts de visualização cuidam do formato.
    df['Collection_day'] = df['Collection_date'].str.extract(r'(\d+)º').astype(int)
    df['Producer_idx'] = df['Producer_idx'].str.replace('Produtor ', '', regex=False).astype(int)
    
    df.drop(columns=['Collection_date'], inplace=True)
    df['Bee'] = bee  # Atribuição escalar direta, sem list comprehension

    return df

def read_excel(dir: Path, bee: str):
    if bee == 'ambas':
        df_jatai = _read_single_bee(dir, 'jatai')
        df_mandacaia = _read_single_bee(dir, 'mandacaia')
        # Concatena os dois DataFrames e redefine os índices (16 + 16 = 32 linhas)
        df_concat = pd.concat([df_jatai, df_mandacaia], ignore_index=True)
        return df_concat
    else:
        return _read_single_bee(dir, bee)