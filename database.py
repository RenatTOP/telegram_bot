import sqlalchemy as sa
import config


class DBHandler:
    def __init__(self, dialect, user, password, host, dbname, port='5432'):
        try:
            connection_string = dialect + "://" + user + ":" + password \
                + "@" + host + ":" + port + "/" + dbname
            print(connection_string)
            self.__conn = sa.create_engine(connection_string)
            self.__meta = sa.MetaData()
            # create internal tables here sql
        except Exception as e:
            print(e)

    def create_internal_tables(self):
        try:
            sa.Table(config.tables_names['USERS_TABLE'], self.__meta,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('first_name', sa.String(30)))

            sa.Table(config.tables_names['PRODUCTS_TABLE'], self.__meta,
                     sa.Column('product_id', sa.String(35), primary_key=True),
                     sa.Column('label', sa.String(50)),
                     sa.Column('amount', sa.Integer),
                     sa.Column('about', sa.String(1024)),
                     sa.Column('picture_url', sa.String(1024)))
            self.__meta.create_all(self.__conn)
        except Exception as ex:
            print(ex)

    def add_user(self, chat_id, first_name):
        try:
            sa.Table('cart_renat_{}'.format(chat_id), self.__meta,
                     sa.Column('product_id', sa.String(35), primary_key=True),
                     sa.Column('number', sa.Integer))
            self.__meta.create_all(self.__conn)
            table = self.__meta.tables[config.tables_names['USERS_TABLE']]
            self.__conn.execute(table.insert((chat_id, first_name)))
        except Exception as ex:
            print(ex)

    def add_product(self, label, amount, about, picture):
        self.__meta.reflect(bind=self.__conn)
        table = self.__meta.tables[config.tables_names['PRODUCTS_TABLE']]
        stmt = sa.select(
            [sa.text("1")]
        ).where(table.c.label == label, table.c.amount == amount, table.c.about == about, table.c.picture == picture)
        self.__conn.execute(stmt).fetchall()

    def get_products(self, page_size, offset):
        self.__meta.reflect(bind=self.__conn)
        table = self.__meta.tables[config.tables_names['PRODUCTS_TABLE']]
        res = self.__conn.execute(sa.select([table.c.product_id, table.c.label, table.c.amount]).limit(
            page_size).offset(offset)).fetchall()
        return res

    def get_product_by_id(self, product_id):
        self.__meta.reflect(bind=self.__conn)
        table = self.__meta.tables[config.tables_names['PRODUCTS_TABLE']]
        res = self.__conn.execute(

            sa.select([table.c.label, table.c.amount, table.c.about, table.c.picture_url]).where(
                table.c.product_id == product_id)

        ).fetchall()
        return res

    def add_products_to_cart(self, chat_id, product_id):
        self.__meta.reflect(bind=self.__conn)
        table = self.__meta.tables['cart_renat_{}'.format(chat_id)]
        stmt = sa.select(
            [sa.text("1")]
        ).where(table.c.product_id == product_id)

        result = self.__conn.execute(stmt).fetchall()

        if len(result) == 0:
            self.__conn.execute(table.insert((product_id, 1)))
        else:
            stmt = table.update().where(table.c.product_id ==
                                        product_id).values(number=table.c.number+1)
            self.__conn.execute(stmt)

    def get_products_from_cart(self, chat_id):
        self.__meta.reflect(bind=self.__conn)
        table = self.__meta.tables['cart_renat_{}'.format(chat_id)]
        return self.__conn.execute(sa.select([table])).fetchall()

    def clear_the_cart(self, chat_id):
        self.__meta.reflect(bind=self.__conn)
        table = self.__meta.tables['cart_renat_{}'.format(chat_id)]
        return self.__conn.execute(table.delete())
