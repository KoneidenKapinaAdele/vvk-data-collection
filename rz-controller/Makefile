
razberry-install:
	wget -q -O $@ http://razberry.z-wave.me/install

ansible-install-stamp:
	sudo apt-get install ansible
	touch $@

clean:
	rm razberry-install *-stamp

.PHONY: clean

