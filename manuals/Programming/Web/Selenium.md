# Introduction
[Selenium](https://www.selenium.dev/) is a browser automation tool that allows you to automate browser actions such as clicking, typing, and scrolling.

Basic usage:
```Python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")
```

# Selecting elements
We can select any element on the page using the `find_element(<method>, <selector>)` method. The method can be:

- `By.ID`: DOM ID
- `By.NAME`: DOM name
- `By.XPATH`: XPath query


# Waiting
Frequently, we need to wait for an element to be present on the page or active. We can do this using the `WebDriverWait` class.

```Python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "id")))
```

The expected condition can be:

- `presence_of_element_located`: the element is present on the page
- `element_to_be_clickable`: the element is clickable


# Interacting with elements
There are several methods to interact with, each described in its own section.

## Clicking
We can click on buttons, links, but also inputs to activate them. To do this:

```Python
element = driver.find_element(By.ID, "id")
element.click()
```

Sometimes, we may encounter the `ElementClickInterceptedException` error with a message like `Element <element> is not clickable at point (x, y). Other element would receive the click: <element>`. This happens when the element is not visible or not clickable. The solution depends on the case. If the element is overlapped by another element, the solution is to click on the parent element instead.



## Typing
We can type text into inputs using the `send_keys` method:

```Python
element = driver.find_element(By.ID, "id")
element.send_keys("text")
```

However, this may fail to pass some special characters (e.g. `@`, `^`, etc.). To overcome this, we can use the clipboard to copy and paste the text:

```Python
import pyperclip
from selenium.webdriver.common.keys import Keys

...

pyperclip.copy("text ^^^")
element.send_keys(Keys.CONTROL + "v")
```


# Downloading files
First it is useful to configure the browser to download files to a specific directory and not ask for confirmation:

```Python
options = uc.ChromeOptions()
...
download_prefs = {
    "download.default_directory": str(download_dir),           # save here
    "download.prompt_for_download": False,                # no Save As dialog
    "download.directory_upgrade": True,                   # use existing folder
    "safebrowsing.enabled": True                          # bypass safe browsing check
}
options.add_experimental_option("prefs", download_prefs)

driver = uc.Chrome(
    options=options,
    ...
)
```

Next, we can just click any download link and the download will start. Next problem can be finding out whether the download is complete. One strategy is to wait till no changes are detected in the download directory:
```Python
stable_since = time.time()
    files_before = list(download_dir.glob("*.*"))
    while time.time() - stable_since < 1:  # needs 1s of unchanging size
        files_after = list(download_dir.glob("*.*"))

        changed = True
        if len(files_after) == len(files_before):
            for file_before, file_after in zip(files_before, files_after):
                if file_before.name != file_after.name:
                    break
                if file_before.stat().st_size != file_after.stat().st_size:
                    break
            changed = False

        if changed:
            files_before = files_after
            stable_since = time.time()
        time.sleep(0.2)
```



# Login
Login is one of the most complicated things to automate, due to several layers of security and the fact that the login page usually serves as the guard point against automation.


## Using Undetected Chrome Driver to prevent automation detection
Sometimes, login through chrome testing driver is detected as automation and the login fails. In this case, we can try to use the [Undetected Chrome Driver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) to prevent detection. To use it, we need to:

- import the driver:
    ```Python
    import undetected_chromedriver as uc
    ```
- pass the path to the chrome browser to driver options:
    ```Python
    options = uc.ChromeOptions() # note the different options class!
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ```
- use the new driver and pass the options to it:
    ```Python
    driver = uc.Chrome(options=options)
    ```
- on Windows, we also need to use the `use_subprocess` argument to avoid an error:
    ```Python
    driver = uc.Chrome(options=options, use_subprocess=True)
    ```

## Storing cookies to avoid re-login
We can store the cookies so that we do not have to re-login every time. Example:

```Python
...
cookies_file = Path("cookies.pkl")
if cookies_file.is_file():
    cookies = pickle.load(cookies_file.open("rb"))
    
    #  go to the right domain first
    driver.get("https://www.example.com")

    # add the cookies
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    # go to the desired page
    driver.get("https://www.example.com/desired_page")
else:
    # normal login here
    ...
    # after login, store the cookies
    pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))
```





