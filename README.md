Tässä firewall.sh skripti linux palvelimella:


//Local and trusted hosts and networks

iptables -P INPUT ACCEPT

iptables -P OUTPUT ACCEPT

iptables -P FORWARD ACCEPT

iptables -F INPUT

iptables -F OUTPUT

iptables -F FORWARD

iptables -F -t nat
iptables -F -t mangle

//Local and trusted hosts and networks

iptables -A INPUT -i lo -j ACCEPT

iptables -A INPUT -s 192.168.0.0/24 -j ACCEPT # example how to allow whole IP n>

iptables -A INPUT -s 193.167.100.97 -j ACCEPT # DO NOT COMMENT OR MODIFY THIS. >


//Completely open services

iptables -A INPUT -p tcp --dport 22 -j ACCEPT # DO NOT COMMENT OR MODIFY THIS. >

iptables -A INPUT -p tcp --dport 80 -j ACCEPT # HTTP

//established traffic inbound (allow return traffic back which was originated f>

iptables -A INPUT -p ALL -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT


