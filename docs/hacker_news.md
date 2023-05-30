# ScrapeHackerNews

This script contains a class `ScrapeHackerNews` that inherits from `BaseOperator`. The purpose of this class is to scrape and filter a given number of pages from [Hacker News](https://news.ycombinator.com/) based on provided keywords, if any, and excluding specific words in the titles.

## Class Methods

### run_step

This method handles the execution of the step by calling the helper function `scrape_hacker_news` with the necessary parameters and the AI context.

**Parameters:**

- `step`: The step that contains the parameters required to execute the scraping.
- `ai_context`: The AI context which provides methods to handle outputs and logs.

### scrape_hacker_news

This helper function does the main work of scraping the Hacker News website and filtering the results based on the user's input. It is called by the `run_step` method and uses the `requests`, `BeautifulSoup`, and `json` libraries to help with the web scraping and data processing.

**Parameters:**

- `params`: A dictionary containing the parameters needed for the scraping and filtering process. It can have the `keywords` key (a list of keywords to filter the news by) and the `num_pages` key (the number of pages to scrape).
- `ai_context`: The AI context which provides methods to handle outputs and logs.

**Functionality:**

1. Retrieves the `keywords` and `num_pages` from the `params`. If not provided, it sets `keywords` to an empty list and `num_pages` to 1.
2. Ensures that the provided number of pages is not more than 5 to prevent excessive scraping.
3. Initializes the `title_link_dict`, an empty dictionary that will store the articles' titles and links after the filtering process.
4. Iterates through the specified range of pages and sends an HTTP request to the Hacker News website.
5. Uses BeautifulSoup to parse the HTML content and select each post on the page.
6. For each post, checks if it meets the filtering criteria:
    - If keywords are provided, the title must contain at least one of the keywords.
    - The title must not contain any of the excluded words (`AskHN`, `ShowHN`, `LaunchHN`).
7. If the post meets the filtering criteria, adds the title and link to the `title_link_dict`.
8. After iterating through all the posts and pages, sets the `title_link_dict` output and adds a log message.

## Summary

In summary, the `ScrapeHackerNews` class scrapes the specified number of pages from the Hacker News website, filters the articles by keywords (if provided) and excluded words, and stores the filtered articles' titles and links in a dictionary. This dictionary is then set as the output of the script using the AI context.