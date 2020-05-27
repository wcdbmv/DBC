from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from faker import Faker
from myblog.models.comment import Comment
from myblog.models.post import Post

fake = Faker()


class Command(BaseCommand):
    help = 'Generates fake data for db'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', type=int, default=0)
        parser.add_argument('-p', '--posts', type=int, default=0)
        parser.add_argument('-c', '--comments', type=int, default=0)

    @staticmethod
    def create_users(users):
        offset_id = User.objects.count()
        User.objects.bulk_create(
            [
                User(
                    first_name=(first_name := fake.first_name()),
                    last_name=(last_name := fake.last_name()),
                    username=(username := f'{first_name}{last_name}{offset_id + i}'),
                    password=f'{username}password',
                    email=f'{username}@example.com',
                )
                for i in range(users)
            ]
        )

    @staticmethod
    def fast_rand(mx):
        return int(fake.random.random() * mx) + 1

    @staticmethod
    def create_posts(posts):
        user_id_max = User.objects.count()
        Post.objects.bulk_create(
            [
                Post(
                    title=fake.sentence(),
                    body=fake.paragraph(nb_sentences=15),
                    user_id=Command.fast_rand(user_id_max),
                )
                for i in range(posts)
            ]
        )

    @staticmethod
    def create_comments(posts):
        user_id_max = User.objects.count()
        post_id_max = Post.objects.count()
        Comment.objects.bulk_create(
            [
                Comment(
                    body=fake.paragraph(nb_sentences=15),
                    user_id=Command.fast_rand(user_id_max),
                    post_id=Command.fast_rand(post_id_max),
                )
                for i in range(posts)
            ]
        )

    def handle(self, *args, **options):
        print(f'Generate {options["users"]} users')
        self.create_users(options['users'])
        print(f'Generate {options["posts"]} posts')
        self.create_posts(options['posts'])
        print(f'Generate {options["comments"]} comments')
        self.create_comments(options['comments'])
