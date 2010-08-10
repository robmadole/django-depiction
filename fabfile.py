import os

from fabric.api import env, run, put, local, roles

env.hosts     = ['localbase.webfactional.com']
env.roledefs  = {'eggserver': ['localbase.webfactional.com']}
env.user      = 'localbase'

@roles('eggserver')
def deploy():
    local('rm -rf dist/*')
    local('python setup.py sdist')

    dist_files = os.listdir('dist')

    filename = dist_files[0]

    local_filename  = 'dist/%s' % filename
    remote_filename = '/home/localbase/webapps/eggs/%s' % filename

    put(local_filename, remote_filename)
