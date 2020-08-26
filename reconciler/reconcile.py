import pandas as pd
import requests

test_df = pd.DataFrame(
    {
        "City": ["Rio de Janeiro", "São Paulo", "São Paulo", "Natal"],
        "Inutil": ["bla", "blabla", "blablabla", "blablabla"],
    }
)


def get_query_dict(df_column):
    pass
