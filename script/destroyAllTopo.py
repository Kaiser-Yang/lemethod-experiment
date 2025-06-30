#!/usr/bin/env python3

# Usage: python destroyAllTopo.py

from vemu_api import *
from commonConfig import *
import commonConfig

if __name__ == "__main__":
    init(None)
    projectList = commonConfig.projectManager.get_projects()
    for project in projectList:
        commonConfig.projectManager.destroy(project)
        print(f"destroy project {project} successfully.")
