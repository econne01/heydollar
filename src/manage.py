#!"c:\program files\python27\python.exe"

import sys
sys.path[0:0] = [
  'c:\\users\\eric\\projects\\heydollar\\src',
  'c:\\users\\eric\\projects\\heydollar\\eggs\\south-0.7.6-py2.7.egg',
  'c:\\users\\eric\\projects\\heydollar\\eggs\\djangorecipe-1.5-py2.7.egg',
  'c:\\users\\eric\\projects\\heydollar\\eggs\\django-1.4-py2.7.egg',
  'c:\\users\\eric\\projects\\heydollar\\eggs\\zc.recipe.egg-2.0.0a3-py2.7.egg',
  'c:\\users\\eric\\projects\\heydollar\\eggs\\zc.buildout-2.0.0-py2.7.egg',
  'c:\\users\\eric\\projects\\heydollar\\eggs\\distribute-0.6.35-py2.7.egg',
  'c:\\users\\eric\\projects\\heydollar',
  ]

import djangorecipe.manage

if __name__ == '__main__':
    sys.exit(djangorecipe.manage.main('project.settings.local'))
