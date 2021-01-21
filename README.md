# Predicting Oil and Gas Stocks - Final Project
LINK TO HEROKU: https://final-project-stage.herokuapp.com/


## Background
The goal of this algorithm is to accurately predict stock trends to help determine the best time one should buy or sell. The data our team used to create the models does not come close to the amount of data that large companies spend large sums of money each year for millions of lines of data to help structure their predictions models.  However, we hope that the small sampling demonstrated here today will provide one with a sense of what goes into making stock predictions and all the related intricacies. Here we present you with 10 Oil and Gas stocks. We wanted to focus on stocks in one category and understand if these may not suit your interests. Were we to have chosen a random sampling across various categories, our predictions models would not have yielded results as accurate.


![](https://github.com/JonZagorski/final-project/blob/main/screenshots/Graph1.png)![](https://github.com/JonZagorski/final-project/blob/main/screenshots/Graph2.png)
## Data Cleanup
The goal of the back-end is to find the data necessary to tell a story. 

![](https://github.com/JonZagorski/final-project/blob/main/screenshots/main.PNG)

We sourced our data from Yahoo Finance through a series of API calls. Originally, we were going to use a CSV from Quandl but abandoned this idea for Yahoo Finance as this allowed our team to pull in data that was as current as possible without incurring fees. Cleaning the data itself went about with minor hiccups.  

The challenges of converting everyting needed to Json files and figuring out the proper syntax took time to figure.  Once data was cleaned, it was loaded to a PostGres database. The Postgres database was hosted on AWS which was called by Flask and deployed to Heroku!

![](https://github.com/JonZagorski/final-project/blob/main/screenshots/yf_data_grab.PNG)

Hiccups encountered with issues with the data/time not pulling in correctly. Flask setup was also a learning experience.  A lesson learned was that not using primary keys meant we could not use Automap.base. Instead a Postgres database adapter - psycopg2 was used. 

## Machine Learning 
Trained and tested KNN (k-nearest neighbors), SVR (support vector regression), Linear Regression, and Decision Tree Regressor.  The Decision Tree Regressor model yielded the highest percentage of accuracy (about 97%) and is the model used for the results shown here. Features used for the modeling were:

![](https://github.com/JonZagorski/final-project/blob/main/screenshots/add_features.PNG)

![](https://github.com/JonZagorski/final-project/blob/main/screenshots/split_dataset.PNG)

![](https://github.com/JonZagorski/final-project/blob/main/screenshots/model_picking.PNG)

![](https://github.com/JonZagorski/final-project/blob/main/screenshots/model_accuracy.PNG)

![](https://github.com/JonZagorski/final-project/blob/main/screenshots/decision_tree_regressor.PNG)


## Technique/Technology 
* Clean Up:  Python/Pandas was used to initial cleaning and visualizing the data. Data was then converted to JSON.
* Machine Learning:  KNN (k-nearest neighbors), SVR (support vector regression), Linear Regression, and Decision Tree Regressor
* Graphic Analysis: D3
* Bootstrap for the HTML, CSS, and JavaScript Framework for web application.
* Database: PostGres hosted on AWS (called by Flask)
* Host Application:  Heroku
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
* Google Slides Presentation: https://docs.google.com/presentation/d/1pBWh26kjqHpMV2-2cadd5DjturxX8UY4JPbyi2F8PWY/edit?usp=sharing
>>>>>>> origin/main
=======
* Google Slides Presentation: https://docs.google.com/presentation/d/1pBWh26kjqHpMV2-2cadd5DjturxX8UY4JPbyi2F8PWY/edit?usp=sharing
>>>>>>> b1700c11035c0289beff651000a9e23d6ddaa8bc
=======
* Google Slides Presentation: https://docs.google.com/presentation/d/1pBWh26kjqHpMV2-2cadd5DjturxX8UY4JPbyi2F8PWY/edit?usp=sharing
>>>>>>> origin/main


#### [Images](Images)
Screenshots for presentation and ReadMe.

#### [Proposal](Proposal)
https://docs.google.com/document/d/1fRwJzVR5bxfnTkelrMhkKAD3qvZvKew23lo8Wl8mvM8/edit

#### [Static](Static)
CSS and JS and images

#### [Assets](assets)
CSS and JS for leaflet maps, demographic charts, and Covid charts.

#### [Templates](templates)
Index, About, Process 

#### [Test](test)
Jupyter Notebook files of cleaned data used for testing and training machine learning algorithms.

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> origin/main
=======

>>>>>>> b1700c11035c0289beff651000a9e23d6ddaa8bc
=======

>>>>>>> origin/main
![](https://github.com/JonZagorski/final-project/blob/main/screenshots/indexhtml.png)

Distribution of tasks
1.	Finding Data Source - team
2.	Cleaning up and transofroming the data - Brendan with assistance from Roshini
3.	Loading and testing the data - Brendan and Roshini 
4.	Proposal - Kim with support from the team
5.	Set up landing page – Kim
6.	Set up index.html, about.html, process.html and style.css - Kim with assistance from team
7.  Set up visualizations – Roshini
8.	PowerPoint - Kim with assistance from team
9. ReadMe - Kim with images from Brendan and Roshini
10. Postgres - Brendan
11. Flask - Jon
12.	Javascript - Roshini and Jon
13. Heroku - Jon

Regularly touched base via Slack to ensure project is on track.

## Contributors
* [Brendan Rhoads](https://github.com/BRhoads1155)
* [Jon Zagorski](https://github.com/JonZagorski)
* [Roshini Jayantha](https://github.com/RoshiniGau)
* [Kimberly Gore](https://github.com/KGore12)

GITHUB FOR FINAL PROJECT: https://github.com/JonZagorski/final-project
