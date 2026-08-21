# Selenium

## Introduction
[Selenium](https://www.selenium.dev/) is a browser automation tool that allows you to automate browser actions such as clicking, typing, and scrolling.

Basic usage:
```Python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")
```

## Selecting elements
We can select any element on the page using the `find_element(<method>, <selector>)` method. The method can be:

- `By.ID`: DOM ID
- `By.NAME`: DOM name
- `By.XPATH`: XPath query


## Waiting
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


## Interacting with elements
There are several methods to interact with, each described in its own section.

### Clicking
We can click on buttons, links, but also inputs to activate them. To do this:

```Python
element = driver.find_element(By.ID, "id")
element.click()
```

Sometimes, we may encounter the `ElementClickInterceptedException` error with a message like `Element <element> is not clickable at point (x, y). Other element would receive the click: <element>`. This happens when the element is not visible or not clickable. The solution depends on the case. If the element is overlapped by another element, the solution is to click on the parent element instead.



### Typing
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


## Downloading files
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



## Login
Login is one of the most complicated things to automate, due to several layers of security and the fact that the login page usually serves as the guard point against automation.


### Using Undetected Chrome Driver to prevent automation detection
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

### Storing cookies to avoid re-login
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



# Playwright

- [Official website](https://playwright.dev/)
- [GitHub](https://github.com/microsoft/playwright)
- [Wikipedia](https://en.wikipedia.org/wiki/Playwright_(software))


Playwright is a browser automation suite that can be used for testing, scraping, or as a gateway for LLMs.

## Playwright MCP

- [Introduction](https://playwright.dev/mcp/introduction)
- [Official documentation](https://playwright.dev/docs/getting-started-mcp)

To start the Playwright MCP server, run:
```bash
npx @playwright/mcp@latest <args>
```

which is typically set up in `JSON` like
```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        <args>
      ]
    }
  }
}
```

Typical arguments are:

- `--browser <browser>`: specify the browser to use, e.g., `chromium`, `firefox`, `webkit`
- `--extension`: connect to a running browser instance with the [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm) installed
- `--headless`: run the browser in headless mode, i.e., without a user interface
- `--isolated`: start a new browser every time, instead of having one session per workspace and reusing it
- `--port <port>`: specify the port to use for the Playwright server


## Connecting to Browsers
[Official documentation](https://playwright.dev/mcp/configuration/browser-extension)

Normally, Playwright uses its own browser instance. However, sometimes, it may be usefull to let it access a running user browser, i.e., to access sites behind a login without giving the credentials to the LLM. Currently, this is only supported in Chrome and Edge.

There are two ways how to connect to a browser:

- via [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/): access to a specific tab
    - best for a specific task on a single page
- via [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/): access to browser as a whole, including all tabs and cookies.
    - best for browser-wide debugging


### Connecting via Playwright Extension
[Official documentation](https://github.com/microsoft/playwright/blob/main/packages/extension/README.md)

1. Install the [Playwright Extension](https://chromewebstore.google.com/detail/playwright-extension/mmlmfjhmonkocbjadbfplnigmagldckm), if not yet installed
1. in the extension settings in the browser, check the `Allow access to file URLs` checkbox (otherwise, file uploads are not possible)
1. Add `--extension` as an argument to the MCP server configuration:
    ```json
    "mcpServers": {
        "playwright": {
          "type": "stdio",
          "command": "npx",
          "args": [
            "@playwright/mcp@latest",
            "--extension"
          ]
        }
    }
1. If running another browser than Chrome, you also need to use the `--browser` argument to specify the browser to use.

When strting the Playwright server manually, e.g., for external use from a sandbox, the command line can be:
```bash
npx @playwright/mcp@latest --port 8931 --browser msedge --extension
```


### Connecting via Chrome DevTools Protocol
We can either use automatic discovery of the browser instance with enabled remote debugging, or we can manually set the remote debugging port.

For **automatic discovery**:

1. go to [chrome://inspect/#remote-debugging](chrome://inspect/#remote-debugging), and check the `Allow remote debugging for this browser instance` checkbox
1. add `--cdp-endpoint=chrome` as an argument to the MCP server configuration:
    ```json
    "mcpServers": {
        "playwright": {
          "type": "stdio",
          "command": "npx",
          "args": [
            "@playwright/mcp@latest",
            "--cdp-endpoint=chrome"
          ]
        }
    }
    ```

For **manual discovery**:

1. Run the browser with the debugging port specified, e.g.:
    ```bash
    chrome --remote-debugging-port=9222
    ```
1. Add `--cdp-endpoint=http://localhost:9222` as an argument to the MCP server configuration:
    ```json
    "mcpServers": {
        "playwright": {
          "type": "stdio",
          "command": "npx",
          "args": [
            "@playwright/mcp@latest",
            "--cdp-endpoint=http://localhost:9222"
          ]
        }
    }
    ```


