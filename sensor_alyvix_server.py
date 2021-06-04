#!/usr/bin/env python3


"""
    PRTG custom sensor for Alyvix Server
    Copyright (C) 2021 Francesco Melchiori
    <https://www.francescomelchiori.com/>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see
    <http://www.gnu.org/licenses/>.
"""


import argparse
import json
import socket
import ssl
import urllib.request

from prtg.sensor.result import CustomSensorResult


class AlyvixServerMeasure:
    def __init__(self,
                 timestamp_epoch,  # 1619000540323290112
                 hostname,  # "alyvixserver"
                 domain_username,  # "CO\\AlyvixUser05"
                 test_case_alias,  # "visittrentino"
                 test_case_duration_ms,  # 13998
                 test_case_exit,  # "true"
                 test_case_state,  # 0
                 transaction_alias,  # "vt_home_ready"
                 transaction_performance_ms,  # 4689
                 transaction_exit,  # "true"
                 transaction_state,  # 0
                 test_case_name=None,  # "visittrentino"
                 test_case_arguments=None,  # "text"
                 test_case_execution_code=None,  # "pb02Al05vino1619000538"
                 transaction_name=None,  # "vt_home_ready"
                 transaction_group=None,  # "text"
                 transaction_detection_type=None,  # "appear"
                 transaction_timeout_ms=None,  # 10000
                 transaction_warning_ms=None,  # null
                 transaction_critical_ms=None,  # null
                 transaction_accuracy_ms=None,  # 82
                 transaction_record_text=None,  # "text"
                 transaction_record_extract=None,  # "text"
                 transaction_resolution_width=None,  # 1280
                 transaction_resolution_height=None,  # 800
                 transaction_scaling_factor=None):  # 100
        self.timestamp_epoch = timestamp_epoch
        self.hostname = hostname
        self.domain_username = domain_username
        self.test_case_alias = test_case_alias
        self.test_case_duration_ms = test_case_duration_ms
        self.test_case_exit = test_case_exit
        self.test_case_state = test_case_state
        self.transaction_alias = transaction_alias
        self.transaction_performance_ms = transaction_performance_ms
        self.transaction_exit = transaction_exit
        self.transaction_state = transaction_state
        self.test_case_name = test_case_name
        self.test_case_arguments = test_case_arguments
        self.test_case_execution_code = test_case_execution_code
        self.transaction_name = transaction_name
        self.transaction_group = transaction_group
        self.transaction_detection_type = transaction_detection_type
        self.transaction_timeout_ms = transaction_timeout_ms
        self.transaction_warning_ms = transaction_warning_ms
        self.transaction_critical_ms = transaction_critical_ms
        self.transaction_accuracy_ms = transaction_accuracy_ms
        self.transaction_record_text = transaction_record_text
        self.transaction_record_extract = transaction_record_extract
        self.transaction_resolution_width = transaction_resolution_width
        self.transaction_resolution_height = transaction_resolution_height
        self.transaction_scaling_factor = transaction_scaling_factor


class AlyvixServerPRTGMeasure(AlyvixServerMeasure):
    def __repr__(self):
        return self.output_measure()

    def output_measure(self):
        prtg_agent_measure_output = ''
        prtg_agent_separator = ''
        prtg_agent_none = ''
        prtg_agent_measure_output += '{0}={1};{2};{3};;{4}'.format(
            self.transaction_alias,
            self.transaction_performance_ms
            if self.transaction_performance_ms else prtg_agent_none,
            self.transaction_performance_ms
            if self.transaction_warning_ms else prtg_agent_none,
            self.transaction_performance_ms
            if self.transaction_critical_ms else prtg_agent_none,
            prtg_agent_separator)
        return prtg_agent_measure_output

    def output_testcase(self):
        prtg_agent_measure_output = ''
        prtg_agent_separator = ' '
        prtg_agent_none = ''
        prtg_agent_measure_output += '{0}{1}'.format(
            self.test_case_state, prtg_agent_separator)
        prtg_agent_measure_output += '"Alyvix {0}"{1}'.format(
            self.test_case_alias, prtg_agent_separator)
        prtg_agent_measure_output += '{0}={1};;;;'.format(
            'duration',
            self.test_case_duration_ms
            if self.test_case_duration_ms else prtg_agent_none)
        return prtg_agent_measure_output


class AlyvixServerPRTGSensor:
    def __init__(self,
                 alyvix_server_https_url,
                 test_case_alias):
        self.alyvix_server_https_url = alyvix_server_https_url
        self.test_case_alias = test_case_alias
        self.alyvix_server_request = ''
        self.alyvix_server_response = {}
        try:
            self.get_alyvix_server_data()
        except urllib.error.URLError:
            print('Please, check --alyvix_server_https_url ({0})'.
                  format(self.alyvix_server_request))
            raise SystemExit
        self.alyvix_server_measure_response = None
        self.alyvix_server_prtg_measure = None
        self.alyvix_server_prtg_measures = []
        self.alyvix_server_prtg_testcase = None
        self.build_alyvix_server_prtg_measures()

    def __repr__(self):
        prtg_agent_output = ''
        if self.alyvix_server_response['measures']:
            prtg_agent_output += \
                self.alyvix_server_prtg_testcase.output_testcase()
            prtg_agent_output += '|'
            prtg_agent_output += \
                '|'.join(
                    [self.alyvix_server_prtg_measure.output_measure()
                     for self.alyvix_server_prtg_measure
                     in self.alyvix_server_prtg_measures])
            prtg_agent_output += ' Test case report: '
            prtg_agent_output += \
                '{0}/v0/testcases/{1}/reports/?runcode={2}'.format(
                    self.alyvix_server_https_url, self.test_case_alias,
                    self.alyvix_server_prtg_testcase.
                    test_case_execution_code)
        return prtg_agent_output

    def get_alyvix_server_data(self):
        self.alyvix_server_request = '{0}/v0/testcases/{1}/'.format(
            self.alyvix_server_https_url, self.test_case_alias)
        ssl._create_default_https_context = \
            ssl._create_unverified_context
        self.alyvix_server_response = json.load(
            urllib.request.urlopen(self.alyvix_server_request))
        return self.alyvix_server_response

    def build_alyvix_server_prtg_measure(self):
        self.alyvix_server_prtg_measure = AlyvixServerPRTGMeasure(
            timestamp_epoch=self.alyvix_server_measure_response[
                'timestamp_epoch'],
            hostname=self.alyvix_server_measure_response[
                'hostname'],
            domain_username=self.alyvix_server_measure_response[
                'domain_username'],
            test_case_alias=self.alyvix_server_measure_response[
                'test_case_alias'],
            test_case_duration_ms=self.alyvix_server_measure_response[
                'test_case_duration_ms'],
            test_case_exit=self.alyvix_server_measure_response[
                'test_case_exit'],
            test_case_state=self.alyvix_server_measure_response[
                'test_case_state'],
            transaction_alias=self.alyvix_server_measure_response[
                'transaction_alias'],
            transaction_performance_ms=self.alyvix_server_measure_response[
                'transaction_performance_ms'],
            transaction_exit=self.alyvix_server_measure_response[
                'transaction_exit'],
            transaction_state=self.alyvix_server_measure_response[
                'transaction_state'],
            test_case_name=self.alyvix_server_measure_response[
                'test_case_name'],
            test_case_arguments=self.alyvix_server_measure_response[
                'test_case_arguments'],
            test_case_execution_code=self.alyvix_server_measure_response[
                'test_case_execution_code'],
            transaction_name=self.alyvix_server_measure_response[
                'transaction_name'],
            transaction_group=self.alyvix_server_measure_response[
                'transaction_group'],
            transaction_detection_type=self.alyvix_server_measure_response[
                'transaction_detection_type'],
            transaction_timeout_ms=self.alyvix_server_measure_response[
                'transaction_timeout_ms'],
            transaction_warning_ms=self.alyvix_server_measure_response[
                'transaction_warning_ms'],
            transaction_critical_ms=self.alyvix_server_measure_response[
                'transaction_critical_ms'],
            transaction_accuracy_ms=self.alyvix_server_measure_response[
                'transaction_accuracy_ms'],
            transaction_record_text=self.alyvix_server_measure_response[
                'transaction_record_text'],
            transaction_record_extract=self.alyvix_server_measure_response[
                'transaction_record_extract'],
            transaction_resolution_width=self.alyvix_server_measure_response[
                'transaction_resolution_width'],
            transaction_resolution_height=self.alyvix_server_measure_response[
                'transaction_resolution_height'],
            transaction_scaling_factor=self.alyvix_server_measure_response[
                'transaction_scaling_factor'])
        return self.alyvix_server_prtg_measure

    def build_alyvix_server_prtg_measures(self):
        if self.alyvix_server_response['measures']:
            self.alyvix_server_prtg_measures = [
                self.build_alyvix_server_prtg_measure() for
                self.alyvix_server_measure_response in
                self.alyvix_server_response['measures']]
            self.select_alyvix_server_prtg_measures()
            self.alyvix_server_prtg_testcase = \
                self.alyvix_server_prtg_measures[0]
        return self.alyvix_server_prtg_measures

    def select_alyvix_server_prtg_measures(
            self, selection_criterion='last_measures'):
        if selection_criterion == 'last_measures':
            execution_codes = [
                (measure.timestamp_epoch, measure.test_case_execution_code)
                for measure in self.alyvix_server_prtg_measures]
            last_execution_code = max(execution_codes)[1]
            self.alyvix_server_prtg_measures = [
                measure
                for measure in self.alyvix_server_prtg_measures
                if measure.test_case_execution_code == last_execution_code]
        return self.alyvix_server_prtg_measures


class AlyvixServerTestcases:
    def __init__(self, alyvix_server_https_url):
        self.alyvix_server_https_url = alyvix_server_https_url
        self.alyvix_server_request = ''
        self.alyvix_server_response = {}
        try:
            self.get_alyvix_server_data()
        except urllib.error.URLError:
            print('Please, check --alyvix_server_https_url ({0})'.
                  format(self.alyvix_server_request))
            raise SystemExit
        self.alyvix_server_prtg_testcases = []
        self.get_alyvix_server_prtg_testcases()

    def __call__(self):
        return self.alyvix_server_prtg_testcases

    def get_alyvix_server_data(self):
        self.alyvix_server_request = '{0}/v0/testcases/'.format(
            self.alyvix_server_https_url)
        ssl._create_default_https_context = ssl._create_unverified_context
        self.alyvix_server_response = json.load(
            urllib.request.urlopen(self.alyvix_server_request))
        return self.alyvix_server_response

    def get_alyvix_server_prtg_testcases(self):
        if self.alyvix_server_response['testcases']:
            self.alyvix_server_prtg_testcases = [
                testcase_response['testcase_alias'] for testcase_response
                in self.alyvix_server_response['testcases']]
        return self.alyvix_server_prtg_testcases


def main():
    parser = argparse.ArgumentParser(
        description='This PRTG custom sensor uses the RESTful web API'
                    'of the Alyvix Server to gather transaction'
                    'measurements about a given ongoing Alyvix test'
                    'case.')
    parser.add_argument(
        '-a', '--alyvix_server_https_url',
        help='set the HTTPS URL to Alyvix Server (e.g.'
             'https://alyvixserver.co.lan)')
    parser.add_argument(
        '-t', '--test_case_alias',
        help='set the Alyvix test case alias (e.g. visittrentino)')

    args = parser.parse_args()
    if args.alyvix_server_https_url:
        alyvix_server_https_url = args.alyvix_server_https_url
    else:
        alyvix_server_https_url = 'https://'
        alyvix_server_https_url += socket.gethostbyname(
            socket.gethostname())
    if args.test_case_alias:
        alyvix_server_test_cases = [args.test_case_alias]
    else:
        alyvix_server_test_cases = AlyvixServerTestcases(
            alyvix_server_https_url)()

    for test_case_alias in alyvix_server_test_cases:
        alyvix_server_prtg_agent = AlyvixServerPRTGSensor(
            alyvix_server_https_url, test_case_alias)
        print(alyvix_server_prtg_agent)


def test():
    csr = CustomSensorResult(text='execution_code')

    csr.add_channel(name="duration",
                    value=100,
                    unit='ms')

    csr.add_channel(name="transaction_alias_1",
                    value=10,
                    unit='ms',
                    is_limit_mode=True,
                    limit_max_warning=20,
                    limit_max_error=30)

    csr.add_channel(name="transaction_alias_2",
                    value=10,
                    unit='ms',
                    is_limit_mode=True,
                    limit_max_warning=20,
                    limit_max_error=30)

    print(csr.json_result)


if __name__ == '__main__':
    # main()
    test()
