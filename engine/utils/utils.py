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
from daksha.settings import STORAGE_PATH, GIT_USER, GIT_PASS, REPO_ORG, REPO_USER
from engine.logs import *
import subprocess
from daksha.settings import SCRIPT_DIR
import os
import traceback
from subprocess import Popen, PIPE



def git_login():
    if len(GIT_USER) == 0 or len(GIT_PASS) == 0:
        logger.info("Username OR password not given, mode is : public repository")
        github = Github()
        return get_org_instance(github, REPO_USER, REPO_ORG)
    else:
        github = Github(GIT_USER, GIT_PASS)
        return get_org_instance(github, REPO_USER, REPO_ORG)


def get_file_content(repo_name, branch_name, file_path):
    org = git_login()
    logger.info("Fetching the content from %s of %s branch %s ", file_path, repo_name, branch_name)
    repo = org.get_repo(repo_name)
    file_content = repo.get_contents(file_path, branch_name)
    return file_content


# Download the file from github
def download_file_content(file_content, test_id):
    content = base64.b64decode(file_content.content)
    ymlcontent = yaml.full_load(content)
    logger.info(ymlcontent)
    file_path = f"{STORAGE_PATH}/{test_id}/"

    try:
        with open(file_path + file_content.name, "w") as file:
            yaml.dump(ymlcontent, file)
            file.close()
        logger.info(file_content.name)
        logger.info("File %s downloaded", file_content.path)
    except IOError as exc:
        logger.error('Error creating file : %s', exc)


# read yaml file
def read_yaml(repo, branch, file_path, test_id):
    try:
        file_content = get_file_content(repo, branch, file_path)
        download_file_content(file_content, test_id)
        file_name = f"{STORAGE_PATH}/{test_id}/{file_content.name}"
        with open(file_name, 'r') as stream:
            yaml_content = yaml.load(stream)
            logger.info("Find your text file at location %s" % file_name)
            return yaml_content
    except Exception:
        logger.error("File %s is not present in %s branch of %s" % (file_path, branch, repo))
        return None


def read_local_yaml(file_path):
    with open(file_path, 'r') as stream:
        yaml_content = yaml.load(stream)
        return yaml_content


def get_org_instance(github, repo_user, repo_org):
    if len(repo_user) != 0 and len(repo_org) != 0:
        logger.error("Please provide either REPO_USER or REPO_ORG")
        raise Exception("Please provide either REPO_USER or REPO_ORG, terminating engine...")
    if len(repo_user) == 0 and len(repo_org) == 0:
        logger.error("Both REPO_USER or REPO_ORG are empty, please provide one")
        raise Exception("Both REPO_USER or REPO_ORG are empty, please provide one, terminating engine...")
    if len(repo_org) != 0:
        logger.info("REPO_ORG is present in config, accessing via : get_organization")
        org = github.get_organization(repo_org)
    else:
        logger.info("REPO_USER is present in config, accessing via : get_user")
        org = github.get_user(repo_user)
    return org


def execute_bash_file(**kwargs):
    """
    execute shell script file
    should run with sh
    """
    try:
        file_name = kwargs['name']
        subprocess.call(['sh', os.path.join(SCRIPT_DIR, file_name)])
        logger.info(file_name + " Bash File executed successfully")
        return True, None
    except KeyError:
        raise Exception("argument 'name' must be present in the list of args")
    except Exception as e:
        error_stack = traceback.format_exc()
        logger.error("Unable to executed Bash File : "+error_stack)
        return False, error_stack


def execute_bash_script(**kwargs):
    """
    execute shell script
    """
    try:
        script = kwargs['script']
        p = Popen(script, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        logger.info("Successfully executed the script ".join(script))
        return True, output
    except KeyError:
        raise Exception("argument 'script' must be present in the list of args")
    except Exception as e:
        error_stack = traceback.format_exc()
        logger.error("Unable to executed Bash File : "+error_stack)
    return False, error_stack




