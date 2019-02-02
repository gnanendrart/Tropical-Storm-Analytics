# Tropical-Storm-Analytics
The NOAA National Hurricane Center has several databases available. We’re going to work with a historical one called “HURDAT2”. From http://www.nhc.noaa.gov/data/#hurdat we can download two data files (Pacific and Atlantic) in a non-standard CSV/fixed-width format. The strangeness is due to the mixture of two interrelated line formats, the lack of column headers, and many missing data values (-99 & -999). There are accompanying PDFs on that same webpage that describe the data format in fine detail.

I have started the analysis by first finding more about the data by finding some basic information about the storms present and the exploring the data. 
For the exploratory analysis I computed and printed out details like:
- Storm system ID, Name and Date range recorded for the storm
- The highest Maximum sustained wind (in knots) and when it first occurred (date & time). This was performed numerically as the "Record Identifier" is not available for all the data.
- The total pressure change in millibars and No of times of Landfall for a storm.
- Total number of storms tracked per year and Total number of hurricane-level storms tracked per year. It was calculated using the condition maximum wind >= 64kts.

Then with the help of "PyGeodesy" library, the total distance the storm was tracked in nautical miles is calculated. The storm propagation and the mean and maximum propagation speeds per storm is calculated.

The relative Storm Engines are calculated:
- The relative power as maximum_sustained_wind for each data row is calculated.
- The relative storm energy and the TRSE (total relative storm energy) is calculted. 
Storm energy is calculted by the following manner: Energy = Power * Time. Multiply that power above by the interval of hours between the current and previous data row
- Using only the 64-kt radii measures (the last 4 columns of data), compute the approximate surface area covered by hurricane-speed winds to get Hurricane surface area.
