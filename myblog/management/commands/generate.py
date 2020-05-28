from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from myblog.models.comment import Comment
from myblog.models.post import Post
from myblog.models.tag import Tag
from myblog.models.vote import Vote

fake = Faker()


class Command(BaseCommand):
    help = 'Generates fake data for db'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int, default=0)
        parser.add_argument('-t', '--tags', type=int, default=0)
        parser.add_argument('-T', '--max-tags-per-post', type=int, default=0)
        parser.add_argument('-p', '--posts', type=int, default=0)
        parser.add_argument('-c', '--comments', type=int, default=0)
        parser.add_argument('-P', '--max-votes-per-post', type=int, default=0)
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
    def create_posts(posts, max_tags_per_post):
        user_id_max = User.objects.count()
        Post.objects.bulk_create(
            [
                Post(
                    title=fake.sentence(),
                    body=fake.paragraph(nb_sentences=15),
                    user_id=Command.fast_randint(1, user_id_max),
                )
                for i in range(posts)
            ]
        )

        through_model = Post.tags.through
        n_posts = Post.objects.count()
        tag_ids = list(Tag.objects.values_list('id', flat=True))  # list for sample()
        through_list = []
        for post_id in range(n_posts - posts + 1, n_posts + 1):
            n_tags = Command.fast_randint(0, max_tags_per_post)
            through_list += [
                through_model(
                    post_id=post_id,
                    tag_id=tag_id,
                )
                for tag_id in fake.random.sample(tag_ids, n_tags)
            ]
        through_model.objects.bulk_create(through_list)

    @staticmethod
    def create_comments(posts):
        user_id_max = User.objects.count()
        post_id_max = Post.objects.count()
        Comment.objects.bulk_create(
            [
                Comment(
                    body=fake.paragraph(nb_sentences=15),
                    user_id=Command.fast_randint(1, user_id_max),
                    post_id=Command.fast_randint(1, post_id_max),
                )
                for i in range(posts)
            ]
        )

    @staticmethod
    def generate_votes_for_model(model_cls, max_votes_per_post):
        if max_votes_per_post == 0:
            return

        user_ids = list(User.objects.values_list('id', flat=True))  # list for sample()
        models = model_cls.objects.all()
        model_type_id = ContentType.objects.get_for_model(model_cls).id

        votes = []
        for model in models:
            n_votes = Command.fast_randint(0, max_votes_per_post)
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
        print(f'Generate {options["users"]} users')
        self.create_users(options['users'])
        print(f'Generate {options["tags"]} tags')
        self.create_tags(options['tags'])
        print(f'Generate {options["posts"]} posts')
        self.create_posts(options['posts'], options['max_tags_per_post'])
        print(f'Generate {options["comments"]} comments')
        self.create_comments(options['comments'])
        print(f'Generate up to {options["max_votes_per_post"]} votes for each post')
        self.generate_votes_for_model(Post, options["max_votes_per_post"])
        print(f'Generate up to {options["max_votes_per_comment"]} votes for each comment')
        self.generate_votes_for_model(Comment, options["max_votes_per_comment"])
