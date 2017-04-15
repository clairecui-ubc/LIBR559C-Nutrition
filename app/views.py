from flask import render_template, flash, redirect,request,url_for,session
from app import app
from .forms import IndexNumber, Recommendation
import xml.etree.ElementTree as ET

#Import the data from the XML file:
xmlstring=(open('recipe_new.xml')).read()
parser = ET.XMLParser(encoding="utf-8")  #Using Parser to format the data
root = ET.fromstring(xmlstring,parser=parser)

# index view function suppressed for brevity
# Three pages: homepage,nutrition_amount, recommend_meal

#-------------------------#
#------The first page-----#
#------Home Page ---------#
#-------------------------#

@app.route('/',methods = ['GET', 'POST'])
@app.route('/index',methods = ['GET', 'POST'])

def homepage():
    
    #Forms are defined in the forms.py   
    form = IndexNumber() 
             
    # ---If the user have input index number in the form,--#
    # ---Save the number to the session--------------------#
    # ---Redirect to the assessment page ------------------#
    if request.method == 'POST':
        if form.validate():
            session['index1']=form.index1.data
            session['index2']=form.index2.data
            session['index3']=form.index3.data
            session['index4']=form.index4.data
            session['index5']=form.index5.data
            session['gender']=form.gender.data
            return redirect(url_for('nutrition_amount'))
        
        # ----If the number user input is wrong, ------#
        # -print the message and link back to homepage-#
        else:
            flash('All fields are required.')
            return render_template("home.html",
                title = 'Home',
                form=form)
    
    #---If the route is access directly from the url,---#
    #---get to homepage --------------------------------#    
    elif request.method == 'GET':
        flash('haha')
        return render_template("home.html",
            title = 'Home',
            form=form)
        
#--------------------------#
#------The Second page-----#
#------Assessment ---------#
#--------------------------#               

@app.route('/yournutrition', methods=['GET', 'POST'])

def nutrition_amount(): 
    app.app_context()
    #---Unify the unit of the nutrition---#
    nutrition_unit={'Niacin': 'mg', 'Vitamin E (Alpha Tocopherol)': 'mg', 'Sodium': 'mg', 'Beta Tocopherol': 'mg', 'Vitamin D': 'IU', 'Selenium': 'mcg', 'Thiamin': 'mg', 'Folate': 'mcg', 'Vitamin B12': 'mcg', 'Choline': 'mg', 'Dietary Folate Equivalents': 'mcg', 'Beta Carotene': 'mcg', 'Potassium': 'mg', 'Lutein+Zeaxanthin': 'mcg', 'Lycopene': 'mcg', 'Vitamin B6': 'mg', 'Pantothenic Acid': 'mg', 'Folic Acid': 'mcg', 'Phosphorus': 'mg', 'Retinol': 'mcg', 'Manganese': 'mg', 'Betaine': 'mg', 'Vitamin C': 'mg', 'Beta Cryptoxanthin': 'mcg', 'Riboflavin': 'mg', 'Magnesium': 'mg', 'Iron': 'mg', 'Retinol Activity Equivalent': 'mcg', 'Vitamin K': 'mcg', 'Fluoride': 'mcg', 'Copper': 'mg', 'Gamma Tocopherol': 'mg', 'Calcium': 'mg', 'Vitamin A': 'IU', 'Food Folate': 'mcg', 'Alpha Carotene': 'mcg', 'Zinc': 'mg', 'Delta Tocopherol': 'mg'}
    
    form=Recommendation()
    
    #----Index Number is aquired from the form in homepage-----------------#
    #----Only the first column is required, so the others might be empty---#
    #----Only save indexes that are not empty------------------------------#
    indexes=[session['index1']]
    if session['index5']!=None:
        indexes=[session['index1'],session['index2'],session['index3'],session['index4'],session['index5']]
    elif session['index4']!=None:
        indexes=[session['index1'],session['index2'],session['index3'],session['index4']]
    elif session['index3']!=None:
        indexes=[session['index1'],session['index2'],session['index3']]
    elif session['index2']!=None:
        indexes=[session['index1'],session['index2']]
    
    gender=session['gender']
    
    #-------Use dictionaries to store the total amount of nutrition--------#
    sum_vitamins={}
    sum_minerals={}
    
    for index in indexes:
        for nutrition in root[index-1]:  # Use the index number to locate nutrition facts of recipe
            if nutrition.tag=='Vitamins':
            
            #---Calculate Vitamins and Minerals Independently---#
                for child_of_nutrition in nutrition:
                    if child_of_nutrition.attrib['amount']!='~' and child_of_nutrition.attrib['amount']!='0.0' :
                        #print child_of_nutrition.attrib['name'],child_of_nutrition.attrib['amount'],child_of_nutrition.attrib['unit']
                        if sum_vitamins.has_key(child_of_nutrition.attrib['name']):
                            sum_vitamins[child_of_nutrition.attrib['name']]=float(sum_vitamins[child_of_nutrition.attrib['name']])+float(child_of_nutrition.attrib['amount'])

                        else:
                            sum_vitamins[child_of_nutrition.attrib['name']]=float(child_of_nutrition.attrib['amount'])
                            
            elif  nutrition.tag=='Minerals':
                 for child_of_nutrition in nutrition:
                    if child_of_nutrition.attrib['amount']!='~' and child_of_nutrition.attrib['amount']!='0.0' :
                        #print child_of_nutrition.attrib['name'],child_of_nutrition.attrib['amount'],child_of_nutrition.attrib['unit']
                        if sum_minerals.has_key(child_of_nutrition.attrib['name']):
                            sum_minerals[child_of_nutrition.attrib['name']]=float(sum_minerals[child_of_nutrition.attrib['name']])+float(child_of_nutrition.attrib['amount'])
                        else:
                            sum_minerals[child_of_nutrition.attrib['name']]=float(child_of_nutrition.attrib['amount'])
    
    #---The need for nutritions are stored in need_nutrition---#
    need_nutrition={
        'male_minerals':{'Copper': 900, 'Zinc': 11, 'Sodium': 2300, 'Selenium': 55, 'Manganese': 2.3, 'Calcium': 1000, 'Magnesium': 420, 'Iron': 8, 'Potassium': 4700, 'Fluoride': 4, 'Phosphorus': 700},
        'male_vitamins':{'Niacin': 14, 'Vitamin E (Alpha Tocopherol)': 15, 'Thiamin': 1.1, 'Folate': 400, 'Vitamin C': 75, 'Vitamin B12': 2.4, 'Vitamin A': 900, 'Riboflavin': 1.1, 'Choline': 550, 'Vitamin D': 15, 'Vitamin K': 120, 'Vitamin B6': 1.5, 'Pantothenic Acid': 5},
        'female_vitamins':{'Niacin': 18, 'Vitamin E (Alpha Tocopherol)': 15, 'Thiamin': 1.4, 'Folate': 400, 'Vitamin C': 85, 'Vitamin B12': 2.4, 'Vitamin A': 700, 'Riboflavin': 1.4, 'Choline': 425, 'Vitamin D': 15, 'Vitamin K': 90, 'Vitamin B6': 1.9, 'Pantothenic Acid': 5},
        'female_minerals':{'Copper': 1000, 'Zinc': 8, 'Sodium': 2300, 'Selenium': 55, 'Manganese': 1.8, 'Calcium': 1200, 'Magnesium': 320, 'Iron': 18, 'Potassium': 4700, 'Fluoride': 3, 'Phosphorus': 700}
    }
    
    #----Lack of vitamins----#
    
    lack_vitamin={}
    for key, value in need_nutrition[gender+'_vitamins'].items():
        #--If the type of nutrition intake is in the need_nutrition list--#
        #--Calculate the lack of nutrition using the difference  ---------#
        if key in sum_vitamins.keys():
            lack_vitamin[key]=value-sum_vitamins[key]
        #--Otherwise the lack of nutrition equals to the total needs------#
        else:
            lack_vitamin[key]=value
    
    #-----Lack of minerals----#
    
    lack_mineral={}
    for key, value in need_nutrition[gender+'_minerals'].items():
        if key in sum_minerals.keys():
            lack_mineral[key]=value-sum_minerals[key]
        else:
            lack_mineral[key]=value
    
    #----Also, calculate the portion of lack in nutrition----#
    #----portion=lack_nutritions/need_nutrtions--------------#
    lack_nutrition_portion={}
    for key,value in lack_vitamin.items():
        if value>0:
            lack_nutrition_portion[key]=float(value)/need_nutrition[gender+'_vitamins'][key]
    for key,value in lack_mineral.items():
        if value>0 :
            lack_nutrition_portion[key]=float(value)/need_nutrition[gender+'_minerals'][key]
    
    
    #----If the user click "recommendation" bottom,------#
    #----Redirect to recommendations page ---------------#
    
    if request.method == 'POST' and form.validate():
    
        #-----Recommend the recipe with the most amount of the nutrition-----#
       
        recommendations={}
        for key,value in lack_nutrition_portion.items():
            if  key in lack_mineral.keys() and value>0:        
                list_nutrition=[float(x.attrib['amount'])for x in root.findall('./Meal/Minerals/Row/[@name="%s"]'%key)]
                recommendations[key]={'meal':root[list_nutrition.index(max(list_nutrition))].attrib['name'],'amount':max(list_nutrition)}
            
            elif value>0:
                list_nutrition=[float(x.attrib['amount']) for x in root.findall('./Meal/Vitamins/Row/[@name="%s"]'%key)]
                recommendations[key]={'meal':root[list_nutrition.index(max(list_nutrition))].attrib['name'],'amount':max(list_nutrition)}
        
        session['recommendations']=recommendations
            
        
        return redirect(url_for('recommend_meal'))
            
    
    else:
        return render_template('Assessment.html',
            title='Your Nutrtion Today',
            sum_minerals=sum_minerals,
            sum_vitamins=sum_vitamins,
            nutrition_unit=nutrition_unit,
            lack_mineral=lack_mineral,
            lack_vitamin=lack_vitamin,
            form=form)
        
@app.route('/recommendation')

def recommend_meal():
    nutrition_unit={'Niacin': 'mg', 'Vitamin E (Alpha Tocopherol)': 'mg', 'Sodium': 'mg', 'Beta Tocopherol': 'mg', 'Vitamin D': 'IU', 'Selenium': 'mcg', 'Thiamin': 'mg', 'Folate': 'mcg', 'Vitamin B12': 'mcg', 'Choline': 'mg', 'Dietary Folate Equivalents': 'mcg', 'Beta Carotene': 'mcg', 'Potassium': 'mg', 'Lutein+Zeaxanthin': 'mcg', 'Lycopene': 'mcg', 'Vitamin B6': 'mg', 'Pantothenic Acid': 'mg', 'Folic Acid': 'mcg', 'Phosphorus': 'mg', 'Retinol': 'mcg', 'Manganese': 'mg', 'Betaine': 'mg', 'Vitamin C': 'mg', 'Beta Cryptoxanthin': 'mcg', 'Riboflavin': 'mg', 'Magnesium': 'mg', 'Iron': 'mg', 'Retinol Activity Equivalent': 'mcg', 'Vitamin K': 'mcg', 'Fluoride': 'mcg', 'Copper': 'mg', 'Gamma Tocopherol': 'mg', 'Calcium': 'mg', 'Vitamin A': 'IU', 'Food Folate': 'mcg', 'Alpha Carotene': 'mcg', 'Zinc': 'mg', 'Delta Tocopherol': 'mg'}
    
    recommendations=session['recommendations']
    
    return render_template('Recommendation.html',
        title='Recommendation',
        recommendations=recommendations,
        nutrition_unit=nutrition_unit
        )
