# LIBR559C-Nutrition
This is the final project for LIBR 559C of UBC iSchool
contributed by: Ruiqi Chen, Can (Claire) Cui, Wendy Lu 

## Run the website locally

1. clone the folder to the local machine
2. run in command line
   `$pip install -r requirements.txt`

3. Go to the main folder 
`$python run.py`

4. Access the website at
http://localhost:5000/

## Introduction
   The project is built using the python library **Flask**.
   
   The website is designed for the age to calculate nutrition in meal, and recommend future meals based on the meal they take.
   
   ##Main functions:
###Nutrition Calculation of the recipe
We used data collected above to look up for the amount of the nutrition in a recipe. Index numbers were given to each recipe and listed on the webpage, which are identical to the data in our database. 
We used form to acquire the data that the user have input. When the user click submit, the webpage will redirect to the second webpage, where will show the nutrition in the meal.
The function was realized using several for loop and if judgement to look up data in the file recipe_new.xml. Two dictionaries were used to store the total amount of Vitamins and Minerals independently. 
###Nutricion that the user lack
A standard dictionary of the amount of nutrition that males and females older than 65 need for each day was given. The amount of nutritions calculated according to the recipe were used to be compared with the standard dictionary, then the amount that the user lack could be calculated. 
###Recommendations of meal containing appropriate nutrition
After the amounts of nutrition that the user lack are calculated, we use that amounts divide the standard amount that a person need, then according to the portion and amount to recommend meals for the user. Currently, the algorithm we used to calculate the recommendation meal was to filter the meal with the largest amount of the nutrition that the user lack, and select one meal for each nutrition.
####Online Link:
https://libr559c-nutrition.herokuapp.com/
(still need to be fixed)
