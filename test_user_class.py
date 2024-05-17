import pytest
from unittest.mock import patch, MagicMock
from base import *

sample_users = {
  "janesmth": {
    "name": "Jane Smith",
    "email": "janesmith33@gmail.com",
    "password": "gAAAAABmRQt-mpYi3gUPY4EhHNj22K2WXhsdzVYnyaDTc2qf_LXuaijIGs7rJb1y0a-Cvxevv3GZMJH3CeqdIudlb3YkgBRcmQ==",
    "is_active": True,
    "leading": [
      "newProject"
    ],
    "involved": []
  },
  "alexb": {
    "name": "Alex Brown",
    "email": "alexb@gmail.com",
    "password": "gAAAAABmRlagHX_qJr_uwOnsUUfbt1cqSpW7zDXSIwwfvinj9Ivi9ZRIjRXRWwF-EKrhMCFJ6qnu3fkZosGnaSsqbOljEd7VmQ==",
    "is_active": True,
    "involved": [
      "newProject"
    ],
    "leading": []
  }
}