#### What's this?
Here are some tools written in Python to monitor BillGates Linux Botnet activity (DDoS commands, update commands, etc).

#### What's BillGates?
Well, that's a Linux botnet I've found in February, 2014. It it splitted in modules usually called **atddd**, **cupsdd**, **cupsddh**, **ksapdd**, **kysapdd**, **sksapdd**, **skysapdd**.

**cupsdd** is the main module which I call "Gates" (because it locks /tmp/gates.lock). It unpacks **cupsddh** ("Bill") module (the last character depends on configuration) to the directory where the **cupsdd** is stored (usually **/etc**), creates `/etc/init.d/DbSecuritySpt` and makes symlinks to it in `/etc/rc[1-5].d/97DbSecuritySpt`, establishes connection to "Gates" CnC server on IP 116.10.189.246. Newer version of "Gates" module also includes Monitor module "moni". It copies itself to **/usr/bin/pojie** and acts as "moni" only if ran as **/usr/bin/pojie**.
"Bill" can perform simple DDoS.

**atddd**, **ksapdd**, **kysapdd**, **sksapdd**, **skysapdd** is an advanced DDoS module which I call "Melinda" (it doesn't have this name and I thought I can give it). It can perform TCP, UDP, ICMP and DNS DDoS with packet forgery.
The only difference between these files is the CnC server IP address.

    atddd = 202.103.178.76
    ksapdd = 121.12.110.96
    kysapdd = 112.90.252.76
    skysapdd = 112.90.22.197
    sksapdd = 112.90.252.79

#### How can I get this botnet?
That's pretty easy, just set your root password to "1" or something and make sure you have openssh running. You'll definitely get it in some time.
It seems like the installation process is performed by an individual and not automatically.

#### How can I delete this botnet from my PC?
Well, I have successfully deleted this botnet by cleaning root crontab file, `/etc/rc.local`, `/etc/init.d/DbSecuritySpt`, `/etc/rc[1-5].d/97DbSecuritySpt`, all the botnet files from **/etc** (they all have SUID bit and some of them have Immunitable bit), `/etc/conf.n`, `/etc/cmd.n`, `/tmp/*.lock` and `/usr/bin/pojie`. But beware, "Bill" module has some code to execute `insmod /usr/lib/xpacket.ko` and write something to `/usr/lib/libamplify.so` so your PC could be easily infected by rootkit (although I haven't seen any).

#### More information
You can read my writeup [in Russian](http://habrahabr.ru/post/213973/) (or [ Google-translated](http://translate.google.com/translate?sl=ru&tl=en&js=y&prev=_t&hl=ru&ie=UTF-8&u=http%3A%2F%2Fhabrahabr.ru%2Fpost%2F213973%2F&edit-text=))
