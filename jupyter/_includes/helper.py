import requests
import json
import pandas as pd


class APIHelper:
    def __init__(self, config_dict, verbose=False):

        required_keys = {"server", "token_name", "token_secret", "content_url", "api_version"}
        if set(config_dict.keys()) != required_keys:
            raise ValueError("config_dict does not have the required keys.")

        self.server = config_dict["server"]
        self.token_name = config_dict["token_name"]
        self.token_secret = config_dict["token_secret"]
        self.content_url = config_dict["content_url"]
        self.api_version = config_dict["api_version"]

        self.base_url = f'{self.server}/api/{self.api_version}'

        self.headers = {}
        self.base_site_url = None
        self.base_api_url = None
        self.token = None
        self.site_id = None
        self.user_id = None
        self.verbose = verbose
        self.authenticate()

    def authenticate(self):
        api_url = f'{self.base_url}/auth/signin'

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        payload = {
            'credentials': {
                'personalAccessTokenName': self.token_name,
                'personalAccessTokenSecret': self.token_secret,
                'site': {
                    'contentUrl': self.content_url
                }
            }
        }

        response = requests.post(api_url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 200:
            response_json = response.json()
            self.token = response_json['credentials']['token']
            self.site_id = response_json['credentials']['site']['id']
            self.user_id = response_json['credentials']['user']['id']
            self.headers['X-Tableau-Auth'] = self.token

            self.base_site_url = f'{self.server}/api/{self.api_version}/sites/{self.site_id}'
            self.base_api_url = f' {self.server}/api/-'

            print(f'Authentication successful')
            if self.verbose:
                print(f'Site ID: {self.site_id[0:8]}-xxxxxxxx')
                print(f'User ID: {self.user_id[0:8]}-xxxxxxxx')
                print(f'Token  : {self.token[0:8]}-xxxxxxxx')
            else:
                pass
            print(f'Base Site URL : {self.server}/api/{self.api_version}/sites/{self.site_id[0:8]}-xxxxxxxx')
            print(f'Base API URL  : {self.server}/api/-')
        else:
            print(f'Failed to authenticate. Status code: {response.status_code}')
            print(f'Error message: {response.text}')

    def get_datasource_dict(self):
        api_url = f'{self.base_site_url}/datasources'
        response = requests.get(api_url, headers=self.headers)
        items = response.json()['datasources']['datasource']

        extracted_data = [
            (item.get('id'), item.get('name'), item.get('type'), item.get('project', {}).get('name'),
             item.get('owner', {}).get('name'))
            for item in items
        ]
        sorted_data = sorted(extracted_data, key=lambda x: (x[3], x[1]))
        datasource_dict = {}
        for item in sorted_data:
            datasource_dict[item[1]] = item[0]
        return datasource_dict

    def get_datasource_dict_tuple(self):
        api_url = f'{self.base_site_url}/datasources'
        response = requests.get(api_url, headers=self.headers)
        items = response.json()['datasources']['datasource']

        extracted_data = [
            (item.get('id'), item.get('name'), item.get('type'), item.get('project', {}).get('name'),
             item.get('owner', {}).get('name'))
            for item in items
        ]
        sorted_data = sorted(extracted_data, key=lambda x: (x[3], x[1]))
        datasource_dict_tuple = {}
        for item in sorted_data:
            datasource_dict_tuple[(item[3], item[1])] = item[0]
        return datasource_dict_tuple

    def get_user_dict(self):
        api_url = f'{self.base_site_url}/users'
        response = requests.get(api_url, headers=self.headers)
        items = response.json()['users']['user']

        extracted_data = [
            (item.get('id'), item.get('name'), item.get('siteRole'), item.get('email'))
            for item in items
        ]
        sorted_data = sorted(extracted_data, key=lambda x: x[1])
        user_dict = {}
        for item in sorted_data:
            user_dict[item[1]] = item[0]
        return user_dict

    def get_pulse_metric_definitions_dict(self):

        api_url = f'{self.base_api_url}/pulse/definitions'

        metadata_list = []
        api_response = requests.get(api_url, headers=self.headers)
        api_response_json = api_response.json()
        metadata_list.extend(api_response_json['definitions'])

        while 'next_page_token' in api_response_json and api_response_json['next_page_token'] != '':
            next_page_token = api_response_json['next_page_token']
            api_response = requests.get(f'{api_url}?pageToken={next_page_token}', headers=self.headers)
            api_response_json = api_response.json()
            metadata_list.extend(api_response_json['definitions'])

        definition_dict = {}

        for item in metadata_list:
            metadata = item.get('metadata', {})
            metadata_name = metadata.get('name', {})
            metadata_id = metadata.get('id', {})
            definition_dict[metadata_name] = metadata_id

        return definition_dict

    def get_metrics_list_by_definition_id(self, definition_id):
        metric_list = []
        endpoint = f'{self.base_api_url}/pulse/definitions/{definition_id}/metrics'
        api_response = requests.get(endpoint, headers=self.headers)
        api_response_json = api_response.json()
        metric_list.extend(api_response_json['metrics'])

        while 'next_page_token' in api_response_json and api_response_json['next_page_token'] != '':
            next_page_token = api_response_json['next_page_token']
            api_response = requests.get(f'{endpoint}?pageToken={next_page_token}', headers=self.headers)
            api_response_json = api_response.json()
            metric_list.extend(api_response_json['metrics'])

        metric_data_list = []

        for metric in metric_list:
            metric_data_list.append({
                'definition_id': metric['definition_id'],
                'metric_id': metric['id'],
                'granularity': metric['specification']['measurement_period']['granularity'],
                'range': metric['specification']['measurement_period']['range'],
            })

        return metric_data_list

    def get_user_df(self):
        api_url = f'{self.base_site_url}/users'
        response = requests.get(api_url, headers=self.headers)
        items = response.json()['users']['user']

        extracted_data = [
            (item.get('id'), item.get('name'))
            for item in items
        ]
        sorted_data = sorted(extracted_data, key=lambda x: x[1])

        user_df = pd.DataFrame(sorted_data, columns=['user_id', 'user_name'])
        user_df['user_name'] = user_df['user_name'].apply(
            lambda email: email[:2] + '*****@' + 'domain.com'
        )
        return user_df


    def get_pulse_metric_definitions_and_metrics_df(self, filter=None):

        api_url = f'{self.base_api_url}/pulse/definitions'

        metadata_list = []
        api_response = requests.get(api_url, headers=self.headers)
        api_response_json = api_response.json()
        metadata_list.extend(api_response_json['definitions'])

        while 'next_page_token' in api_response_json and api_response_json['next_page_token'] != '':
            next_page_token = api_response_json['next_page_token']
            api_response = requests.get(f'{api_url}?pageToken={next_page_token}', headers=self.headers)
            api_response_json = api_response.json()
            metadata_list.extend(api_response_json['definitions'])

        definition_dict = {}

        for item in metadata_list:
            metadata = item.get('metadata', {})
            metadata_name = metadata.get('name', {})
            metadata_id = metadata.get('id', {})
            specification = item.get('specification', {})
            datasource_id = specification.get('datasource', {}).get('id', ''),
            definition_dict[metadata_name] = metadata_id

        if filter:
            definition_dict = {key: value for key, value in definition_dict.items() if filter in key}

        definition_df = pd.DataFrame(list(definition_dict.items()), columns=['definition_name', 'definition_id'])

        definition_id_list = list(definition_dict.values())

        metric_data_list = []

        for definition_id in definition_id_list:
            print(f'Processing : {definition_id}')
            metric_list = self.get_metrics_list_by_definition_id(definition_id)
            metric_data_list.extend(metric_list)

        metric_df = pd.DataFrame(metric_data_list, columns=['definition_id', 'metric_id', 'granularity', 'range'])

        df = definition_df.merge(metric_df, how='left')
        df = df[['definition_id', 'definition_name', 'metric_id', 'granularity', 'range']]

        return df

    def get_pulse_subscription_df(self):
        api_url = f'{self.base_api_url}/pulse/subscriptions'

        subscription_list = []
        api_response = requests.get(api_url, headers=self.headers)
        api_response_json = api_response.json()
        subscription_list.extend(api_response_json['subscriptions'])

        while 'next_page_token' in api_response_json and api_response_json['next_page_token'] != '':
            next_page_token = api_response_json['next_page_token']
            api_response = requests.get(f'{api_url}?pageToken={next_page_token}', headers=self.headers)
            api_response_json = api_response.json()
            subscription_list.extend(api_response_json['subscriptions'])

        subscription_detail_list = []

        for item in subscription_list:
            subscription_id = item.get('id', '')
            metric_id = item.get('metric_id', '')
            user_id = item.get('follower', {}).get('user_id', '')

            subscription_detail_list.append({
                'subscription_id': subscription_id,
                'metric_id': metric_id,
                'user_id': user_id
            })

        df = pd.DataFrame(subscription_detail_list, columns=['subscription_id', 'metric_id', 'user_id'])
        return df

if __name__ == '__main__':

    # Code Testing

    import config as config

    config_dict = config.config_dict

    helper = APIHelper(config_dict)

    datasource_dict = helper.get_datasource_dict()
    print(datasource_dict)

    datasource_dict_tuple = helper.get_datasource_dict_tuple()
    print(datasource_dict_tuple)

    user_dict = helper.get_user_dict()
    print(user_dict)

    definition_dict = helper.get_pulse_metric_definitions_dict()
    print(definition_dict)

    subscription_df = helper.get_pulse_subscription_df()
    print(subscription_df)

    metric_df = helper.get_pulse_metric_definitions_and_metrics_df(filter='DataDev')
    print(metric_df)
