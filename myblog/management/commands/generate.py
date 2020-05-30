from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from myblog.models.comment import Comment
from myblog.models.article import Article
from myblog.models.tag import Tag
from myblog.models.vote import Vote

fake = Faker()


class Command(BaseCommand):
    help = 'Generates fake data for db'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int, default=0)
        parser.add_argument('-t', '--tags', type=int, default=0)
        parser.add_argument('-T', '--max-tags-per-article', type=int, default=0)
        parser.add_argument('-s', '--max-sentences-per-article', type=int, default=15)
        parser.add_argument('-a', '--articles', type=int, default=0)
        parser.add_argument('-S', '--max-sentences-per-comment', type=int, default=8)
        parser.add_argument('-c', '--comments', type=int, default=0)
        parser.add_argument('-A', '--max-votes-per-article', type=int, default=0)
        parser.add_argument('-C', '--max-votes-per-comment', type=int, default=0)

    @staticmethod
    def create_users(users):
        offset_id = User.objects.count() + 1
        User.objects.bulk_create(
            [
                User(
                    first_name=(first_name := fake.first_name()),
                    last_name=(last_name := fake.last_name()),
                    username=(username := f'{first_name}{last_name}{offset_id + i}'),
                    password=make_password(f'{username}password', None, 'md5'),
                    email=f'{username}@example.com',
                )
                for i in range(users)
            ]
        )

    @staticmethod
    def create_tags(tags):
        offset_id = Tag.objects.count() + 1
        Tag.objects.bulk_create(
            [
                Tag(
                    tag=f'{fake.word()}{offset_id + i}'
                )
                for i in range(tags)
            ]
        )

    @staticmethod
    def fast_randint(mn, mx):
        return int(fake.random.random() * (mx - mn + 1)) + mn

    @staticmethod
    def fast_vote(kindness_coefficient=0.5):
        return 1 if fake.random.random() < kindness_coefficient else -1

    @staticmethod
    def create_articles(articles, max_tags_per_article, max_sentences_per_article):
        user_id_max = User.objects.count()
        Article.objects.bulk_create(
            [
                Article(
                    title=fake.sentence(),
                    body=fake.paragraph(nb_sentences=max_sentences_per_article),
                    user_id=Command.fast_randint(1, user_id_max),
                )
                for i in range(articles)
            ]
        )

        through_model = Article.tags.through
        n_articles = Article.objects.count()
        tag_ids = list(Tag.objects.values_list('id', flat=True))  # list for sample()
        through_list = []
        for article_id in range(n_articles - articles + 1, n_articles + 1):
            n_tags = Command.fast_randint(0, max_tags_per_article)
            through_list += [
                through_model(
                    article_id=article_id,
                    tag_id=tag_id,
                )
                for tag_id in fake.random.sample(tag_ids, n_tags)
            ]
        through_model.objects.bulk_create(through_list)

    @staticmethod
    def create_comments(comments, max_sentences_per_comment):
        user_id_max = User.objects.count()
        article_id_max = Article.objects.count()
        Comment.objects.bulk_create(
            [
                Comment(
                    body=fake.paragraph(nb_sentences=max_sentences_per_comment),
                    user_id=Command.fast_randint(1, user_id_max),
                    article_id=Command.fast_randint(1, article_id_max),
                )
                for i in range(comments)
            ]
        )

    @staticmethod
    def generate_votes_for_model(model_cls, max_votes_per_article):
        if max_votes_per_article == 0:
            return

        user_ids = list(User.objects.values_list('id', flat=True))  # list for sample()
        models = model_cls.objects.all()
        model_type_id = ContentType.objects.get_for_model(model_cls).id

        votes = []
        for model in models:
            n_votes = Command.fast_randint(0, max_votes_per_article)
            rating = 0
            kindness_coefficient = fake.random.random()
            for user_id in fake.random.sample(user_ids, n_votes):
                value = Command.fast_vote(kindness_coefficient)
                rating += value
                votes.append(
                    Vote(
                        value=value,
                        object_id=model.pk,
                        content_type_id=model_type_id,
                        user_id=user_id,
                    )
                )
            model.rating += rating

        Vote.objects.bulk_create(votes)
        model_cls.objects.bulk_update(models, ['rating'])

    def handle(self, *args, **options):
        if (users := options["users"]) > 0:
            print(f'Generate {users} users')
            self.create_users(users)
        if (tags := options['tags']) > 0:
            print(f'Generate {tags} tags')
            self.create_tags(tags)
        if (articles := options['articles']) > 0:
            max_tags_per_article = options['max_tags_per_article']
            max_sentences_per_article = options['max_sentences_per_article']
            print(f'Generate {articles} articles with up to {max_sentences_per_article} sentences and up to {max_tags_per_article} tags for each article')
            self.create_articles(articles, max_tags_per_article, max_sentences_per_article)
        if (comments := options['comments']) > 0:
            max_sentences_per_comment = options['max_sentences_per_comment']
            print(f'Generate {comments} comments with up to {max_sentences_per_comment} sentences for each comment')
            self.create_comments(comments, max_sentences_per_comment)
        if (max_votes_per_article := options["max_votes_per_article"]) > 0:
            print(f'Generate up to {max_votes_per_article} votes for each article')
            self.generate_votes_for_model(Article, max_votes_per_article)
        if (max_votes_per_comment := options["max_votes_per_comment"]) > 0:
            print(f'Generate up to {max_votes_per_comment} votes for each comment')
            self.generate_votes_for_model(Comment, max_votes_per_comment)
