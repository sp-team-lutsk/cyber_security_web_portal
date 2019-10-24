import urllib.request
from .models import News


def int_news():
    projects = []

    photo = ''
    header = input("Заголовок:")
    opis = input("Текс:")
    link = ''

    projects.append({
        'image': photo,
        'title': header,
        'description': opis,
        'read_more': link
    })

    for project in projects:
        print(project)

    return projects
def save(projects):
    for project in projects:
        News.objects.create(
                title=project['title'],
                description=project['description'],
                news_link=project['read_more'],
                images_link=project['image1'])


def main():
    projects = []

    int_news()
    save(projects)

if __name__ == '__main__':
    main()

