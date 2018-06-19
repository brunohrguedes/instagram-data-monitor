import datetime
import codecs
import os

from src import generate_actor

NOW = datetime.datetime.now()


def generate_actors_info_csv(debug=False, folder='data/actors_info/csv/'):
    """Monta a lista de urls usada para extrair as informações dos atores"""
    #@TODO Detalhar cada argumento e o porquê destes valores default

    if not os.path.exists(folder):
        os.makedirs(folder)

    path = folder
    urls = []
    valid_urls = []

    with open('data/actors_list.txt', 'r') as actors_list:
        for row in actors_list:
            # Retira a quebra de linha
            urls.append(row[:-1])

    filename = f'{path}atores_dados_{NOW.strftime("%d-%m-%y-%H:%M")}.csv'
    with codecs.open(filename, 'w', 'utf-8') as file_data:
        headers = 'Nome real da conta,Conta,Seguidores,Seguindo,Postagens\n'
        file_data.write(headers)

        for url in urls:
            #@TODO Logging é preferível do que prints
            print(url)
            actor = generate_actor.actor_from_url(url)

            #@TODO Porque dessa condicional?
            if actor.follows != 0:
                account = f'https://www.instagram.com/{actor.username}/'
                url_str = f'{actor.full_name},{account},{actor.followed}'\
                            f',{actor.follows},{actor.posts}\n'
                file_data.write(url_str)
                valid_urls.append(url)
            else:
                #@TODO Verificar porque utiliza ; nesta url e na de cima
                # é utilizado ,
                file_data.write(f'{actor.full_name};/s;/s;/s;/s\n')
                valid_urls.append(url)

    #@TODO Este comentário ainda é necessário?
    #  Atualizar a lista mantendo APENAS os links validos
    # with open('atores_lista', 'w') as file_data:
    #     for url in valid_urls:
    #         file_data.write(url+'\n')

    return filename


if __name__ == '__main__':
    generate_actors_info_csv()
