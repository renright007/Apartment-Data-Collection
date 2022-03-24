
# This script usese BeautifulSoup to scrape the goals information of PL players for the tables that can be found on the offical Premier League Website. It demonstrates proficiencies in both Beautiful Soup and Pandas. 

# Import Libraries

from pathlib import Path
import selenium
import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


listings_data = {
    'Listing Name':[],
    'Street Address':[],
    'City':[],
    'Postal Code':[],
    'Unit Type':[],
    'Specs':[],
    'Bathrooms':[],
    'Price':[],
    'Size':[]
    }

# Open ChromeDrive

host = '192.168.12.12'  # Define the Host and Port
port = 12345

url = 'https://www.zumper.com/apartments-for-rent/vancouver-bc'
driver = webdriver.Chrome(ChromeDriverManager().install())  # Define the Driver
driver.get(url) # Get the PL Websitre

driver.maximize_window()    # Maximize Window so the full screen information appears

listings_table = "//*[@id='rail']/div/div/div[1]/div[3]/div[1]"
r = driver.find_elements_by_xpath(listings_table + "/div")    # Get the row lenght
rc = len (r)

print(rc)

# Click first photo to enter full screen mode
name = driver.find_element_by_xpath("//*[@id='rail']/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div[2]/div[1]/div[3]/a")   # Define the name of the first listing
name.click()    # Click to navigate to the listing view

time.sleep(2)  # Time to rest prior to removing cookie pop up

next_btn = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/button[3]")  # Define the xpath to the next listing button

for i in range (1, 5):

    time.sleep(2)  # Time to rest prior to removing cookie pop up

    # Listing Name details
    listing_name = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div/div[2]").text
    
    # Scrape full address and append details accordingly
    address = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/div/h1/span").text
    address_list = address.split(", ")  # Split by comma to get details

    # Define the address details
    street_address = address_list[0]
    city = address_list[1]  
    postal_code = address_list[2].split(" ")[1] + " " + address_list[2].split(" ")[2]  # Postal code requires additional split to identify PC prefix

    element = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div[2]/h2')  # Here we define the view location for the about section, which allows the floorplans to appear
    listing_name_loc = driver.find_element_by_xpath("//*[@id='root']/div/div/div[2]/div/div/div/div/div[1]/div/div[2]")     # Define the location of the top of the page so we return to click the next button
    # Using the ActionChain plug in, we can move to different locations on the listing
    actions = ActionChains(driver)  
    actions.move_to_element(element).perform()  # This brings the floorplan section into view

    time.sleep(2)  # Time to rest prior to removing cookie pop up

    floorplans = driver.find_elements_by_class_name("css-o6i9hf")   # Using the class name, we can get a list of the floorplans
    fpc = len(floorplans)   # Count the amount that exist within the listing

    fp_table = "//*[@id='root']/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div[1]/div/" # Define the xpath to the floorplan section

    for j in range(1, fpc + 1):

        fp_click = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[1]/div[2]/div[1]/div[1]")
        fp_click.click()    # Click floorplan to expand details

        unit_type = fp_click.text[:-1]   # Grab floorplan type

        unit_plans = int(driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[1]/div[2]/div[2]").text.split(' ')[0]) # Isolate the integer value for the number of floor plans

        if unit_plans > 1:  # If there are more than one, we must use a loop to scrape all unit plans

            for k in range(1, unit_plans+1):    # For loop to grab all unit info within the floorplan
                
                # Define values for the floorplan information, using j within the floorplan section and k within the unit plans
                fp_name = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div[" + str(k) + "]/div/div[1]/div[2]/div[1]/div[1]").text     
                fp_bath = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div[" + str(k) + "]/div/div[1]/div[2]/div[2]").text
                fp_sqft = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div[" + str(k) + "]/div/div[1]/div[2]/div[3]/span").text
                fp_price = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div[" + str(k) + "]/div/div[1]/div[2]/div[1]/div[2]").text

                # Append Floorplan Information
                listings_data['Specs'].append(fp_name) 
                listings_data['Bathrooms'].append(fp_bath)
                listings_data['Size'].append(fp_sqft)
                listings_data['Price'].append(fp_price)

                # Append Listing Information
                listings_data['Listing Name'].append(listing_name)
                listings_data['Street Address'].append(street_address)
                listings_data['City'].append(city)
                listings_data['Postal Code'].append(postal_code)
                listings_data['Unit Type'].append(unit_type)

        else:   # If just one plane

            # Define values for the floorplan information, using j within the floorplan section
            fp_name = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]").text
            fp_bath = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div/div/div[1]/div[2]/div[2]/span").text
            fp_sqft = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div/div/div[1]/div[2]/div[3]/span").text
            fp_price = driver.find_element_by_xpath(fp_table + "div[" + str(j) + "]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]").text

            # Append Floorplan Information
            listings_data['Specs'].append(fp_name) 
            listings_data['Bathrooms'].append(fp_bath)
            listings_data['Size'].append(fp_sqft)
            listings_data['Price'].append(fp_price)

            # Append Listing Information
            listings_data['Listing Name'].append(listing_name)
            listings_data['Street Address'].append(street_address)
            listings_data['City'].append(city)
            listings_data['Postal Code'].append(postal_code)
            listings_data['Unit Type'].append(unit_type)

    time.sleep(2)  # Time to rest to pull information
    actions.move_to_element(listing_name_loc).perform() # Move back to top of the page

    next_btn.click()    # Navigate to next listing

listing_df = pd.DataFrame.from_dict(listings_data)    # Convert to data frame
print(listing_df.to_string())

