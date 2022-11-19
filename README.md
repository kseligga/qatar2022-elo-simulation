# qatar2022-elo-simulation

Simulation of 2022 FIFA World Cup, based on ELO ratings

1 000 000 simulations illustrated [in PL]: https://docs.google.com/spreadsheets/d/1O-9eeGCxWnFwgZy3XfEVjRs6ErOu1sMvsD51MnvRZqg/

## Modeling

**modeling_report.pdf** - Quick pdf report from what is done in all of the other modeling files. Here is written about methodology of simulation.<br>
**stspaste.txt** - pasted data from a bookmaker, used in model_making.py<br>
**model_making.py** - generates model_res.csv and bookmaker_we.csv<br>
**model_res.csv** - data from bookmaker, win expectancy and prob. of scoring n goals<br>
**bookmaker_we** - list of 48 win expectations from bookmaker in WC 2022 group stage<br>
**modeling.R** - file covering things done in a pdf report<br>

## Simulating

**copiedwebsite.txt** - copied https://eloratings.net/2022_World_Cup as html<br>
**simulation_handling.py** - simulation structure and generating result files: champs.csv, all_matches.csv, groups.csv, elo_we.csv<br>
**tournament.py** - simulation of whole tournament, runnable<br>

## Analyzing

**analysis.R** - script processing data generated in python simulation files
