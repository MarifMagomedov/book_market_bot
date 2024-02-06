from sqlalchemy import select, update, delete
from database.models import (session_factory, Base, UserModel, GoodsModel,
                             ShoppingCartModel, OrdersModel, engine)


class Database:
    @staticmethod
    def start_db() -> None:
        Base.metadata.create_all(engine)

    @staticmethod
    def check_user_in_base(user_id: int) -> bool:
        with session_factory() as session:
            select_user_query = select(1).where(UserModel.user_id == user_id)
            result = session.execute(select_user_query).scalar()
        return result

    @staticmethod
    def select_user(user_id: int) -> tuple:
        with session_factory() as session:
            query = select(UserModel).where(UserModel.user_id == user_id).select_from(UserModel)
            user = session.execute(query).scalar()
            return user.name, user.surname, user.email, 0, 0

    @staticmethod
    def create_profile(user_id: int, name: str, surname: str, email: str) -> None:
        with session_factory() as session:
            user = UserModel(
                user_id=user_id,
                name=name,
                surname=surname,
                email=email
            )
            session.add(user)
            session.flush()
            session.commit()

    @staticmethod
    def update_user_profile(user_id: int, edit_param: str, edit_value: str) -> None:
        with session_factory() as session:
            query = update(
                UserModel
            ).where(
                UserModel.user_id == user_id
            ).values(
                {edit_param: edit_value}
            )
            session.execute(query)
            session.commit()

    @staticmethod
    def get_goods_categories() -> list[str]:
        with session_factory() as session:
            query = select(
                GoodsModel.category
            ).group_by(
                GoodsModel.category
            ).where(
                GoodsModel.value != 0
            ).select_from(
                GoodsModel
            )
            res = session.execute(query).scalars().all()
            return res

    @staticmethod
    def get_goods_titles(category: str) -> list[tuple[str, str]]:
        with session_factory() as session:
            query = select(
                GoodsModel.title,
                GoodsModel.good_id
            ).where(
                GoodsModel.category == category
            ).select_from(
                GoodsModel
            )
            res = session.execute(query).all()
            return res

    @staticmethod
    def get_good_info(good_id: int) -> tuple:
        with session_factory() as session:
            query = select(
                GoodsModel.title,
                GoodsModel.author,
                GoodsModel.category,
                GoodsModel.description,
                GoodsModel.price,
                GoodsModel.value
            ).where(
                GoodsModel.good_id == good_id
            ).select_from(
                GoodsModel
            )
            res = session.execute(query).all()
            return res[0]
        
    @staticmethod
    def get_user_cart(user_id: int) -> list[ShoppingCartModel]:
        with session_factory() as session:
            user = session.get(UserModel, user_id)
            return user.cart
            
    
    @staticmethod
    def update_user_cart(
        user_id: int, 
        good_id: str, 
        put_value: int, 
        good_title: str,
        total_sum: int
    ) -> None:
        with session_factory() as session:
            user = session.get(UserModel, user_id)
            item = ShoppingCartModel(
                good_id=good_id, 
                good_value=put_value, 
                good_title=good_title,
                total_sum=total_sum
            )
            user.cart.append(item)
            session.refresh(user)
            session.commit()
    
    @staticmethod
    def update_goods_value(good_id: int, update_good_value: int) -> None:
        with session_factory() as session:
            good = session.get(GoodsModel, good_id)
            good.value = good.value - update_good_value
            session.refresh(good)
            session.commit()
            
    @staticmethod
    def delete_user_cart_item(cart_id) -> None:
        with session_factory() as session:
            query = delete(
                ShoppingCartModel
            ).where(
                ShoppingCartModel.cart_id == cart_id
            )
            session.execute(query)
            session.commit()
    















# def zxc():
#     db = Database()
#     db.start_db()
#     with session_factory() as session:
#         goods = [
#             GoodsModel(category='Программирование', title='Грокаем алгоритмы', author='Адитья Бхаргава', description='Алгоритмы - это всего лишь пошаговые алгоритмы решения задач, и большинство таких задач уже были кем-то решены, протестированы и проверены. Можно, конечно, погрузиться в глубокую философию гениального Кнута, изучить многостраничные фолианты с доказательствами и обоснованиями, но хотите ли вы тратить на это свое время? Оrкройте великолепно иллюстрированную книrу, и вы сразу поймете, что алгоритмы - это просто. А грокать алгоритмы - это веселое и увлекательное занятие.', price=799, value=15),
#             GoodsModel(category='Сказки', title='Синяя птица', author='Морис Метерлинк', description='В 1905 году бельгийский писатель и драматург Морис Метерлинк написал пьесу в шести актах «Синяя птица», посвящённую вечному поиску человеком символа счастья и познания бытия – Синей птицы. Позже гражданская жена писателя, французская актриса Жоржетта Леблан переделала пьесу в сказку для детей в 10 главах.', price=500, value=2),
#             GoodsModel(category='Программирование', author='Чарльз Петцольд', title='КОД: Тайный язык информатики', description='Научно-популярная книга американского программиста Чарльза Петцольда, в которой рассказывается, как персональные компьютеры работают на аппаратном и программном уровне. В предисловии к изданию Петцольд написал, что его цель состояла в том, чтобы читатели поняли, как работают компьютеры на конкретном уровне, который «мог бы даже соперничать с уровнем инженеров-электриков и программистов».', price=1500, value=123),
#             GoodsModel(category='Саморазвитие', title='Атрибут власти', author='Анвар Бакиров', description='НЛП – это новаторское, предельно рациональное направление в психологии, помогающее найти кратчайший ответ на ключевой вопрос: как получить максимум, затратив минимум ресурсов и времени?Из этой книги вы узнаете, как вызывать доверие с первого взгляда, управлять своими и чужими эмоциями, извлекать выгоду даже из поражений и т.д', price=3500, value=11),
#             GoodsModel(category='Программирование', title='От джуна до сеньора', description='Владимир Швец имеет 15-летний опыт коммерческой разработки;работал почти на всех должностях корпоративной лестницы — от тестировщика до ведущего архитектора.• В книге освещены все самые актуальные проблемы в сфере разработки: полезные практики по работе с кодом, выстраивание коммуникаций в коллективе, личный рост, борьба с выгоранием, сомнениями и страхами.• К каждой теме добавлены задания и истории из жизни.Быть разработчиком — трудно, а делать первые шаги — еще труднее.', price=509, value=53),
#             GoodsModel(category='Любовные романы', author='Натализа Кофф', title='Мой реванш', description='У Ермака — служба, а в перспективе планы на частный бизнес. Хмурый, серьезный, упрямый, гораздо старше «золотой» избалованной девочки по имени Даша. Они никогда не должны были встретиться, но именно Дарья, после увольнения, стала первым частным заказом Ермакова', price=899, value=0),
#             GoodsModel(category='Фэнтези', title='Опасная игра', author='Ляна Зелинская', description='zxczxzxz', price=122, value=1),
#             GoodsModel(category='Классика', title='Тарас Бульба', author='Николай Гоголь', description='События произведения происходят в среде запорожских казаков в первой половине XVII века[1]. В основу повести Н. В. Гоголя легла история казацкого восстания 1637—1638 годов, подавленного гетманом Николаем Потоцким. ', price=699, value=1000),
#             GoodsModel(category='Классика', title='Тихий Дон', author='Михаил Шолохов', description='«Ти́хий Дон» — роман-эпопея в четырёх томах, написанный Михаилом Шолоховым (1905-1984). Тома 1—3-й написаны с 1925 по 1932 год, опубликованы в журнале «Октябрь» в 1928—1932 годах. Том 4-й был написан в 1932 году, закончен в 1940 году, опубликован в журнале «Новый мир» в 1937—1940 годах[1].Одно из наиболее значимых произведений русской литературы XX века, рисующее широкую панораму жизни донского казачества во время Первой мировой войны, революционных событий 1917 года и Гражданской войны в России.', price=1229, value=876),
#             GoodsModel(category='Классика', title='Дубровский', author='А.С.Пушкин', description='Наиболее известный разбойничий роман на русском языке, необработанное для печати произведение А. С. Пушкина. Повествует о любви Владимира Дубровского к Марии Троекуровой - потомков двух враждующих помещичьих семейств.', price=999, value=783)
#         ]
#     for i in goods:
#         session.add(i)
#         session.flush()
#         session.commit()


