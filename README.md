# HOUSE ROCKET FORECAST PROFIT

<img src="https://user-images.githubusercontent.com/87786119/154064315-b4a80be0-7888-4e09-93e5-baf9073a2c4f.png" width = "700">

## Disclaimer

This project is based on a dataset of houses sales in King Couny, US. The data is available in kaggle site. The values on the dataset are real, but the scenario used is fictitious. The source of the dataset can be viewed on the link below:

https://www.kaggle.com/harlfoxem/housesalesprediction

# 1. Business Problem

The House Rocket Co business is buy and sell houses. Basically the company buy houses with prices lower than the market price and sell it for a higher price to get profits from each operation. The problem is the portfólio size, that is too big to deal with it manualy, and because of that the company looses good business oportunities. To identifie a good operation the company need to deal with various attributes like region, sazonality, house age, the number of bathrooms, bedrooms, etc. So with a lot of information a data science solution is nedded to analyse all the attributes and find the best negotiation.

# 2. Business Assumptions

## 2.1 Data Available

The columns description of the available data is given below:

- **id** - Unique ID for each home sold
- **date** - Date of the home sale
- **price** - Price of each home sold
- **bedrooms** - Number of bedrooms
- **bathrooms** - Number of bathrooms, where .5 accounts for a room with a toilet but no shower
- **sqft_living** - Square footage of the apartments interior living space
- **sqft_lot** - Square footage of the land space
- **floors** - Number of floors
- **waterfront** - A dummy variable for whether the apartment was overlooking the waterfront or not
- **view** - An index from 0 to 4 of how good the view of the property was
- **condition** - An index from 1 to 5 on the condition of the apartment,
- **grade** - An index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 have a high quality level of construction and design.
- **sqft_above** - The square footage of the interior housing space that is above ground level
- **sqft_basement** - The square footage of the interior housing space that is below ground level
- **yr_built** - The year the house was initially built
- **yr_renovated** - The year of the house’s last renovation
- **zipcode** - What zipcode area the house is in
- **lat** - Lattitude
- **long** - Longitude
- **sqft_living15** - The square footage of interior housing living space for the nearest 15 neighbors
- **sqft_lot15** - The square footage of the land lots of the nearest 15 neighbors

## 2.2 Assumptions

For analyze the project we assume the following conditions:
- The median price of the houses is $450.000.
- All the houses are in good condition for buy and use.
- The houses with waterview are more expensive.
- The houses were builded among the years 1900 and 2015.
- Houses with date above 2014-01-01 will be nominated as new_house, and in other cases old_house
- Houses with one bedroom will be nominated as studio, two bedrooms as apartment and more than two bedrooms as house
- Will be assumed the next condition type categorization:
    - Bad: if the condition column value is lower or equals 2
    - Regular: if the condition column value is equal 3 or 4 
    - Good: if the condition column value is equal a 5 
- Will be assumed the next level categorization:
    - Level 0: price between R$0.00 and R$321.950
    - Level 1: price between R$321.950  and R$450.000
    - Level 2: price between R$450.000 and R$645.000
    - Level 3: price above R$645.000
- The sazonaltity for sale will defined based on the date provided by the dataset

# 3. Solution Strategy

## 3.1 Final Product

It will be delivered the following tools:

- Visualization tools to answer all the hypothesis.
- A table with purchase recommendation.
- A table wit sells recommendation with profits of 10% and 30%.

Note: Link in the Appendix

## 3.2 Tools

Python 3.3.0

Jupyter Notebook

Streamlit

Git and Github

## 3.3 Process
	
### 3.3.1 What houses House Rocket must buy?

- Get the data on kaggle
- Group the houses by region (zipcode)
- Find the price median by region
- Suggest the houses wich are in good condition (>3) with the corresponding profit

### 3.3.2 Once the house was purchased, what is the best moment to sell it and for what price?

- Group the houses bay region and by sazonality (summer, inter)
- Find the median price by region (zipcode)
- If price is above the median of that region, the sell price can be 10% above the purchase price
- If price is below the median of that region, the sell price can be 30% above the purchase price

# 4. Data Insights

Top three Hyphotesis:

**H1:** Houses that have waterview, are 3 times more expansive, in average, than houses without waterview.

**TRUE**

![image](https://user-images.githubusercontent.com/87786119/154069384-0ef20a52-d52f-43da-a921-cfccad520c61.png)

**H2:** Houses built among decades of 40 and 70 are cheaper than all other houses built in other decades.

**TRUE**

![image](https://user-images.githubusercontent.com/87786119/154069562-cfc220e7-b152-49c8-af84-ba461845c29f.png)

**H10:** Houses with at least two bathrooms are 10% more expensive than those with one.

**FALSE:** Houses with at least two bathrooms are about 30% more expensive than those with one.

![image](https://user-images.githubusercontent.com/87786119/154069795-47043bdf-fef8-4848-9819-d37d0b0fbe7e.png)

# 5. Business Results

It was considered two scenarios of selling:

- Selling the houses with a profit of 30%
- Selling the houses with a profit of 10%

The next table ilustrate the amount of investiment by purchasing all the houses recomended, and the forecast of revenue by selling them.

|Amount of Investment     | $ 11.523.953.411       |
|:-----------------------:|:--------------------:|
|Max Revenues             | $ 13.489.025.920,1      |
|Max Profit               | $ 1.965.072.509,1       |

# 6. Conclusion

The solution delivered is an online dashboard where the client can view both the recomendations for purchase and sell, besides it can be viewed all the portfólio houses available for sale.

# 7. Next Steps

For the next iterations of the project cycle:
- the number of houses available can be increased
- more configurations houses and attributes can be included in the decision business



# Appendix:

Link to the page of Dashboard:

 <a href="https://house-rocket-sales.herokuapp.com" target="_blank"> Dashboard Page </a>
