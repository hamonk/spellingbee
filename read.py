import pandas as pd

df = pd.read_excel('word list.xlsx', names=['word', 'definition', 'example'])

df = df[df.definition.notnull()]

print(len(df))

df.to_csv('words.csv')