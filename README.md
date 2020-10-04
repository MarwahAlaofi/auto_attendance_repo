# Description
This script can be used to automate marking student attendance at taibahu.
<br>A **demo** can be found [Here](https://vimeo.com/464170126)
<br>When using the script, the browser can be hidden and the **submit button** can be activated for a *lazier* experience! :)

# How to use?
Follow the steps below to get things up and running:
1. Download and install <strong>python</strong>: https://www.python.org/downloads/
2. Add Python directory to the *environment path*
3. Download and install **selenium** and **pandas** using the following commands: <br>
<code>python -m pip install selenium </code><br>
<code>python -m pip install pandas</code>
4. Download **chrome driver**: https://chromedriver.chromium.org/downloads
5. Add chrome driver directory to the *environment path*.
6. **Modify** the script by setting the *parameter section*.
7. **Run** the script using the following command:<br>
<code>python scriptname.py [lecture_date] #expected date format: DD-MM-YY {default: today's date} </code>
8. Enjoy :tada:
# Troubleshooting
The script is built and primarily tested on **Mac OS**. Some successful testing has been done on **Windows 10** as well.
<br>The code is built based on some assumptions (e.g., there is no more than one session/day) which may not be true in all cases and many issues are likely to arise while using the script. Below I will add some common issues and how to address them:     
1. The script assumes that your e-service main page looks like the screenshot below (there is no suggestion box):
<a href="https://ibb.co/jWmHXnQ"><img src="https://i.ibb.co/jWmHXnQ/main-page-suggestion-box.png" alt="main-page-suggestion-box" border="0"></a> <br>
If you do have a suggestion box, then you may either 1) write some suggestions so it disappears or 2) change the paragraph index in following line:
    <code>section_table_rows = driver.find_elements_by_xpath('//*[@id="Table_01"]/tbody/tr[2]/td/table/tbody/tr/td[1]/p[1]/table[2]/tbody/tr')</code><br>

to:
    <code>section_table_rows = driver.find_elements_by_xpath('//*[@id="Table_01"]/tbody/tr[2]/td/table/tbody/tr/td[1]/p[3]/table[2]/tbody/tr')</code> <br>

2. [*Element not found* | *element is unclickable exception*] ➔ this is likely to happen when the element within DOM (Document Object Model of the page) is not yet downloaded. To resolve this issue, you may add some sleeping time just before the problematic element as follows: <code> time.sleep(5) # you may increase the time as needed </code><br>
:

# Contribute
You are **welcome** to contribute to the script. There are many possible improvements, e.g., **email notifications** to those with high denial risk, **auto-run** at specific time intervals, create a **more user-friendly interface**..etc  
