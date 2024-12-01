import os
import ast
import requests
import json
from dotenv import load_dotenv
import os
from langgraph_module.state import AgentGraphState


load_dotenv()





def format_results(organic_results):

        result_strings = []
        for result in organic_results:
            title = result.get('title', 'No Title')
            link = result.get('link', '#')
            snippet = result.get('snippet', 'No snippet available.')
            result_strings.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n---")
        
        return '\n'.join(result_strings)

def google_serper(state:AgentGraphState, plan):
    #load_config(config_path)

    plan_data = plan().content
    plan_data = json.loads(plan_data)
    search = plan_data.get("search_term")

    search_url = "https://google.serper.dev/search"
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': os.getenv("GOOGLE_SERPER_API_KEY"),
    }
    payload = json.dumps({"q": search})
    
    # Attempt to make the HTTP POST request
    try:
        response = requests.post(search_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4XX, 5XX)
        results = response.json()
        
        # Check if 'organic' results are in the response
        if 'organic' in results:
            formatted_results = format_results(results['organic'])
            state = {**state, "serper_response": formatted_results}
            return state
        else:
            return {**state, "serper_response": "No organic results found."}

    except requests.exceptions.HTTPError as http_err:
        return {**state, "serper_response": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {**state, "serper_response": f"Request error occurred: {req_err}"}
    except KeyError as key_err:
        return {**state, "serper_response": f"Key error occurred: {key_err}"}
