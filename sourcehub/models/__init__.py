from mongoengine import *

connect('sourcehub')

from .user import User
from .link import Link
from .tag  import Tag
