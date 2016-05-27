
RPI=192.168.7.143

ping: hosts ansible-install-stamp ssh-configure-stamp
	ansible all -i hosts -m ping -u pi

hosts: Makefile
	echo "${RPI}" > $@

ssh-configure-stamp:
	test -s "$$HOME/.ssh/id_rsa.pub" || ssh-keygen -t rsa
	ssh-copy-id "pi@${RPI}"
	touch $@

razberry-install:
	wget -q -O $@ http://razberry.z-wave.me/install

ansible-install-stamp:
	sudo apt-get install ansible
	touch $@

clean:
	rm hosts razberry-install *-stamp

.PHONY: clean

