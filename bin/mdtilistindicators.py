import splunklib.searchcommands as sc
import os
import sys
import json
import asyncio
from graph_client_setup import setup_graph_client
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators

# SPLUNK SEARCH QUERY: | makeresults | eval article_id="EXAMPLE" | mdtilistindicators fieldname=article_id

# Configure system paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, '/opt/splunk/etc/apps/MicrosoftDefenderTI/bin/lib/python3.9/site-packages/')

@Configuration()
class MdtiIndicatorsCommand(sc.StreamingCommand):

    # Option to accept article_id from the search query
    fieldname = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the field containing the article ID''',
        require=True, validate=validators.Fieldname())

    async def get_indicators(self, article_id):
        try:
            # Initialize the graph client
            graph_client = setup_graph_client()

            # Fetch indicators related to the specified article ID
            response = await graph_client.security.threat_intelligence.articles.by_article_id(article_id).indicators.get()

            # Initialize a list to store indicators data
            indicators_list = []

            # Checks if the response contains a 'value' attribute (list of indicators)
            if hasattr(response, 'value'):
                for indicator in response.value:
                    # Extract fields with safe handling
                    indicator_data = {
                    "id": getattr(indicator, "id", "null"),
                    "indicatorType": getattr(indicator, "indicatorType", "null"),
                    "value": getattr(indicator, "value", "null"),
                    "createdDateTime": str(getattr(indicator, "createdDateTime", "null")),
                    "lastUpdatedDateTime": str(getattr(indicator, "lastUpdatedDateTime", "null")),
                    "description": getattr(indicator, "description", "null")
                    }

                # Append each indicator's data to the list
                indicators_list.append(indicator_data)

                # Convert the list to a JSON string
                return json.dumps(indicators_list, indent=4)
            else:
                return "No indicators found"
        except Exception as e:
            return f"Error fetching indicators data: {str(e)}"

    def async_wrapper(self, coro):
        """Helper to run async code in a synchronous context"""
        return asyncio.run(coro)

    def stream(self, records):
        for record in records:
            try:
                # Fetch the article_id from the record using the fieldname option
                article_id = record.get(self.fieldname, None)
                if not article_id:
                    record['mdti_indicators'] = "Error: No article_id provided in the record"
                else:
                    # Fetch indicators data using async wrapper
                    indicators_data = self.async_wrapper(self.get_indicators(article_id))
                    record['mdti_indicators'] = indicators_data

                yield record
            except Exception as e:
                record['mdti_indicators'] = f"Unexpected error: {str(e)}"
                yield record

if __name__ == "__main__":
    dispatch(MdtiIndicatorsCommand, sys.argv, sys.stdin, sys.stdout, __name__)
