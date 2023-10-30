# sqlalchemy-challenge

A climate analysis was done to examine the area of Honolulu, Hawaii.

# Analyze and Explore the Climate Data
Python and SQLAlchemy, Python, SQLAlchemy ORM queries, Pandas, and Matplotlib were used to do a basic climate analysis and data exploration of this climate database.

A precipitation analysis was done for the previous 12 months of precipitation data.
A summary statistics was created for the precipitation data.

A station analysis was done by calculating the total number of stations in the dataset, and calculating the lowest, highest, and average temperatures for the most-active station. 
The previous 12 months of temperature observation (TOBS) data was also queried. 

# Climate App
A Flask API was created to create a Climate App based on these queries. The following routes were created:
- homepage
- precipitation: analysis on the last 12 months of data
- list of stations
- dates and temperature observations for the most-active station for the previous year
- minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range
