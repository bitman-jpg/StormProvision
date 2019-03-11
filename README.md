One-click Storm Cluster Provision

Let's say you want a storm cluster with 3 zookeepers, 50 workers, 1 master(of course it's one) in QA in LVS data center. just two steps:

    1. edit conf/openrc.sh ( Automated capacity addition Storm )
    2. newVM -e qa -c lvs -z 3 -w 50 -m 1 --rc ../conf/openrc.sh

Follow instructions and everythin is done! Check storm UI, you're ready to deploy your topologies.

what if you want storm 1.0?

    newVM -e qa -c lvs -z 3 -w 50 -m 1 -v apache-storm-1.0.1.tar.gz

By default the serers are xlarge, if you prefer other flavors, you just tell it.

    newVM -e qa -c lvs -z 3 -w 50 -m 1 --flavor small

If you're not sure what flavors are available in your environment, query it:

    newVM --flavor list

Not sure what images are available? List it:

    newVM --image list

By default the image is emi-ubuntu-12.04.2-server-amd64(you may use image ID because of C3 bug recently), you can change it.say:

     newVM -e qa -c lvs -z 3 -w 50 -m 1 --image emi-centos-6.4-initrd-2.6.32-358.el6.x86_64-new --rc /PATH/TO/YOUR/CREDENTIAL

check newVM usage:

    newVM --help
    Usage: 
         newVM -c COLO -e COS -m NUM -w NUM -z NUM --rc OPENRC [-p HOST] [--flavor FLAVOR] [--image IMAGE] [-v stormTarball] [--appsvc applicationService]
         newVM -c COLO -e COS -m HOST -w NUM --rc OPENRC [--flavor FLAVOR] [--image IMAGE] [-v stormTarball] [--appsvc applicationService]
         newVM --flavor list --rc OPENRC
         newVM --image  list --rc OPENRC
    
    This is used to create new VMs in OpenStack
    
         -c         COLO is slc, phx or lvs, it's used for colo-specific configuration
         -e         environment: prod, pre_prod, qa, dev
         -m         number of nimbus host,or nimbus host to which we add capacity
         -w         number of supervisor host
         -z         number of zookeeper host
         -p         nimbus host from whose supervisor we copy montage.{COS}.property, if a host is passed to -m or conf/montage.{COS}.property exists(deleted after use), we use it.
         --flavor   size of VM,e.g. tiny, small, medium, large, xlarge(by default), etc. (see newVM --flavor list)
         --image    image names or ID(preferred, because of possiblly duplicate names), (see newVM --image list), emi-ubuntu-12.04.2-server-amd64 by default
         --rc       credentials for C3 Service 
         --appsvc   comman-seperated list of ApplicationServcie resourceID for provisioned boxes
         -v         storm tarball name in cronus srepo, check http://cronus-srepo.vip.ebay.com/packages/mp/montageapi/storm/static_content/ebay/montage/
    Example:
         * create a cluster with 1 nimbus, 1 supervisor and 1 zookeeper with credentials in ../conf/openrc.sh, don't create montage property files
         newVM -c lvs -e qa -m 1 -w 1 -z 1 --rc ../conf/openrc.sh
    
         * list available flavor
         newVM --flavor list --rc ../conf/openrc.sh
    
         * create storm 1.0 cluster in production with xlarge 3 nimbus, 20 supervisors and 3 zookeepers, using default image
         newVM -c lvs -e prod -m 3 -w 20 -z 3 --flavor xlarge -v apache-storm-1.0.0.tar.gz --rc /PATH/TO/YOUR/CREDENTIAL --appsvc test:ENVasdajlfd,app2:ENVlkhajdla
    
         * add 3 more supervisors to a storm 1.0.1 cluster whose Nimbus is montage-nimbus4-1147776.stratus.lvs.ebay.com
         newVM -c lvs -e prod -m montage-nimbus4-1147776.stratus.lvs.ebay.com -w 3 -v apache-storm-1.0.1.tar.gz --rc ../conf/openrc.sh
    
         * create only 2 xlarge emi-centos-6.5-x86_64 supervisors with your own credentials
         newVM -c lvs -e qa -w 2 --image emi-centos-6.5-x86_64 --rc /PATH/TO/YOUR/CREDENTIAL 
       
     
Troubleshooting

Q: If I got erros when setting up a single node, what do I do?
A: there must be something wrong in newStorm, get the root cause and then login to the server, go to /tmp/, run newStorm again. for example,
     
    [montage-storm-zk1-7554.phx01.dev.ebayc3.com] out: ======================================================== 
    [montage-storm-zk1-7554.phx01.dev.ebayc3.com] out: ++++ Installing zookeeper config 
    [montage-storm-zk1-7554.phx01.dev.ebayc3.com] out: ======================================================== 
    [montage-storm-zk1-7554.phx01.dev.ebayc3.com] out: tar: This does not look like a tar archive 
    [montage-storm-zk1-7554.phx01.dev.ebayc3.com] out: tar: Exiting with failure status due to previous errors 
    [montage-storm-zk1-7554.phx01.dev.ebayc3.com] out: cp: cannot create regular file `/etc/zookeeper/conf/zoo.cfg’: No such file or directory 
    [montage-storm-zk1-7554.phx01.dev.ebayc3.com] out: grep: /etc/zookeeper/conf/zoo.cfg: No such file or directory

 because I forget to set up phx colo in cronus-srepo, that is, http://cronus-srepo.vip.ebay.com/packages/mp/montageapi/storm/static_content/ebay/montage/conf.colo/phx/zookeeper.tar is missing. after I put it in place, I rerun newStorm in montage-storm-zk1-7554.phx01.dev.ebayc3.com.
    
      #./newStorm  -e qa -c phx -z
                ========================================================
                ++++   Provisioning a zookeeper node in phx
                ========================================================
                ========================================================
                ++++   Java is already installed, validating its version
                ========================================================
                Java version is correct, skipping Java installation
                ========================================================
                ++++   checking existence of zookeeper account
                ========================================================
                adduser: The user `zookeeper' already exists.
                ========================================================
                ++++   zookeeper account is created
                ========================================================
    
                ========================================================
                ++++   Installing zookeeper binary
                ========================================================
                ========================================================
                ++++   zookeeper binary installed
                ========================================================
                ========================================================
                ++++   Installing supervisorD daemon
                ========================================================
                Reading package lists... Done
                Building dependency tree       
                Reading state information... Done
                supervisor is already the newest version.
                0 upgraded, 0 newly installed, 0 to remove and 109 not upgraded.
                ========================================================
                ++++   SupervisorD Configuration Done
                ========================================================
                ========================================================
                ++++   Configuring zookeeper
                ========================================================
                ========================================================
                ++++   Installing zookeeper config
                ========================================================
                ========================================================
                ++++   myid of zookeeper is set in /var/lib/zookeeper/myid
                ========================================================
                ========================================================
                ++++   zookeeper config Installed
                ========================================================
                ========================================================
                ++++   Starting zookeeper
                ========================================================
                Stopping supervisor: supervisord.
                Starting supervisor: supervisord.
                zookeeper      RUNNING    pid 3104, uptime 0:00:03
