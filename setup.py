import os
from distutils.core import setup

doc_dir = os.path.join(os.path.dirname(__file__), 'docs')
long_desc_file = os.path.join(doc_dir, 'overview.rst')
version_num = __import__('rbac').__version__ 

setup(
    name='django-rbac',
    version=version_num,
    description='Role-based Access Control (RBAC) implementation for management of permissions in Django.',
    long_description=open(long_desc_file).read(),
    author='Hector Garcia',
    author_email='hector@nomadblue.com',
    url='http://nomadblue.com/projects/django-rbac/',
    download_url='http://bitbucket.org/nabucosound/django-rbac/downloads/django-rbac-%s.tar.gz' % version_num,
    packages=['rbac', 'rbac.templatetags', 'example', 'example.myapp'],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Framework :: Django',
    ]
)
