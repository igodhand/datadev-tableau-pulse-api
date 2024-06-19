## Step 0: Authenticate

Sample code to authenticate with Tableau using a Personal Access Token, obtain a JSON response, and create the `X-Tableau-Auth` header.

## Step 1: List Metric Definitions

Working code to list Tableau Pulse Metric Definitions, providing an idea of what you need to prepare to create Tableau Pulse Metric Definitions.

### Reference
* https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_pulse.htm#MetricQueryService_ListDefinitions

## Step 2: Get Data Source ID

Sample code to retrieve the `datasource_id` from a published data source using the **Project Name** and **Published Data Source Name**.

### Reference
* https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm

## Step 3: Get Column Names

When creating Tableau Pulse Metric Definitions, you need to know the column names.

* You can use the Tableau Pulse Datasource Endpoint to get the column names.
* Generally, you should already know which columns you have and set them as metric filters or calculations.

### Reference
* Learning by Doing !

