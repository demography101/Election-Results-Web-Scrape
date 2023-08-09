#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 20:28:45 2023

@author: corinamccullough
"""

import pandas as pd
import lxml
import re

# Voter Data
wikiurl = "https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Florida"

df_fl = pd.read_html(wikiurl)

county_vote = df_fl[38]

county_vote

# Republican Votes
rep_vote = county_vote[['County', 'Donald TrumpRepublican']].copy()

rep_vote.columns = rep_vote.columns.droplevel()

rep_vote = rep_vote.rename(columns={'#': 'Total_Votes', '%': 'Perct_Votes'})

rep_vote.insert(1, "Political_Party", "Republican", True)
rep_vote.insert(2, "Candidates", "Donald Trump and Mike Pence", True)


# Democrat Votes
dem_vote = county_vote[['County', 'Joe BidenDemocratic']].copy()

dem_vote.columns = dem_vote.columns.droplevel()

dem_vote = dem_vote.rename(columns={'#': 'Total_Votes', '%': 'Perct_Votes'})

dem_vote.insert(1, "Political_Party", "Democrat", True)
dem_vote.insert(2, "Candidates", "Joe Biden and Kamala Harris", True)


# FIPS codes
fipsurl = "https://en.wikipedia.org/wiki/List_of_United_States_FIPS_codes_by_county"

fips_fl = pd.read_html(fipsurl)
fips = fips_fl[1]

fips.rename(columns = {'State or equivalent':'State'}, inplace = True)

fips['County'] = fips['County or equivalent'].apply(lambda x : re.findall(r"[\w']+",x)[0])

fips = fips.drop('County or equivalent', axis=1)

fips = fips.query("State == 'Florida'")

fips

# State Abbreviations
abbvurl = "https://simple.wikipedia.org/wiki/List_of_U.S._states_by_traditional_abbreviation"

abbv = pd.read_html(abbvurl)

abbv = abbv[0]

abbv.rename(columns = {'Otherabbreviations':'Abbreviations'}, inplace = True)

abbv = abbv.drop('Traditionalabbreviation', axis=1)

abbv


# Merge Dataframes
fl_vote = pd.concat([rep_vote, dem_vote])

fl_county = pd.merge(left=abbv, right=fips, left_on='State', right_on='State')

county_votes = pd.merge(fl_vote, fl_county, left_index=True, right_index=True)

county_votes.to_csv("FL County 2020 Presidential Results.csv") 



# Reference Code:
# https://www.askpython.com/python-modules/pandas/read-html-tables
# https://stackoverflow.com/questions/57256760/extract-first-word-for-each-row-in-a-column-under-multiple-conditions











 





















