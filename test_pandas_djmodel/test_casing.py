#!/usr/bin/env python
# coding=utf-8
import pytest


from pandas_djmodel.djmodel import snake_case, camel_case

# props to Don Marquis http://donmarquis.com/reading-room/song-of-mehitabel/


@pytest.mark.parametrize("test_input,expected", [
    ('my youth i shall never forget', 'my_youth_i_shall_never_forget'),
    ('butThereSNothingIReallyRegret', 'but_there_s_nothing_i_really_regret'),
    ('wotthehell.wotthehell', 'wotthehell_wotthehell'),
    ('there_s    a.dance in the old dame yet', 'there_s____a_dance_in_the_old_dame_yet'),
    ('toujours_gai_toujours_gai', 'toujours_gai_toujours_gai'),
    ('TOUJOURS GAI TOUJOURS GAI', 'toujours_gai_toujours_gai'),

])
def test_snake_case(test_input, expected):
    assert snake_case(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [
    ('my youth i shall never forget', 'myYouthIShallNeverForget'),
    ('butThereSNothingIReallyRegret', 'butThereSNothingIReallyRegret'),
    ('wotthehell.wotthehell', 'wotthehellWotthehell'),
    ('there_s    a.dance in the old dame yet', 'thereSADanceInTheOldDameYet'),
    ('toujours_gai_toujours_gai', 'toujoursGaiToujoursGai'),
    ('TOUJOURS GAI TOUJOURS GAI', 'toujoursGaiToujoursGai'),
])
def test_camel_case(test_input, expected):
    assert camel_case(test_input) == expected
