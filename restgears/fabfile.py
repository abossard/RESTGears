from fabric.api import local

#from http://www.allbuttonspressed.com/projects/djangoappengine#installation

def hello():
    print("Hello world!")

def make_gae_ready():
    curl('http://bitbucket.org/wkornewald/django-nonrel/get/tip.zip')
    local('mv wkornewald-django-nonrel-*/django .')
    local('rm -rf wkornewald-django-nonrel-*')
    
    curl('http://bitbucket.org/wkornewald/djangoappengine/get/tip.zip')
    local('mv wkornewald-djangoappengine-* djangoappengine')
    #local('rm djangoappengine.zip')
    
    curl('http://bitbucket.org/wkornewald/djangotoolbox/get/tip.zip')
    local('mv wkornewald-djangotoolbox-*/djangotoolbox .')
    local('rm -rf wkornewald-djangotoolbox-*')

    curl('http://bitbucket.org/twanschik/django-autoload/get/tip.zip')
    local('mv twanschik-django-autoload-*/autoload .')
    local('rm -rf twanschik-django-autoload-*')
    
    curl('http://bitbucket.org/wkornewald/django-dbindexer/get/tip.zip')
    local('mv wkornewald-django-dbindexer-*/dbindexer .')
    local('rm -rf wkornewald-django-dbindexer-*')

    curl('http://bitbucket.org/wkornewald/django-testapp/get/tip.zip')
    local('mv wkornewald-django-testapp-* testapp')

    local('pip install --install-option="--prefix=$PWD" django-piston')
    local('mv lib/python2.6/site-packages/piston .')
    local('rm -rf lib')

def curl(url=None):
    filename = ''.join(url.split('/')[-1:])
    local('curl -L -O %s' % (url, ))
    local('unzip tip.zip')
    local('rm tip.zip')

def clean_gae():
    local('rm -rf django')
    local('rm -rf djangoappengine')
    local('rm -rf djangotoolbox')
    local('rm -rf autoload')
    local('rm -rf dbindexer')
    local('rm -rf testapp')
    local('rm -rf piston')
