#! python3
"""Pull trading data from Cryptocompare and graph trailing 3-month price/volume activity"""

# TODO: add webhook to run script when Slackbot receives a message (Flask)
# TODO: implement testing

from datetime import datetime, timedelta
from turtle import bgcolor, fillcolor
import pandas as pd
import numpy as np
import requests

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# retrieve dataframe
def retrieve_data(
    symbol, comparison_symbol="USD", limit=1, aggregate=1, allData="true"
):
    """Note that raw dataframe includes empty data rows for periods where the token didn't exist. Not an issue for graphing trailing 3-months, but will skew metric calculations for full period."""
    url = f"https://min-api.cryptocompare.com/data/histoday?fsym={symbol}&tsym={comparison_symbol}&limit={limit}&aggregate={aggregate}&allData={allData}&tryconversion=true"
    page = requests.get(url)
    data = page.json()["Data"]
    df = pd.DataFrame(data)
    df.name = symbol.upper()  # storing input symbol for later use chart titles
    return df


def format_data(df):
    """
    Strip dataframe to required columns and format times from unix to m/d/Y.
    """
    df["time"] = [datetime.fromtimestamp(d) for d in df.time]
    df["time"] = df["time"] + pd.Timedelta(
        hours=6  # toggle this depending on timezone.
    )
    df["time"] = pd.to_datetime(df.time)
    df["time"] = df["time"].dt.strftime("%m/%d/%Y")
    return df


def chart(df):
    """Create combined line+bar chart from dataframe."""
    SYM = df.name  # for use in axes titles
    df = df.tail(93)

    # set up plotly figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # close price line chart
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["close"],
            line=dict(color="blue", width=5),
            marker_color="blue",
            name=f"{SYM} 'Closing Price'",
            opacity=1,
            showlegend=True,
        ),
    )

    # volume bar chart as secondary axis
    fig.add_trace(
        go.Bar(
            x=df["time"],
            y=df["volumeto"],
            marker_color="red",
            name="Volume",
            opacity=0.8,
            showlegend=True,
        ),
        secondary_y=True,
    )

    # TODO: add transparency to bars so that line is more visible when they overlap
    fig.update_layout(
        yaxis=dict(
            title=dict(text=f"<b>{SYM} Price (USD)</b><br>", font=dict(size=24)),
            tickprefix="$",
            tickformat=",",
            title_standoff=50,
            gridcolor="Black",
            range=[0, df["close"].max()],
        ),
        yaxis2=dict(
            title=dict(text=f"<b>{SYM} Volume (USD)</b><br>", font=dict(size=24)),
            tickprefix="$",
            tickformat=",",
            title_standoff=50,
            showgrid=False,
        ),
        xaxis=dict(dtick=4, tickangle=-45, title_standoff=50),
        legend=dict(
            orientation="h",
            x=0.4,
            traceorder="reversed",
            font=dict(size=24),
        ),
        font_family="Calibri",
        font_color="Black",
        font_size=20,
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=50, b=0, t=25, pad=0))
    
    outfile = "crypto/graphs/" + SYM + ".html"
    fig.write_html(outfile, include_plotlyjs='cdn')

    
    



def main(SYM="ETH"):
    df = retrieve_data(SYM)
    df = format_data(df)
    chart(df)


if __name__ == "__main__":
    main()
