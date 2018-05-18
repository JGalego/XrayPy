#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Xray API Module
"""

import os
import re
import base64
import logging
import json
import requests

from requests.auth import HTTPBasicAuth
from xraypy import xrayutils

__author__ = "João Galego"
__copyright__ = "João Galego"
__license__ = "mit"

LOGGER = logging.getLogger(__name__)

JIRA_REST_API = "/rest/api/2"
XRAY_REST_API = "/rest/raven/1.0"

class XrayApiClient(object):
    """Wrapper for Xray's REST API Client"""

    def __init__(self, xray_properties):
        """XrayApiClient constructor

        :param xray_properties (str) path to the Xray properties JSON file
        """

        # Initialize LOGGER
        xrayutils.setup_logging(logging.INFO)

        # Load Xray properties
        with open(xray_properties) as file_props:
            self.properties = json.load(file_props)

    def get_project_info(self, project):
        """Returns the project info

        :param project (str) project key or ID
        """

        # Create URL
        url = self.properties["host"] + JIRA_REST_API + "/project/" + project

        # Make request
        LOGGER.info("GET %s", url)
        response = requests.get(url, \
                                auth=HTTPBasicAuth(self.properties["username"], \
                                                   self.properties["password"]))

        # Check status code
        if response.status_code != 200:
            LOGGER.error("%d: Failed to get project info", response.status_code)

        return json.loads(response.text)

    def get_project_id(self, project_key):
        """Returns the project ID

        :param project_key (str) project key
        """

        project_info = self.get_project_info(project_key)
        return project_info["id"]

    def get_issue_info(self, issue):
        """Returns information about a JIRA issue

        :param issue (str) issue key or id
        """

        # Create URL
        url = self.properties["host"] + JIRA_REST_API + "/issue/" + issue

        # Make request
        LOGGER.info("GET %s", url)
        if "username" in self.properties and "password" in self.properties:
            response = requests.get(url, \
                                    auth=HTTPBasicAuth(self.properties["username"], \
                                                       self.properties["password"]))
        else:
            response = requests.get(url)

        # Check status code
        if response.status_code != 200:
            LOGGER.error("%d: Failed to get issue info", response.status_code)

        return json.loads(response.text)

    def save_test_run(self, test_execution_key, test_run_info):
        """Saves a test run in the context of a test execution

        :param test_execution_key (str) test execution key
        :param test_run (dict) test run info
        """

        # Create URL
        url = self.properties["host"] + XRAY_REST_API + "/import/execution"

        # Create test run payload
        test_run = {'testExecutionKey': test_execution_key, 'tests': [test_run_info]}

        # Set up headers
        headers = {'content-type': 'application/json'}

        # Make request
        LOGGER.info("POST %s", url)
        response = requests.post(url, \
                                 data=json.dumps(test_run), \
                                 headers=headers, \
                                 auth=HTTPBasicAuth(self.properties["username"], \
                                                    self.properties["password"]))

        # Check status code
        if response.status_code != 201:
            LOGGER.error("%d: Failed to save test run", response.status_code)

        return json.loads(response.text)

    def get_test_run_info(self, test_execution_key, test_key):
        """Returns information about a test run

        :param test_execution_key (str) test execution key
        :param test_key (str) test key
        """

        # Create URL
        url = self.properties["host"] + XRAY_REST_API + \
                    "/api/testrun?testExecIssueKey=" + test_execution_key + \
                    "&testIssueKey=" + test_key

        # Make request
        LOGGER.info("GET %s", url)
        response = requests.get(url, \
                                auth=HTTPBasicAuth(self.properties["username"], \
                                                   self.properties["password"]))

        # Check status code
        if response.status_code != 200:
            LOGGER.error("%d: Failed to get test run info", response.status_code)

        return json.loads(response.text)

    def create_issue(self, issue):
        """Create an issue in JIRA

        :param issue (JSON) issue payload
        """

        # Create URL
        url = self.properties["host"] + JIRA_REST_API + "/issue"

        # Set up headers
        headers = {'content-type': 'application/json'}

        # Make request
        LOGGER.info("POST %s", url)
        response = requests.post(url, \
                                 data=json.dumps(issue), \
                                 headers=headers, \
                                 auth=HTTPBasicAuth(self.properties["username"], \
                                                    self.properties["password"]))

        # Check status code
        if response.status_code != 201:
            LOGGER.error("%d: Failed to create issue", response.status_code)

        return json.loads(response.text)

    def create_manual_test(self, project_key, summary, description):
        """Creates a manual Test issue in JIRA

        :param project_key (str) project key
        :param summary (str) issue summary
        :param description (str) issue description
        """

        # Get project ID
        project_id = self.get_project_id(project_key)

        # Create test issue payload
        issue = {'fields': {'project': {'id': project_id}, 'summary': summary, \
                    'description': description, 'issuetype': {'name': 'Test'}}}

        # Make request
        response = self.create_issue(issue)

        return response

    def create_test_set(self, project_key, summary, description):
        """Creates a Test Set issue in JIRA

        :param project_key (str) project key
        :param summary (str) issue summary
        :param description (str) issue description
        """

        # Get project ID
        project_id = self.get_project_id(project_key)

        # Create test set issue payload
        issue = {'fields': {'project': {'id': project_id}, 'summary': summary, \
                    'description': description, 'issuetype': {'name': 'Test Set'}}}

        # Make request
        response = self.create_issue(issue)

        return response

    def create_test_plan(self, project_key, summary, description):
        """Creates a Test Plan issue in JIRA

        :param project_key (str) project key
        :param summary (str) issue summary
        :param description (str) issue description
        """

        # Get project ID
        project_id = self.get_project_id(project_key)

        # Create test plan issue payload
        issue = {'fields': {'project': {'id': project_id}, 'summary': summary, \
                    'description': description, 'issuetype': {'name': 'Test Plan'}}}

        # Make request
        response = self.create_issue(issue)

        return response

    def create_test_execution(self, project_key, summary, description):
        """Creates a Test Execution issue in JIRA

        :param project_key (str) project key
        :param summary (str) issue summary
        :param description (str) issue description
        """

        # Get project ID
        project_id = self.get_project_id(project_key)

        # Create test execution issue payload
        issue = {'fields': {'project': {'id': project_id}, 'summary': summary, \
                    'description': description, 'issuetype': {'name': 'Test Execution'}}}

        # Make request
        response = self.create_issue(issue)

        return response

    def add_evidence_to_test_run(self, test_run_id, evidence, content_type):
        """Uploads evidence files to a test run

        :param test_run_id (str) test run ID
        :param evidence (str) path to the evidence file
        :param content_type (str) content type of the evidence file
        """

        # Create URL
        url = self.properties["host"] + XRAY_REST_API + \
                    "/api/testrun/" + test_run_id + "/attachment"

        # Encode the file contents with Base64
        encoded_data = ""
        with open(evidence, "rb") as evidence_file:
            encoded_data = base64.b64encode(evidence_file.read())

        # Get file name
        filename = os.path.basename(evidence)

        # Create attachment payload
        attachment = {'data': encoded_data, 'filename': filename, 'contentType': content_type}

        # Set up headers
        headers = {'content-type': 'application/json'}

        # Make request
        LOGGER.info("POST %s", url)
        response = requests.post(url, \
                                 data=json.dumps(attachment), \
                                 headers=headers, \
                                 auth=HTTPBasicAuth(self.properties["username"], \
                                                    self.properties["password"]))

        # Check status code
        if response.status_code != 201:
            LOGGER.error("%d: Failed to upload test run evidence", response.status_code)

        return json.loads(response.text)

    def export_results(self, **kwargs):
        """Exports test run results from JIRA by
            1. Test Execution Key + Test Key
            2. Test Execution Key
            3. Test Plan Key
            4. Saved Filter ID

        Example:
            export_results(test_execution_key="...", test_key="...")
            export_results(test_execution_key="...")
            export_results(test_plan_key="...")
            export_results(saved_filter_id="...")
        """

        # Create base URL
        url = self.properties["host"] + XRAY_REST_API + "/testruns?"

        # Add URL suffix
        if "test_execution_key" in kwargs and "test_key" in kwargs:
            url += "testExecKey=" + kwargs["test_execution_key"] + \
                   "&testKey=" + kwargs["test_key"]
        elif "test_plan_Key" in kwargs:
            url += "testPlanKey=" + kwargs["test_plan_key"]
        elif "test_execution_key" in kwargs:
            url += "testExecKey=" + kwargs["test_execution_key"]
        elif "saved_filter_id" in kwargs:
            url += "savedFilterId=" + kwargs["saved_filter_id"]

        # Make request
        LOGGER.info("GET %s", url)
        response = requests.get(url, \
                                auth=HTTPBasicAuth(self.properties["username"], \
                                                   self.properties["password"]))

        # Check status code
        if response.status_code != 200:
            LOGGER.error("%d: Failed to export results from JIRA", response.status_code)

        return json.loads(response.text)

    def import_json_results(self, json_results):
        """Import JSON results to JIRA

        :param json_results (str) path to the JSON results
        """
        # Create base URL
        url = self.properties["host"] + XRAY_REST_API + "/import/execution"

        # Make request
        LOGGER.info("POST %s", url)
        response = requests.post(url, \
                                 data=json.dumps(json_results), \
                                 auth=HTTPBasicAuth(self.properties["username"], \
                                 self.properties["password"]), \
                                 verify=False)

        # Check status code
        if response.status_code != 200:
            LOGGER.error("%d: Failed to import JSON results to JIRA", response.status_code)

        return json.loads(response.text)

    def import_junit_results(self, junit_xml_report, project_key, **kwargs):
        """Import JUnit results to JIRA

        :param junit_xml_report (str) path to the JUnit XML report
        :param project_key (str) project key
        """
        # Create base URL
        url = self.properties["host"] + XRAY_REST_API + \
                                            "/import/execution/junit?projectKey=%s" % project_key

        # Add Test Plan key
        if "test_plan_key" in kwargs:
            if kwargs["test_plan_key"]:
                url += "&testPlanKey=%s" % kwargs["test_plan_key"]

        # Add Test environments
        if "test_environments" in kwargs:
            if kwargs["test_environments"]:
                url += "&testEnvironments=%s" % kwargs["test_environments"]

        # Add revision
        if "revision" in kwargs:
            if kwargs["revision"]:
                url += "&revision=%s" % kwargs["revision"]

        # Add fix version
        if "fix_version" in kwargs:
            if kwargs["fix_version"]:
                url += "&fixVersion=%s" % kwargs["fix_version"]

        # Create multipart form
        files = {'file': (os.path.basename(junit_xml_report), open(junit_xml_report, 'rb'), \
                                                            'application/xml', {'Expires': '0'})}

        # Make request
        LOGGER.info("POST %s", url)
        response = requests.post(url, \
                                 files=files, \
                                 auth=HTTPBasicAuth(self.properties["username"], \
                                 self.properties["password"]), \
                                 verify=False)

        # Check status code
        if response.status_code != 200:
            LOGGER.error("%d: Failed to import JUnit results to JIRA", response.status_code)

        return json.loads(response.text)

    def run_jql_query(self, jql_query):
        """Runs a JQL query

        :param jql_query (str) JQL query
        """

        # Encode unsupported characters in the JQL query so it can be used in the URI
        # For more information, please check RFC 3986
        jql_query = re.sub(r"\s+", '%20', jql_query)
        jql_query = re.sub(r"=", '%3D', jql_query)

        # Create URL
        url = self.properties["host"] + JIRA_REST_API + "/search?jql=" + jql_query

        # Make request
        LOGGER.info("GET %s", url)
        response = requests.get(url, \
                                auth=HTTPBasicAuth(self.properties["username"], \
                                                   self.properties["password"]))

        # Check status code
        if response.status_code != 200:
            LOGGER.error("%d: Failed to run JQL query", response.status_code)

        return json.loads(response.text)
