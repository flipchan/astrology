
## Flask site for astrology

using the python library [flatlib](https://github.com/flatangle/flatlib)

### Includes:  
*  Astrology houses   
*  Zodiac signs   

## Python logic to generate your zodiac data            
```python
tiden = yy+'/'+mm+'/'+dd
date = Datetime(tiden, '17:00', '+00:00')
geo_coordinates = get_geo_cords(town,country)
if not geo_coordinates:
    return flask.render_template("advanced.html", countries=countries, error="Could not find the city")

g0,g1 = float(geo_coordinates[0]), float(geo_coordinates[1].replace('</span>', ''))
pos = GeoPos(g0, g1)
chart = Chart(date, pos, IDs=const.LIST_OBJECTS)
sun = chart.getObject(const.SUN)
```



