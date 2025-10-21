# Title: Importando dados de um arquivo CSV da web

# Importando dados de um arquivo CSV da web 
# Salvo o Arquivo em um diretório local
# Renomeando as colunas do DataFrame
# Salvando o DataFrame em um novo arquivo CSV



# Import package
from urllib.request import urlretrieve

# Import pandas
import pandas as pd

# Assign URL of file
url = 'https://raw.githubusercontent.com/luasampaio/datasets/main/customers.csv'

# Save file locally with the correct name
urlretrieve(url, 'customers.csv')

# Read file into a DataFrame
df = pd.read_csv('customers.csv', sep=',')
#print(df.head())

# Renomear as colunas 
df = df.rename(columns={
    'customer_id': 'identificador',
    'first_name': 'primeiroNome',
    'last_name': 'segundoNome',
    'city': 'Cidade',
    'state': 'Estado',
    'zip_code': 'CEP',
    'street': 'Av/Rua',
})

# Display the first two rows after renaming
print(df.head(100))

# save the DataFrame to a new CSV file
df.to_csv('customers.csv', index=False)


