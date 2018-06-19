import wget
import re
import os


class Actor(object):
    """Inicia os dados comuns de um ator"""
    #@TODO Detalhar cada argumento e o porquê destes valores default
    def __init__(self, username, full_name, posts=-1, follows=-1, followed=-1):
        self.full_name = full_name
        self.username = username
        self.followed = followed
        self.follows = follows
        self.posts = posts


# Ideia: ter uma hash pra mapear (nome_instagram => nome real)
def actor_from_url(url):
    """Recebe uma url e retorna um objeto do tipo ator"""
    #@TODO Detalhar o argumento url

    #@TODO Explícito é melhor que implícito, logo, qual tipo de exception
    # vocês estão coletando? Porque está retornando um booleano ao
    # coletar ela?
    try:
        actor = re.findall(r'\.com\/(.*)\/', url)[0]
    except:
        return False

    #@TODO Explícito é melhor que implícito, logo, qual tipo de exception
    # vocês estão coletando? Porque a ignoram quando encontram ela?
    try:
        # Impedir uso do arquivo velho e apaga-lo apos o uso
        os.remove(f'{actor}.html')
    except:
        pass

    #@TODO Logging é preferível do que prints
    print(f'ator :: {actor}')

    #@TODO Explícito é melhor que implícito, logo, qual tipo de exception
    # vocês estão coletando? Porque está tratando ela desta forma?
    try:
        html_file = open(wget.download(url=url, out=f'{actor}.html'), 'r')
        html = html_file.read()
        html_file.close()
        os.remove(f'{actor}.html')
    except:
        with open('data/removed_actors.txt', 'a') as rm_actors:
            rm_actors.write(f'{url}\n')
            full_name = actor
            #@TODO Porque existem estes valores default se já contém valores
            # default na classe?
            followed = 0
            follows = 0
            posts = 0

        return Actor(username=actor, posts=posts, followed=followed,
                    follows=follows, full_name=full_name)

    followed = int(re.findall(r'edge_followed_by":\{"count":(\d+)', html)[0])
    posts = int(re.findall(r'"edge_owner_to_timeline_media":\{"count":(\d+)',
                            html)[0])
    follows = int(re.findall(r'"edge_follow":\{"count":(\d+)', html)[0])
    full_name = re.findall(r'"full_name":"(.*?")',
                            html)[0][:-1].encode().decode()
    full_name = bytes(full_name, 'utf-8').decode('unicode_escape')

    return Actor(username=actor, posts=posts, followed=followed,
                follows=follows, full_name=full_name)
