""" Environment Variables List
These variables are used for information that should not be part of the repository (i.e: Account stuff)
Note: These can be set as follows:
    - Volatile in CLI (via "set VARNAME VALUE") => Will not be available to other CLI or after that CLI closes
    - Persistent (via "setx VARNAME VALUE") => Will be available to other CLI and after CLI closes. These will also
      show up in the environment view (i.e: Windows).
    NOTE: Window may need to be closed and then re-opened for updated values to take place so it is recommended to
    make sure these are set prior to starting the system
"""


class Environment_Var:
    # Account which is used to place orders, read trades, etc.
    IB_ACTIVE_ACCOUNT: str = "IB_ACTIVE_ACCOUNT"
