from .BaseModel import Model


class GuildData(Model):
    TABLE = "guild_data"
    SCHEMA = f"""
        CREATE TABLE IF NOT EXISTS {TABLE}(
            id BIGSERIAL PRIMARY KEY NOT NULL,
            guild_id BIGINT NOT NULL UNIQUE,
            prefix VARCHAR(20) NOT NULL,
            timezone VARCHAR(20) NULL
    )"""

    INDEXES = [f"CREATE INDEX ON {TABLE}(guild_id)"]

    async def _get_prefix(self, guild_id):
        async with self.database.acquire() as con:
            data = await con.fetchrow(
                f"SELECT * FROM {self.TABLE} WHERE guild_id=$1", guild_id
            )

        return data

    async def get_prefix(self, guild_id):
        data = await self._get_prefix(guild_id)
        if not data:
            from config import default_prefix

            await self.insert(guild_id=guild_id, prefix=default_prefix)
            data = await self._get_prefix(guild_id)

        return data


class User(Model):
    TABLE = "users"
    SCHEMA = f"""
        CREATE TABLE IF NOT EXISTS {TABLE}(
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL,
            mentor_id BIGINT NOT NULL,
            channel_id BIGINT NOT NULL,
            guild_id BIGINT NOT NULL REFERENCES guild_data (guild_id) ON DELETE CASCADE
    )"""

    INDEXES = [f"CREATE INDEX ON {TABLE}(user_id, guild_id)"]

    async def get_guild_monitors(self, guild_id):
        async with self.database.acquire() as con:
            data = await con.fetch(
                f"SELECT * FROM {self.TABLE} WHERE guild_id=$1", guild_id
            )

        return data

    async def get_user_monitors(self, mentor_id):
        async with self.database.acquire() as con:
            data = await con.fetch(
                f"SELECT * FROM {self.TABLE} WHERE mentor_id=$1", mentor_id
            )

        return data


class Log(Model):
    TABLE = "logs"
    SCHEMA = f"""
        CREATE TABLE IF NOT EXISTS {TABLE}(
            id BIGSERIAL PRIMARY KEY NOT NULL,
            user_id BIGINT NOT NULL,
            status VARCHAR(10) NOT NULL,
            started TIMESTAMPTZ NOT NULL,
            ended TIMESTAMPTZ NULL,
            guild_id BIGINT NOT NULL REFERENCES guild_data (guild_id) ON DELETE CASCADE
    )"""

    INDEXES = [f"CREATE INDEX ON {TABLE}(user_id, status, started, ended)"]

    async def get_last_log(self, user_id, guild_id):
        async with self.database.acquire() as con:
            data = await con.fetchrow(
                f"SELECT * FROM {self.TABLE} WHERE user_id=$1 AND guild_id=$2 AND ended IS NULL",
                user_id,
                guild_id,
            )

        return data

    async def get_null_logs(self):
        async with self.database.acquire() as con:
            data = await con.fetch(f"SELECT * FROM {self.TABLE} WHERE ended IS NULL")

        return data

    async def get_data_range(self, start, end, status="all"):
        async with self.database.acquire() as con:
            if status == "all":
                data = await con.fetch(
                    "SELECT * FROM logs WHERE started >= $1 AND ended <= $2", start, end
                )
            else:
                data = await con.fetch(
                    "SELECT * FROM logs WHERE started BETWEEN $1 AND $2 AND ended <= $2",
                    start,
                    end,
                    status,
                )

        return data
