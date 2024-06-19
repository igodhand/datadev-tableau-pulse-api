# DataDev Tableau Pulse API
https://github.com/igodhand/datadev-tableau-pulse-api

## Overview
This repository contains samples and applications for the Tableau Pulse API, prepared for DataDev Day in June 2024. It introduces the use of Tableau Pulse APIs to automate metric definitions and metric deployment, designed to work with Tableau Pulse versions 2024.1 - 2024.2. Please note that it may not include Tableau Pulse Premium features due to unreleased APIs.

## Prerequisites
It is assumed that you have the following knowledge:
* How to authenticate Tableau Cloud using a Personal Access Token with the REST API.
* How to query Tableau REST API endpoints, especially for datasources.
* Basic understanding of Tableau Pulse.
* How to publish datasources to Tableau Cloud.

## Setup
You need to set up the Tableau Cloud Personal Access Token and your Tableau Cloud pod in the `_include` folder.

* **config.py** - This file requires three environment variables: `PAT_TOKEN_NAME`, `PAT_TOKEN_SECRET`, and `PAT_CONTENT_URL`
    * `token_name`: `os.environ.get('PAT_TOKEN_NAME')`
    * `token_secret`: `os.environ.get('PAT_TOKEN_SECRET')`
    * `content_url`: `os.environ.get('PAT_CONTENT_URL')`

## Helper Class
In general, we also need a helper class for authentication, querying frequently used endpoints, and utility functions to translate JSON responses into structured data.

* **helper.py** - This file might not cover every use case for the Tableau Pulse API, but it serves as a great foundation for interacting with the Tableau Pulse API.
    * We will need a configuration dictionary (`config_dict`) with the following five keys: `{"server", "token_name", "token_secret", "content_url", "api_version"}`.


## References

### Tableau REST API
* **Authentication**
    * [Tableau REST API Authentication](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_auth.htm)
* **Datasource**
    * [Tableau REST API Datasources](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm)
* **Tableau Pulse API**
    * [Tableau Pulse API Reference](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_pulse.htm)
* **Tableau Pulse API Detailed Reference (Very Useful for getting expected results)**
    * [Tableau Pulse API Detailed Reference](https://help.tableau.com/current/api/rest_api/en-us/REST/TAG/index.html#tag/Pulse-Methods)
* **Salesforce Developer Postman Collection (Very Useful for Payload POSTing)**
    * [Salesforce Developer Postman Collection](https://www.postman.com/salesforce-developers/workspace/salesforce-developers/folder/12721794-d04fce0e-38f8-4bf0-8bca-978f0364c919)

I highly recommend watching Timothy Vermeiren's session about Hacking Tableau 101 to learn more about Tableau HTTP requests.

## Special Thanks

* Will Ayd's pantab library
    * Install pantab with: `pip install pantab`
    * [Pantab Documentation](https://pantab.readthedocs.io/en/latest/)
