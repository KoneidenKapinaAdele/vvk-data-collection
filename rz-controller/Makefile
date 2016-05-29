
RPI=192.168.7.127

razberry-update-stamp: site.yml razberry-install hosts \
		roles/razberry/handlers/main.yml roles/razberry/tasks/main.yml \
		ansible-install-stamp ssh-configure-stamp
	ansible-playbook -i hosts $<
	touch $@

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
	grep -q jessie-backports /etc/apt/sources.list
	sudo apt-get -t jessie-backports install ansible
	touch $@

clean:
	rm hosts razberry-install *-stamp

.PHONY: clean

