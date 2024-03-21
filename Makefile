unload:
	@launchctl unload ~/Library/LaunchAgents/com.user.vpn_check.plist

load:
	@launchctl load ~/Library/LaunchAgents/com.user.vpn_check.plist

install:
	@cp com.user.vpn_check.plist ~/Library/LaunchAgents
	@make load

show/err:
	@cat /tmp/com.user.vpn_check.err

show/out:
	@cat /tmp/com.user.vpn_check.err