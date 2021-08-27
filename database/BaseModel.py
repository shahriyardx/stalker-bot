class ModelMixin:
    TABLE: str
    SCHEMA: str
    INDEXES: list

    def __init__(self, database) -> None:
        self.database = database

    async def fetchrow(self, query, *data):
        async with self.database.acquire() as con:
            data = await con.fetchrow(query, *data)

        return data

    async def fetch(self, query, *data):
        async with self.database.acquire() as con:
            data = await con.fetch(query, *data)

        return data

    async def execute(self, query, *data):
        async with self.database.acquire() as con:
            await con.execute(query, *data)

    async def _create(self):
        async with self.database.acquire() as con:
            await con.execute(self.SCHEMA)

            for index in self.INDEXES:
                await con.execute(index)


class Model(ModelMixin):
    async def get(self, multi=False, **kwargs):
        wheres = []
        wheres_schema = "WHERE "

        if kwargs:
            for idx, arg in enumerate(kwargs.items()):
                wheres += [[idx + 1, arg]]

            for where in wheres:
                wheres_schema += f"{where[1][0]}=${where[0]}"
                if where[0] < len(wheres):
                    wheres_schema += " AND "

            schema = f"SELECT * FROM {self.TABLE} {wheres_schema}"
            if multi:
                data = await self.fetch(schema, *kwargs.values())
            else:
                data = await self.fetchrow(schema, *kwargs.values())
            return data

        return None

    async def delete(self, **kwargs):
        wheres = []
        wheres_schema = "WHERE "

        if kwargs:
            for idx, arg in enumerate(kwargs.items()):
                wheres += [[idx + 1, arg]]

            for where in wheres:
                wheres_schema += f"{where[1][0]}=${where[0]}"
                if where[0] < len(wheres):
                    wheres_schema += " AND "

            schema = f"DELETE FROM {self.TABLE} {wheres_schema}"
            await self.execute(schema, *kwargs.values())

    async def all(self, limit=None, order_field=None, order="ASC"):
        limit_text = ""
        order_text = ""

        if limit:
            limit_text = f"LIMIT {limit}"

        if order_field:
            order_text = f"ORDER BY {order_field} {order}"

        schema = f"SELECT * FROM {self.TABLE} {order_text} {limit_text}"

        data = await self.fetch(schema)
        return data

    async def insert(self, **kwargs):
        intos = ", ".join([x for x in kwargs.keys()])
        values = ", ".join([f"${idx + 1}" for idx, _ in enumerate(kwargs)])

        schema = f"INSERT INTO {self.TABLE}({intos}) VALUES({values})"
        await self.execute(schema, *kwargs.values())

    async def update(self, query, **kwargs):
        schema = f"UPDATE {self.TABLE} SET "

        updates = []
        finds = []
        args = [*kwargs.values()]

        last_index = 1
        for idx, val in enumerate(kwargs.keys()):
            updates.append(f"{val}=${idx + 1}")
            last_index += 1

        for key, val in query.items():
            finds.append(f"{key}=${last_index}")
            args.append(val)
            last_index += 1

        schema += ", ".join(updates) + " WHERE "
        schema += " AND ".join(finds)

        await self.execute(schema, *args)
