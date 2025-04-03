from fasthtml.common import *
from datetime import date, datetime
from monsterui.all import *
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

app, rt = fast_app(hdrs=Theme.blue.headers())

df = pd.read_csv('search_results.csv')
unique_queries = df['query'].unique().tolist()
def pandas_to_monster_table(df):
    "Convert a pandas DataFrame to a nicely styled MonsterUI table."
    header = Tr(*[Th(col) for col in df.columns] + [Th("Actions")])

    rows = []
    for _, row in df.iterrows():
        cells = []
        for col in df.columns:
            value, style = row[col], None
            if pd.api.types.is_numeric_dtype(df[col]):
                style = f"background-color: {'#d4edda' if int(value) == 1 else '#f8d7da'}"
            cells.append(Td(str(value), style=style if col == 'rating' else None))
        cells.append(Td(
            DivLAligned(
                UkIconLink('thumbs-up', hx_post=f'/save?ankihub_id={row["ankihub_id"]}&rating=1'), 
                UkIconLink('thumbs-down', hx_post=f'/save?ankihub_id={row["ankihub_id"]}&rating=0'))
        ))
        rows.append(Tr(*cells))
    
    return Card(
        Table(
            Thead(header),
            Tbody(*rows),
            cls=f"{TableT.striped} {TableT.hover}"))

@rt
def index():
    return Ul(*[Li(A(q, href=f'/search?query={q}', cls=AT.primary)) for q in unique_queries], cls=ListT.bullet)

@rt('/search')
def search(query: str):
    filtered_df = df[df['query'] == query].drop(['anki_id'], axis=1)
    return Titled(
        f"Search Results for '{query}'",
        P(f"Showing {len(filtered_df)} results", cls=TextPresets.muted_sm),
        pandas_to_monster_table(filtered_df))

serve()