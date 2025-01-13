import streamlit as st
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from time import sleep

# Load environment variables
load_dotenv()

# Streamlit app
def main():
    st.title("LinkedIn Profile Data Extractor")
    
    # Input for LinkedIn profile URL
    profile_url = st.text_input("Enter LinkedIn Profile URL:", placeholder="https://www.linkedin.com/in/example/")
    
    # Submit button
    if st.button("Get Profile Data"):
        if profile_url:
            with st.spinner("Fetching profile data..."):
                try:
                    # Setup headless Chrome
                    chrome_options = Options()
                    chrome_options.add_argument("--headless")  # Run in headless mode
                    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
                    chrome_options.add_argument("--no-sandbox")  # Bypass OS-level sandbox
                    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
                    driver = webdriver.Chrome(options=chrome_options)
                    
                    # Navigate to LinkedIn login
                    driver.get("https://www.linkedin.com/login")
                    
                    # Login to LinkedIn
                    email_field = driver.find_element(By.ID, "username")
                    email_field.send_keys(os.getenv("EMAIL"))
                    
                    password_field = driver.find_element(By.ID, "password")
                    password_field.send_keys(os.getenv("PASSWORD"))
                    
                    password_field.submit()
                    sleep(5)  # Wait for login to complete
                    
                    # Navigate to the LinkedIn profile
                    driver.get(profile_url)
                    sleep(5)  # Allow page to load
                    
                    # Extract profile data
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "lxml")
                    
                    name = soup.find("h1").get_text(strip=True) if soup.find("h1") else "N/A"
                    headline_elem = soup.find("div", {"class": "text-body-medium break-words"})
                    headline = headline_elem.get_text(strip=True) if headline_elem else "N/A"
                    
                    profile_data = {
                        "Name": name,
                        "Headline": headline,
                        "Profile URL": profile_url
                    }
                    
                    # Display the extracted data
                    st.success("Profile data fetched successfully!")
                    st.json(profile_data)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    driver.quit()
        else:
            st.warning("Please enter a valid LinkedIn profile URL.")

if __name__ == "__main__":
    main()