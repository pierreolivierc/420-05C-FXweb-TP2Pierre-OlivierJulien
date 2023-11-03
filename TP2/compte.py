import datetime
import os

from babel import dates
from flask import Blueprint, abort, render_template, redirect, url_for, request, session
import re

import app
import bd

bp_compte = Blueprint('compte', __name__)

