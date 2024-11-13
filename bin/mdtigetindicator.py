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
class MdtiCommand(sc.StreamingCommand):

    async def get_data(self, article_indicator_id):
        try:
            # Initialize the graph client
            graph_client = setup_graph_client()

            # Fetch article indicator data asynchronously
            result = await graph_client.security.threat_intelligence.article_indicators.by_article_indicator_id(article_indicator_id).get()
        
            # Return the result as a JSON string if available
            if result:
                return json.dumps(result, default=lambda o: o.__dict__, indent=4)
            else:
                return "No data found"
        except Exception as e:
            # Return detailed error message
            return f"Error fetching article indicator data: {str(e)}"

    def async_wrapper(self, coro):
        """Helper to run async code in a synchronous context"""
        return asyncio.run(coro)

    def stream(self, records):
        for record in records:
            try:
                # Fetch article indicator from the record
                indicator_id = record.get("indicator", None)
                if not indicator_id:
                    record['mdti_articleindicator'] = "Error: No host provided in the record"
                else:
                    # Fetch article indicator data using async wrapper
                    indicator_data = self.async_wrapper(self.get_data(indicator_id))
                    record['mdti_articleindicator'] = indicator_data

                yield record
            except Exception as e:
                # Log any unexpected error
                record['mdti_articleindicator'] = f"Unexpected error: {str(e)}"
                yield record

if __name__ == "__main__":
    dispatch(MdtiCommand, sys.argv, sys.stdin, sys.stdout, __name__)
