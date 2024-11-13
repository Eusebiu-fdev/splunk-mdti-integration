import splunklib.searchcommands as sc
import os
import sys
import json
import asyncio
from graph_client_setup import setup_graph_client
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators

# SPLUNK SEARCH QUERY: | makeresults | eval hostname="www.example.com" | mdtireputation  fieldname=hostname

# Configure system paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
sys.path.insert(0, '/opt/splunk/etc/apps/MicrosoftDefenderTI/bin/lib/python3.9/site-packages/')

@Configuration()
class MdtiCommand(sc.StreamingCommand):
    
    # Define the `fieldname` option to specify which field contains the host identifier
    fieldname = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the field that contains the host identifier''',
        require=True, validate=validators.Fieldname()
    )

    async def get_data(self, host_id):
        try:
            # Initialize the graph client
            graph_client = setup_graph_client()

            # Fetch reputation data asynchronously
            result = await graph_client.security.threat_intelligence.hosts.by_host_id(host_id).reputation.get()

            # Return the result as a JSON string if available
            if result:
                return json.dumps(result, default=lambda o: o.__dict__, indent=4)
            else:
                return "No data found"
        except Exception as e:
            # Return detailed error message
            return f"Error fetching reputation data: {str(e)}"

    def async_wrapper(self, coro):
        """Helper to run async code in a synchronous context"""
        return asyncio.run(coro)

    def stream(self, records):
        for record in records:
            try:
                # Fetch the host_id using the specified fieldname
                host_id = record.get(self.fieldname, None)
                if not host_id:
                    record['mdti_reputation'] = f"Error: No host provided in the field '{self.fieldname}'"
                else:
                    # Fetch reputation data using async wrapper
                    rep_data = self.async_wrapper(self.get_data(host_id))
                    record['mdti_reputation'] = rep_data

                yield record
            except Exception as e:
                # Log any unexpected error
                record['mdti_reputation'] = f"Unexpected error: {str(e)}"
                yield record

if __name__ == "__main__":
    dispatch(MdtiCommand, sys.argv, sys.stdin, sys.stdout, __name__)
