# What?

`pandas_djmodel` generates a Django model definition from a provided Pandas `DataFrame`. 
It comes handy when you need to save data from your DataFrame (being a third-party csv, xls, whatever) into your database.
This is usually a bit of a tricky and boring task. You need to figure out what db fields you should use and what parameters should be set on them. For example, `CharField` requires a `max_length` parameter so you need to check the dataset for maximum length and, as a savvy person, add some extra chars to it. That’s exactly what this little package does. So far it supports pandas’s int, float, object, bool and datetime fields.

## Usage

```
In [1]: import pandas as pd

In [2]: from pandas_djmodel import get_model_repr

In [3]: df = pd.read_csv('http://opendata.praha.eu/dataset/8dbb0d35-692c-4668-b225-c0702853c28e/resource/c4f3157a-ef07-423a-9051-7c748484d6df/download/5d88f52c-78ee-4de3-ad18-9b844737cd63-parking.csv')

In [4]: df.head()
Out[4]: 
            name        lat        lng    pr  totalNumOfPlaces
0      Běchovice  50.080800  14.597429  True                92
1         Chodov  50.032074  14.492015  True               653
2  Depo Hostivař  50.076397  14.517204  True               169
3     Holešovice  50.109318  14.441252  True                74
4        Letňany  50.125168  14.514741  True               633

In [5]: df.dtypes
Out[5]: 
name                 object
lat                 float64
lng                 float64
pr                     bool
totalNumOfPlaces      int64
dtype: object

In [6]: print get_model_repr(df)
class DFModel(models.Model):
    name = models.CharField(max_length=20) # max length was 15
    lat = models.FloatField() # min: 49.986687, max: 50.126156, mean: 50.0709247
    lng = models.FloatField() # min: 14.28977, max: 14.597429, mean: 14.4715175
    pr = models.BooleanField()
    total_num_of_places = models.PositiveSmallIntegerField() # min: 36, max: 1205, mean: 275.1


In [7]: print get_model_repr(df, col_casing='camel', indent=2, hints=False, model_name='PragueParkingLot')
class PRParkingLots(models.Model):
  name = models.CharField(max_length=20)
  lat = models.FloatField()
  lng = models.FloatField()
  pr = models.BooleanField()
  totalNumOfPlaces = models.PositiveSmallIntegerField()
```
