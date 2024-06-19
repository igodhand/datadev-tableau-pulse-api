## Step 0: Authenticate

Sample code to authenticate with Tableau using a Personal Access Token, obtain a JSON response, and create
the `X-Tableau-Auth` header.

## Step 1: List Metric Definitions

Working code to list Tableau Pulse Metric Definitions, providing an idea of what you need to prepare to create Tableau
Pulse Metric Definitions.

### Reference

* https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_pulse.htm#MetricQueryService_ListDefinitions

## Step 2: Get Data Source ID

Sample code to retrieve the `datasource_id` from a published data source using the **Project Name** and **Published Data
Source Name**.

### Reference

* https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_data_sources.htm

## Step 3: Get Column Names

When creating Tableau Pulse Metric Definitions, you need to know the column names.

* You can use the Tableau Pulse Datasource Endpoint to get the column names.
* Generally, you should already know which columns you have and set them as metric filters or calculations.

### Reference

* Learning by Doing !

## Step 4: Create Metric Definitions

In my opinion, the most challenging aspect of developing with the Tableau Pulse REST API is crafting the very **exact**
payload. Even when using the manual method to create metric definitions, it requires input in over ten different
settings.

### Reference

* https://help.tableau.com/current/api/rest_api/en-us/REST/TAG/index.html#tag/Pulse-Methods/operation/MetricQueryService_CreateDefinition

## Step 4.1: Create Simple Summarization Metric Definition

Using Standard **AGGREGATION_SUM**

* Running Total can be **True** only for **AGGREGATION_SUM**

## Step 4.2: Create Other Aggregation Metric Definition

When using other aggregation types

* `AGGREGATION_AVERAGE / AGGREGATION_MEDIAN / AGGREGATION_MAX / AGGREGATION_MIN / AGGREGATION_COUNT / AGGREGATION_COUNT_DISTINCT`
* Running Total can only be **False**

## Step 4.3: Create Customized Calculation

This is the most challenging part, you need to conduct the very exact **viz_state_string**

* Aggregation and Base Measure will not be used for Customized Calculation
* Sample Payload

* `{"vizState":{"rows":[{"fieldOnShelf":{"component":["Calculation_Pulse"]},"fieldCaption":"Calculation_Pulse"}],"columns":[{"fieldOnShelf":{"component":["[Month]"]},"fieldCaption":"[Month]"}]},"dataModel":{"dataSource":[{"columnsToAdd":[{"name":{"component":["Calculation_Pulse"]},"fieldType":"FIELD_TYPE_CONTINUOUS","pivotStrategy":"FIELD_PIVOT_STRATEGY_PIVOT_ON_KEY","role":"FIELD_ROLE_MEASURE","dataType":"DATA_TYPE_REAL_TYPE","calc":{"formula":"SUM([Sales])/{FIXED : SUM([Sales])}"}}]}]}}`

This can be very complicated, but it is still manageable :)

## Step 5: List Metrics

### Reference

* https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_pulse.htm#MetricQueryService_ListMetrics
* https://help.tableau.com/current/api/rest_api/en-us/REST/TAG/index.html#tag/Pulse-Methods/operation/MetricQueryService_ListMetrics

## Step 6: Create Metrics

Here is the combinations of two values (Granularity, Range)

* Granularity can be set
  as `GRANULARITY_BY_YEAR / GRANULARITY_BY_QUARTER / GRANULARITY_BY_MONTH / GRANULARITY_BY_WEEK / GRANULARITY_BY_DAY`
* Range can be set as `RANGE_CURRENT_PARTIAL / RANGE_LAST_COMPLETE`

If **Anchor Date** = 20 June 2024 (Yeah, It is the Data Dev Day !)

| Granularity / Range        | RANGE_CURRENT_PARTIAL                 | RANGE_LAST_COMPLETE               |
|----------------------------|---------------------------------------|-----------------------------------|
| **GRANULARITY_BY_YEAR**    | Year to Date (1 Jan '24 - 20 Jun '24) | Last Year (1 Jan - 31 Dec '24)    |
| **GRANULARITY_BY_QUARTER** | Qtr to Date (1 Apr '24 - 20 Jun '24)  | Last Quarter (1 Jan - 31 Mar '24) |
| **GRANULARITY_BY_MONTH**   | Month to Date (1 - 20 Jun '24)        | Last Month (1 - 30 May '24)       |
| **GRANULARITY_BY_WEEK**    | Week to Date  (16 - 20 Jun '24)       | Last Week (9 - 15 Jun '24)        |
| **GRANULARITY_BY_DAY**     | Today (20 Jun '24)                    | Yesterday (19 Jun' 24)            |

* And then the time comparison, can be set as `TIME_COMPARISON_PREVIOUS_PERIOD / TIME_COMPARISON_YEAR_AGO_PERIOD`
* In general, you will beed to set as **TIME_COMPARISON_PREVIOUS_PERIOD**, if it is not YTD / Prior YTD, you will need
  to always set as this value.

### Reference

* https://help.tableau.com/current/api/rest_api/en-us/REST/TAG/index.html#tag/Pulse-Methods/operation/MetricQueryService_CreateDefinition
* https://www.postman.com/salesforce-developers/workspace/salesforce-developers/request/12721794-ac634b69-dd89-49f3-8ff2-a67066c23f64

## Step 6.1: Create the metric one-by-one

You may add more payload because, by default Tableau Pulse created Month to Date metric for you (it is the most common metric !)

### Reference 
* https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_pulse.htm#MetricQueryService_CreateMetric

## Step 6.2: Looping create the metric (I want it all !)

You can reuse the code from Step 6.1 and make a for loop !

* granularity_list = `['GRANULARITY_BY_YEAR', 'GRANULARITY_BY_QUARTER', 'GRANULARITY_BY_MONTH', 'GRANULARITY_BY_WEEK']`
* range_list = `['RANGE_CURRENT_PARTIAL', 'RANGE_LAST_COMPLETE']`

### Reference
* https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_pulse.htm#MetricQueryService_CreateMetric
