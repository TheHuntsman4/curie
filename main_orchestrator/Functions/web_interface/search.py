import wolframalpha
import google.generativeai as palm
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Secrets.keys import google_api, wolfram_app_id
from dependencies import BaseTool


palm.configure(api_key=google_api)

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name


# App id obtained by the above steps
app_id = wolfram_app_id
client = wolframalpha.Client(app_id)

class websearch:
    def __init__(self, model):
        self.model = model
    def scrape_google_search(self, query, num_pages=5):
        print('initializing...')
        info = []
        references = []
        driver = webdriver.Chrome()
        print('searching...')
        try:
            for page_num in range(num_pages):
                url = f"https://www.google.com/search?q={query}&start={page_num * 10}"
                driver.get(url)

                # Extract search results from the current page
                search_results = driver.find_elements("css selector", 'div.tF2Cxc')

                # Extract data from each search result
                for result in search_results:
                    description = ''
                    title_element = result.find_element("css selector", 'h3')
                    title = title_element.text

                    url_element = result.find_element("css selector", 'a')
                    url = url_element.get_attribute('href')

                    description_element = result.find_element("css selector", 'div')
                    description = f"{description}\n{description_element.text}"

                    '''print(f"Title: {title}")
                    print(f"URL: {url}")
                    print(f"DESCRIPTION: {description}")'''

                    references.append(f"Title: {title}, URL: {url}, DESCRIPTION: {description}")

                info.append(references)

                # Scrape the next page if there are more results
                if page_num < num_pages:
                    # Wait for the "Next" button to be clickable
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, 'pnnext'))
                    )
                    next_button.click()

        except Exception as e:
            print(f"error: {e}")

        finally:
            # print(info)
            driver.quit()
            return references


    def llm_prompt(self, query, context=None):
        if context:
            prompt = f"""
                    Here is my query: {query},
                    answer while keeping in account the following information:{context.replace(':', '')}
                    """

        else:
            try:
                prompt = f"""
                    Here is my query: {query},
                    in case you are not familiar with it, here are some search results: {self.scrape_google_search(query)}
                    """
            except:
                print("failed to scrape results")
                prompt = f"query: {query}"

        completion = palm.generate_text(
            model=self.model,
            prompt=prompt,
            temperature=0,
            # The maximum length of the response
            max_output_tokens=800,
        )

        print(completion.result)
        return completion.result

    def search_wolfram(self, query):
        try:
            res = client.query(query)
            answer = next(res.results).text
            print(f"{answer}\n\n")
        except:
            answer = None
        return answer

    def search(self, query):
        print('start')
        context = self.search_wolfram(query)
        response = f"**query**:\n{query}\n\n**response**:\n{self.llm_prompt(query, context)}"
        return response

# -------------------------------------------------------------------------------------------------------------------

class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "Useful for answering questions about future events, current affairs, positions of power, weather, details and events, browse the internet"
    searching_agent = websearch(model=model)
    def _run(self, tool_input: str, **kwargs) -> str:
        """Run search tool."""
        print("running search...")
        return f"\nquery: {tool_input}\nanswer: {self.searching_agent.search(tool_input)}"

custom_search_tool = CustomSearchTool()