Заходим в Shell
    python manage.py shell

Импортирую все модели
from news.models import *

1). Создать двух пользователей (с помощью метода User.objects.create_user
('username')).
    u1 = User.objects.create_user(username="Bob Djager")
    u2 = User.objects.create_user(username="Tom Hancks")

2). Создать два объекта модели Author, связанные с пользователями.
    a1 = Author.objects.create(author_user=u1)
    a2 = Author.objects.create(author_user=u2)

3). Добавить 4 категории в модель Category.
    c1 = Category.objects.create(category_name='Story')     История   Story
    c2 = Category.objects.create(category_name='Culture')   Культура  Culture
    c3 = Category.objects.create(category_name='Society')   Общество  Society
    c4 = Category.objects.create(category_name='Health')    Здоровье  Health
                c1.category_name

4). Добавить 2 статьи и 1 новость.
     p1 = Post.objects.create(post_author=a1, category_type='NW',
        post_title='Мариинский театр', post_text='Мариинский театр завершил
        строительство своей «вагнерианы», представив комическую оперу
        композитора. Длинный, назидательный опус немецкого гения сумели подать
        ярко и музыкально безупречно.')

     p2 = Post.objects.create(post_author=a2, post_title='Исторические сведения
        о здоровье', post_text='Основа гимнастических упражнений
        «Русской здравы» – это способы укрепления организма, необходимые для
        развития качеств хорошего воина. В те времена, когда каждый мужчина
        должен был обладать способностью в любой момент превратиться из мирного
        пахаря в грозного защитника своего дома и семьи, это было более чем
        оправданно. Поэтому воинские практики использовались уже в воспитании
        детей, что укрепляло не только тело ребенка, но и его дух.')

      p3 = Post.objects.create(post_author=a2, post_title='Покорители морей',
        post_text='Первое русское кругосветное плавание началось 7 августа 1803
        года — ровно 220 лет назад. Небольшие корабли "Нева" и "Надежда" вышли
        из Кронштадта, а вернулись через три года и 12 дней. Сегодня
        путешественники по-прежнему стремятся обогнуть Землю — на самолетах,
        лодках, мотоциклах, даже велосипедах. Какие поездки официально
        считаются кругосветками, сколько стоит такой тур и в чем его
        сложность — в материале РИА Новости.')

                p1.post_title
                    'Мариинский театр'
                Post.objects.get(id=1).post_title

5). Присвоить им категории (как минимум в одной статье/новости должно быть не
меньше 2 категорий).

      Post.objects.get(id=1).post_category.add(Category.objects.get(id=2))
      Post.objects.get(id=1).post_category.add(Category.objects.get(id=3))
      Post.objects.get(id=2).post_category.add(Category.objects.get(id=4))
      Post.objects.get(id=2).post_category.add(Category.objects.get(id=1))
      Post.objects.get(id=2).post_category.add(Category.objects.get(id=3))
      Post.objects.get(id=3).post_category.add(Category.objects.get(id=1))
      Post.objects.get(id=3).post_category.add(Category.objects.get(id=3))

6). Создать как минимум 4 комментария к разным объектам модели Post (в каждом
объекте должен быть как минимум один комментарий).
      Comment.objects.create(comment_post=Post.objects.get(id=1),
      comment_user=Author.objects.get(id=1).author_user,
      comment_text='хорошая новость')

      Comment.objects.create(comment_post=Post.objects.get(id=1),
      comment_user=Author.objects.get(id=1).author_user,
      comment_text='Новость нравится')

      Comment.objects.create(comment_post=p2,
      comment_user=Author.objects.get(id=2).author_user,
      comment_text='Статья мне нравится')

      Comment.objects.create(comment_post=p3,
      comment_user=Author.objects.get(id=2).author_user,
      comment_text='Статья интересная')

      Comment.objects.create(comment_post=p3,
      comment_user=Author.objects.get(id=1).author_user,
      comment_text='Супер')

7). Применяя функции like() и dislike() к статьям/новостям и комментариям,
скорректировать рейтинги этих объектов.

      p1.like()
      Comment.objects.get(id=2).like()
      Comment.objects.get(id=2).dislike()
      Post.objects.get(id=3).like()
      Post.objects.get(id=1).dislike()
            Post.objects.get(id=1).post_rating


8). Обновить рейтинги пользователей.

      s = Author.objects.get(id=2)
      s.update_rating()
      s.author_rating

            a1.update_rating()
            a1.rating

9). Вывести username и рейтинг лучшего пользователя (применяя сортировку и
возвращая поля первого объекта).

      s = Author.objects.order_by('-author_rating')[:1]
           for i in s:
           i.author_user.username
           i.author_rating

           'Tom Hancks'
           38

10). Вывести дату добавления, username автора, рейтинг, заголовок и превью
лучшей статьи, основываясь на лайках/дислайках к этой статье.

      p = Post.objects.order_by('-post_rating')[:1]
      for i in p:
           i.post_date
           i.post_author.author_user.username
           i.post_rating
           i.post_title
           i.preview()

    datetime.datetime(2023, 9, 3, 10, 45, 2, 489674,
    tzinfo=datetime.timezone.utc)
    'Tom Hancks'
    8
    'Покорители морей'
    'Первое русское кругосветное плавание началось 7 августа 1803 года — ровно
    220 лет назад. Небольшие корабли "Нева" и "Надежда"...'

11). Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой
статье.

       Post.objects.all().order_by('-post_rating')[0].comment_set.values
       ('comment_date', 'comment_user', 'comment_rating', 'comment_text')

        <QuerySet [{'comment_date':
        datetime.datetime(2023, 9, 3, 12, 17, 53, 271910,
        tzinfo=datetime.timezone.utc),
        'comment_user': 2,
        'comment_rating': 5,
        'comment_text': 'Статья интересная'},
        {'comment_date':
        datetime.datetime(2023, 9, 3, 12, 20, 26, 399956,
        tzinfo=datetime.timezone.utc),
        'comment_user': 1,
        'comment_rating': 2,
        'comment_text': 'Супер'}]>
