import splunklib.searchcommands as sc
import os
import sys
import json
import asyncio
from graph_client_setup import setup_graph_client
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration

# Configure system paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, '/opt/splunk/etc/apps/MicrosoftDefenderTI/bin/lib/python3.9/site-packages/')

@Configuration()
class MdtiArticlesCommand(sc.StreamingCommand):

    async def get_articles(self):
        try:
            # Initialize the graph client
            graph_client = setup_graph_client()

            # Fetch the articles data directly using the 'get()' method
            response = await graph_client.security.threat_intelligence.articles.get()

            # Initialize a list to store articles data
            articles_list = []

            # Checks if the response contains a 'value' attribute (list of articles)
            if hasattr(response, 'value'):
                for article in response.value:
                    # Extract fields with safe handling, handling FormattedContent objects
                    summary = getattr(article, "summary", None)
                    summary_content = summary.content if summary and hasattr(summary, "content") else "null"

                    body = getattr(article, "body", None)
                    body_content = body.content if body and hasattr(body, "content") else "null"

                    article_data = {
                        "id": getattr(article, "id", "null"),
                        "title": getattr(article, "title", "null"),
                        "summary": summary_content,
                        "body": body_content,
                        "createdDateTime": str(getattr(article, "created_date_time", "null")),
                        "lastUpdatedDateTime": str(getattr(article, "last_updated_date_time", "null")),
                        "isFeatured": getattr(article, "is_featured", "null"),
                        "imageUrl": getattr(article, "image_url", "null"),
                        "tags": getattr(article, "tags", [])
                    }

                    # Append each article's data to the list
                    articles_list.append(article_data)

                # Convert the list to a JSON string
                return json.dumps(articles_list, indent=4)
            else:
                return "No articles found"
        except Exception as e:
            return f"Error fetching articles data: {str(e)}"

    def async_wrapper(self, coro):
        """Helper to run async code in a synchronous context"""
        return asyncio.run(coro)

    def stream(self, records):
        for record in records:
            try:
                # Fetch articles data using async wrapper
                articles_data = self.async_wrapper(self.get_articles())
                record['mdti_articles'] = articles_data

                yield record
            except Exception as e:
                record['mdti_articles'] = f"Unexpected error: {str(e)}"
                yield record

if __name__ == "__main__":
    dispatch(MdtiArticlesCommand, sys.argv, sys.stdin, sys.stdout, __name__)
