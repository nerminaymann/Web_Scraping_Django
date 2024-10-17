# Web_Scraping_Django

## Overview
A web Scraping project using Python (OOP) and Django, Used for scraping product information from Jumia, a popular e-commerce website, and renders it on our website 

### Key Elements:
* Backend: Django View: Handles the web scraping, extracts relevant data from the Jumia website, and passes this data to the frontend for display.
* Frontend: HTML Template: Displays the search form and the table of product results dynamically based on user input.

### Blueprint of project:
#### Web Scraping Module
* A class responsible for managing web requests, including handling headers, session for making requests with the headers and fetching html content.

#### Product Data Extraction Module
* A class responsible for parsing and extracting relevant data from the HTML.

#### Django View
* The Django view will instantiate and use these classes to manage the workflow.


