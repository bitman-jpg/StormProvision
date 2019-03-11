from fabric.api import abort, hide, local, settings, warn, env, run, put, sudo, get, task, runs_once, execute
#from fabric.operations import run, put
from fabric.context_managers import cd, lcd
from fabric.contrib.console import confirm
import os,sys

binDir=os.path.dirname(os.path.abspath(__file__))
baseDir=os.path.dirname(binDir)
confDir=os.path.join(baseDir, 'conf')

env.skip_bad_hosts = True

@task
def zookeeper(env, colo,stormTarball, applicationServices):
    with settings(warn_only=True):
        put("newStorm", "/tmp/", use_sudo=True, mode=0755)
        put(os.path.join(confDir, "zkTemplate.cfg"), "/tmp/", use_sudo=True, mode=0755)
    with cd("/tmp"):
        if applicationServices:
            sudo('./newStorm -e {0} -c {1} -z -v {2} -a {3} -f'.format(env, colo, stormTarball, applicationServices))
        else:
            sudo('./newStorm -e {0} -c {1} -z -v {2} -f'.format(env, colo,stormTarball))
         
@task
def nimbus(env, colo, stormTarball, applicationServices):
    with settings(warn_only=True):
        put("newStorm", "/tmp/", use_sudo=True, mode=0755)
        put(os.path.join(confDir, "nimbusTemplate.yaml"), "/tmp/", use_sudo=True, mode=0755)
    with cd("/tmp"):
        if applicationServices:
            sudo('./newStorm -e {0} -c {1} -m -v {2} -a {3} -f'.format(env, colo, stormTarball, applicationServices))
        else:
            sudo('./newStorm -e {0} -c {1} -m -v {2} -f'.format(env, colo, stormTarball))

@task
def supervisor(env, colo, stormTarball, applicationServices):
    try:
        with settings(warn_only=True):
            put("newStorm", "/tmp/", use_sudo=True, mode=0755)
            put(os.path.join(confDir, "supervisorTemplate.yaml"), "/tmp/", use_sudo=True, mode=0755)
            montageProperties = os.path.join(confDir, "montage.{0}.properties".format(env))
            if(os.path.exists(montageProperties)):
                put(montageProperties,"/tmp", use_sudo=True)
        with cd("/tmp"):
            if applicationServices:
                sudo('./newStorm -e {0} -c {1} -w -v {2} -a {3} -f'.format(env, colo, stormTarball, applicationServices))
            else:
                sudo('./newStorm -e {0} -c {1} -w -v {2} -f'.format(env, colo, stormTarball))
    except SystemExit:
        import traceback
        out=traceback.format_exc()
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        print(FAIL + out + ENDC)

def test(env, colo):
    print(env, colo, os.getcwd())
    print(os.listdir('.'))
    run('id;hostname')

@task
def getRemote(src,dst):
    with settings(warn_only=True):
        basename = os.path.basename(src)
        tmpfile = "/tmp/" + basename
        sudo('cp {src} {tmp};chmod 666 {tmp}'.format(src=src, tmp=tmpfile))
        get(tmpfile, dst)
        sudo('rm -f /tmp/{0}'.format(basename))

@task
def sudo_check():
    with settings(warn_only=True):
        result = sudo('whoami')
        if result == "root":
            return True
        else:
            return False

@task
@runs_once
def can_sudo():
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    results = execute(sudo_check)
    rc = 0
    for k,v in results.iteritems():
        if not v:
            print FAIL + "CAUTION: " + env.user + " CANNOT sudo to root in " + k + "\n" + ENDC
            rc = 1
    sys.exit(rc)
