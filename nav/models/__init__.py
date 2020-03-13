from mongoengine import *

connect('nav')

from .user import User
from .link import Link
from .tag  import Tag
