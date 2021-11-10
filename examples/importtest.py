"""
Simple script to verify that imports work during development. This can be an issue when you try to import in a folder structure
and continually encounter "ModuleNotFound" errors.

Solution is based on: https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944

Summary:
- Use virtual environment
- create folder structure per this project (name folder where source code is the same as the project for ease in distribution later on)
- activate virtual environment
- run this test (it should get the module not found error)
- "python -m pip install -e ." to install the package
- run this test again (it should succeed)
"""

from goopy_ibcp.endpoints import Endpoints

print(Endpoints.AuthenticationStatus)