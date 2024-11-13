import configparser
import sys 
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib')) # Libraries Found in ../lib
sys.path.append('/opt/splunk/etc/apps/MicrosoftDefenderTI/bin/lib/python3.9/site-packages')
sys.path.insert(0, '/opt/splunk/etc/apps/MicrosoftDefenderTI/bin/lib/python3.9/site-packages/')
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph import GraphRequestAdapter
from msgraph_core import GraphClientFactory
from kiota_authentication_azure.azure_identity_authentication_provider import AzureIdentityAuthenticationProvider
from httpx import AsyncClient

# Loads configuration from the config.ini file using configparser
def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

# Function to set up the Graph client using configuration data from config.ini
def setup_graph_client(config_path="config.ini"):
    config = load_config(config_path)

    # Extracts Azure App details from config.ini
    CLIENT_ID = config['azure']['client_id']
    TENANT_ID = config['azure']['tenant_id']
    CLIENT_SECRET = config['azure']['client_secret']
    SCOPES = [config['azure']['scopes']]

    # Extracts Proxy settings from config.ini
    proxies = {
        'http': config['proxy']['http'],
        'https': config['proxy']['https']
    }

    credentials = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        proxies=proxies
    )

    auth_provider = AzureIdentityAuthenticationProvider(credentials, scopes=SCOPES)

    httpx_proxies = {
        'http://': proxies['http'],
        'https://': proxies['https']
    }

    # Custom HTTP Client with the proxies and disabling SSL verification (IMPORTANT!)
    http_client = AsyncClient(proxies=httpx_proxies, verify=False)

    # Applies the default Graph Middleware to the HTTP client
    http_client = GraphClientFactory.create_with_default_middleware(client=http_client)

    # Creates a request adapter with the HTTP client
    adapter = GraphRequestAdapter(auth_provider, http_client)

    # Returns the Graph client for further use
    graph_client = GraphServiceClient(request_adapter=adapter)

    return graph_client
