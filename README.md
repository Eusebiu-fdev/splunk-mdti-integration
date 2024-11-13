# Splunk Integration with Microsoft Defender Threat Intelligence (MDTI)

This repository contains a set of custom Splunk commands for seamless integration with Microsoft Defender Threat Intelligence (MDTI). The application enables users to make GET requests to the MDTI API directly from Splunk, retrieving real-time threat intelligence data such as articles, WHOIS information, and indicators. The fetched data is processed and displayed within Splunk, allowing for streamlined threat analysis and reporting.

## 🌟 Features

- **Custom Splunk Commands**: Provides multiple custom commands (`mdti_articles`, `mdti_whois`, `mdti_indicators`, etc) for querying MDTI API endpoints directly from Splunk.
- **Real-Time Threat Intelligence**: Retrieves the latest threat intelligence data from Microsoft Defender, including threat articles, indicators, and WHOIS information.
- **Asynchronous API Calls**: Leverages asynchronous Python functions (`asyncio`) for efficient data retrieval, ensuring minimal latency and faster response times.
- **JSON Data Parsing**: Extracts and formats relevant data fields from the API response, handling potential errors and null values gracefully.
- **Configurable and Extensible**: Easily configure API access and extend functionality with additional endpoints or custom data fields.

## 📋 Prerequisites

Before you get started, ensure you have the following:

- **Splunk Enterprise** or **Splunk Cloud** with administrative access.
- **Microsoft Defender Threat Intelligence (MDTI)** API access. You need a registered application in Azure AD with the necessary permissions.
- **Python 3.9 or higher** installed on the Splunk server.
- **Python Packages**:
  - `splunklib` for Splunk SDK integration.
  - `msgraph-core` and `azure-identity` for Microsoft Graph API requests.

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/splunk-mdti-integration.git
cd splunk-mdti-integration
```

### 2. Install Required Python Libraries

Ensure you have the necessary Python libraries installed on your Splunk server:

```bash
pip install splunklib msgraph-core azure-identity asyncio httpx
```

### 3. Configure API Access

Update the `graph_client_setup.py` file with your Azure AD credentials:

```python
client_id = "<YOUR_CLIENT_ID>"
client_secret = "<YOUR_CLIENT_SECRET>"
tenant_id = "<YOUR_TENANT_ID>"
scope = ["https://graph.microsoft.com/.default"]
```

### 4. Install the Custom Commands in Splunk

- Copy the custom Python scripts to your Splunk app directory, typically located at:
  `/opt/splunk/etc/apps/your-app-name/bin/`
- Restart the Splunk service for the changes to take effect:

```bash
sudo /opt/splunk/bin/splunk restart
```

## 🚀 Usage

### 1. Fetch Threat Articles

Use the `mdtilistarticles` command to fetch the latest threat articles from MDTI:

```spl
| makeresults | mdtilistarticles
```

### 2. Get WHOIS Information

Use the `mdtiwhois` command to retrieve WHOIS data for a specified domain:

```spl
| makeresults | eval host="example.com" | mdtiwhois
```

### 3. List Indicators for an Article

Use the `mdtigetindicator` command to get indicators associated with a specific article ID:

```spl
| makeresults | eval article_id="your-article-id" | mdtigetindicator
```

### Example Output

The commands return JSON data parsed into Splunk events, displaying fields like `id`, `title`, `description`, `createdDateTime`, `indicatorType`, and more.

ALL commands found in /MicrosoftDefenderTI/bin/README.txt

## ⚙️ Configuration Options

You can customize the behavior of the API calls by editing the Python scripts or adjusting query parameters directly within Splunk.

### Proxy Configuration

If your organization uses a proxy, configure it in the Python scripts:

```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080',
}
```

## 🛠️ Troubleshooting

- **Invalid Characters in Headers**: If you encounter `Invalid characters (CR/LF) in header WWW-Authenticate`, ensure that your API requests do not include newline characters in headers.
- **Attribute Errors**: If you receive errors like `'Object' has no attribute`, verify the field names against the latest Microsoft Graph API documentation.
- **HTTP 400/401 Errors**: Check your Azure AD application permissions and API token configuration.

## 📚 Documentation

- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/api/overview)
- [Splunk Custom Search Commands](https://dev.splunk.com/enterprise/docs/devtools/customsearchcommands/)

## 🤝 Contributions

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

With this integration, you can now leverage Microsoft Defender Threat Intelligence data directly in Splunk, enhancing your threat detection and response capabilities. 🎉

Feel free to update or expand this README.md to fit your specific implementation and requirements.
