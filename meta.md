# Meta

### neos.csv
*   pdes - the primary designation of the NEO. This is a unique identifier in the database, and its "name" to computer systems.
*   name - the International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
*   pha - whether NASA has marked the NEO as a "Potentially Hazardous Asteroid," roughly meaning that it's large and can come quite close to Earth.
*   diameter - the NEO's diameter (from an equivalent sphere) in kilometers.

### cad.json
*   des - primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
*   orbit_id - orbit ID
*   jd - time of close-approach (JD Ephemeris Time)
*   cd - time of close-approach (formatted calendar date/time, in UTC)
*   dist - nominal approach distance (au)
*   dist_min - minimum (3-sigma) approach distance (au)
*   dist_max - maximum (3-sigma) approach distance (au)
*   v_rel - velocity relative to the approach body at close approach (km/s)
*   v_inf - velocity relative to a massless body (km/s)
*   t_sigma_f - 3-sigma uncertainty in the time of close-approach (formatted in days, hours, and minutes; days are not included if zero; example "13:02" is 13 hours 2 minutes; example "2_09:08" is 2 days 9 hours 8 minutes)
*   h - absolute magnitude H (mag)

### main.py

```bash
usage: main.py [-h] [--neofile NEOFILE] [--cadfile CADFILE] {inspect,query,interactive} ...

Explore past and future close approaches of near-Earth objects.

positional arguments:
  {inspect,query,interactive}

optional arguments:
  -h, --help            show this help message and exit
  --neofile NEOFILE     Path to CSV file of near-Earth objects.
  --cadfile CADFILE     Path to JSON file of close approach data.
```