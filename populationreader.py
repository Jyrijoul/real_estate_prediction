import pandas as pd
import geopandas as gpd
from shapely.geometry import Point,Polygon
import numpy as np

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
df=gpd.read_file('Rahvaarv_kokku.kml', driver='KML')

#process text so population for each area so population is it's own metric
df['population']=df['Name'].str.split(' - ').str[1].str.replace('<','').astype(float)

houses=pd.read_csv('dataset_sharehouses.csv')
idk=[]
for i in range(houses.shape[0]):
    #if location exists for property
    if (type(houses['Location'][i])!=type(np.nan)):
        # if location doesn't exist on map
        if df[df['geometry'].contains(Point(np.flip(np.fromstring(houses['Location'][i],sep=','))))]['population'].shape[0]==0:
            idk.append(0)
        else:
            idk.append(df[df['geometry'].contains(Point(np.flip(np.fromstring(houses['Location'][i],sep=','))))]['population'].item())
    else: 
        idk.append(0)
houses['population']=idk

houses.to_csv('dataset_sharehouses_with_population.csv')