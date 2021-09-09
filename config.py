extensions = [
    "cogs.stalker.config",
    "cogs.settings",
    "cogs.stalker",
    "utils.events",
    "utils.errorhandler",
]

db_config = {
    "user": "postgres",
    "password": "root",
    "database": "stalker",
    "host": "localhost",
}


default_prefix = ".."
mode = "development"  # development > Will auto reload cog whenever they get editted.
