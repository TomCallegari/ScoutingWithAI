![alt text](title_page.PNG "Exoplanets")


# Scouting With AI

The purpose of this project was to use the skills taught through the 6-month [University of Toronto School of Continuing Studies Data Analytics Bootcamp](https://bootcamp.learn.utoronto.ca/data/).

Historically, professional sports teams have relied on the intuition and experience of scouts who travel relentlessly, watching thousands of games in person, to 
gain a level of knowledge that allows them to project the future potential of amateur players prior to eligibility for a draft.  This process is designed to give organizations
insight into the available players so that they can select the ones they feel would be best for their organization in the future.  Generally, scouts will write reports on each player
and give their opinions in the form of a quantified grade along with the text write-up.

What if applying machine learning to the problem would give additional insight that had not been uncovered before?

In addition to traditional scouting, data collection of players past performances and meta variables on who they are could be used in conjunction with traditional methods to add another layer
of knowledge and insight. This project is a first attempt to combine both past performance data, scouting write ups and modern neural network machine learning to approximate the theoretical function that exists between
player past performance and future potential.

This Github Repository contains the scripts, files, data, models and presentation for the project.

* [URL Scraper](https://github.com/TomCallegari/ScoutingWithAI/blob/master/Scrapers/eliteprospects_url_scrape.py)
* [Player Profile Scraper](https://github.com/TomCallegari/ScoutingWithAI/blob/master/Scrapers/EliteProspects.py)
* [Extract/Transform/Load(ETL)](https://github.com/TomCallegari/ScoutingWithAI/blob/master/Notebooks/ETL.ipynb)
* [Feature Engineering](https://github.com/TomCallegari/ScoutingWithAI/blob/master/Notebooks/Feature_Engineering.ipynb)
* [Deep NN Model](https://github.com/TomCallegari/ScoutingWithAI/blob/master/Notebooks/Deep_NN.ipynb)
* [Project PowerPoint](https://github.com/TomCallegari/ScoutingWithAI/blob/master/Presentation/final_project_presentation.pdf)


### Technologies Used

* Python
	* Pandas (Data Manipulation)
	* Numpy
	* NLTK (Natural Language Processing)
	* Sklearn (Machine Learning)
	* Tensorflow.Keras (Deep Learning Neural Network)
	* BeautifulSoup (HTML Web Scraping)
	* Matplotlib / Seaborn (Plotting)
* MongoDB
	* Python package PyMongo