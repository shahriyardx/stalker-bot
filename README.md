# Stalker bot
A bot that will notify you whenever your target changes their status

# Commands
#### Server config
..settz <timezone> -> Set your servers timezone. \
Example : `..settz Asia/Dhaka`

..prefix <new_prefix> -> Change server's prefix for this bot \
Example : `..prefix ?`


#### Adding deleting and updating monitor`
..monitor <target> <channel> -> Monitors a *Target* and send message on their status change \
Example : `..monitor @Shahriyar #logs-channel`

..delete <target> -> Delete a monitor if they are monitored. \
Example : `..delete @Shahriyar`

..update <target> <channel> -> Change log channel for that specific target \
Example : `..update @Shahriyar #different-log-channel`

