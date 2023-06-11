"""
Daksha
Copyright (C) 2021 myKaarma.
opensource@mykaarma.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from github import Github
import yaml
import base64
import os
from engine.logs import *

STORAGE_PATH=os.environ.get('STORAGE_PATH', 'reports')
GIT_USER=os.environ.get('GIT_USER', '')
GIT_PASS=os.environ.get('GIT_PASS', '')
REPO_ORG=os.environ.get('REPO_ORG', '')
REPO_USER = os.environ.get('REPO_USER', '')


def git_login():
    if len(GIT_USER) == 0 or len(GIT_PASS) == 0:
        github = Github()
        return get_org_instance(github, REPO_USER, REPO_ORG)
    else:
        github = Github(GIT_USER, GIT_PASS)
        return get_org_instance(github, REPO_USER, REPO_ORG)


def get_file_content(repo_name, branch_name, file_path):
    org = git_login()
    repo = org.get_repo(repo_name)
    file_content = repo.get_contents(file_path, branch_name)
    return file_content


def download_file_content(file_content, cron_store):
    content = base64.b64decode(file_content.content)
    ymlcontent = yaml.full_load(content)
    file_path = f"{STORAGE_PATH}/{cron_store}/"

    try:
        with open(file_path + file_content.name, "w") as file:
            yaml.dump(ymlcontent, file)
            file.close()
    except IOError as exc:
        logger.info("Cron_File_Path/Repo_Name/Branch_Name given incorrectly ")
        pass


# read yaml file
def read_yaml(repo, branch, file_path, cron_store):
    try:
        file_content = get_file_content(repo, branch, file_path)
        download_file_content(file_content, cron_store)
        file_name = f"{STORAGE_PATH}/{cron_store}/{file_content.name}"
        with open(file_name, 'r') as stream:
            yaml_content = yaml.full_load(stream)
            return yaml_content
    except Exception:
        logger.info("Cron_File_Path/Repo_Name/Branch_Name given incorrectly ")
        return None


def get_org_instance(github, repo_user, repo_org):
    if len(repo_user) != 0 and len(repo_org) != 0:
        raise Exception("Please provide either REPO_USER or REPO_ORG, terminating engine...")
    if len(repo_user) == 0 and len(repo_org) == 0:
        raise Exception("Both REPO_USER or REPO_ORG are empty, please provide one, terminating engine...")
    if len(repo_org) != 0:
        org = github.get_organization(repo_org)
    else:
        org = github.get_user(repo_user)
       
    return org

