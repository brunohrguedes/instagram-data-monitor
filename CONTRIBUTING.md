# Contribuições

## Ferramentas utilizadas

* [python 3.6](https://www.python.org/)
* [pip](https://pypi.python.org/pypi/pip)

## Preparar o ambiente

### Clonar repositório

```
$ git clone git@github.com:unb-cic-esw/instagram-data-monitor.git
```

### Criar virtualenv

```
$ python3 -m venv venv
$ source venv/bin/activate
```

### Instalar dependências

Todas as bibliotecas de que o projeto depende estão listadas no arquivo
[requirements.txt](requirements.txt). Para instalá-las, execute:

```
$ cd instagram-data-monitor
$ source venv/bin/activate
$ pip install -r requirements.txt
```


## Executar o sistema

- Prepare o ambiente como foi explicado acima
- Para coletar informações gerais dos atores do ``Instagram`` execute o comando
abaixo. Os dados coletados ficam registrados na pasta *data/actors_info/csv/*.

```
$	python -m src/main.py
```

- Para coletar stories dos atores do ``Instagram`` execute o comando
abaixo. Será perguntado ao usuário qual o nome do arquivo de saída. Caso
queira algum específico, basta digitá-lo e teclar ``ENTER``, com o detalhe
de que apenas *nomes sem caracteres especiais (acento, cedilha, etc)* serão
aceitos.

```
$ python -m src/stories.py
```

  Obs.1: Em caso de erro durante o download das stories, o seguinte procedimento
  deve ser feito:
  	1. navegue até a pasta **data**, que se localiza no mesmo nível hierárquico
    que a pasta *src*.
  	2. A partir desse ponto, entre na pasta *acotrs_info* e depois na
    pasta *csv*.
  	3. Delete o último arquivo criado.
  	4. Volte ao *terminal* e entre novamente o nome do arquivo para guardar
    os dados.

  Obs.2: Caso queira sair do programa em algum momento, pressione as teclas
  *Ctrl*/*Command* e, com elas pressionadas, pressione a tecla *C*.

## Adicionar funcionalidades

Para cada estória a ser resolvida, seguir o seguinte procedimento:

- Clone o repositório
- Prepare o ambiente como foi explicado acima
- Crie uma issue em formato de estória da funcionalidade/bug/etc
- Crie uma branch (local e remoto) sobre o problema a ser resolvido, e.g.:

```
$ git checkout -b dev-subscribers
$ git push origin dev-subscribers
```

- Após resolver a issue, rode os devidos testes (rode mesmo porque seu PR não
  será aceito se seus testes não estiverem passando!)
- Abra um ticket de pull request no github com o sentido (base <- head):

 ```
 unb-cic-esw/instagram-data-monitor/master <- unb-cic-esw/instagram-data-monitor/dev-subscribers
 ```

- Espere o Travis CI executar os testes de integração
- Se todos os testes passarem então peça algum colega do time/organização para aceitar seu PR :rocket:



## Executar os testes

Todos os testes foram desenvolvidos utilizando a biblioteca
[unittest](https://docs.python.org/3/library/unittest.html) nativa do Python.
Para executá-los, a partir da pasta raiz do projeto, execute:

```
$ python -m unittest discover tests
```


## Checar cobertura de código

Para checar a cobertura de código foi utilizado a biblioteca
[coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/).
Para verificar o relatório da cobertura a partir de um determinado arquivo,
execute:

```
$ coverage run --omit=venv/*,*__init__.py -m [modulo do arquivo].[arquivo sem .py] && coverage report -m
```


## Checar estilo de código

Para seguir os padrões PEP8 de código python estamos usando a biblioteca
[pycodestyle](http://pycodestyle.pycqa.org/en/latest/).
Para cada novo módulo adicionado ao projeto é necessário criar um teste para
checar seu estilo de código (ver exemplos em [test_pep8](tests/test_pep8.py)).
Para executar a ferramenta e checar algum código, basta executar:

```
$ pip install pycodestyle
$ pycodestyle [arquivo].py
```


## Executando o sistema via docker

Primeiramente, copie os arquivos *Dockerfile* e *docker-compose.yml* para um
diretório um nível acima da pasta *instagram-data-monitor*, a qual deve conter
diversas pastas incluindo a *src*.  

Após isso, execute o comando:

```
$	docker build -t insta:v0 .
```

Isso irá gerar uma imagem, a qual será usada sempre que se deseja rodar a
aplicação. Após isso, digite o comando:

```
$	docker-compose run insta bash
```

Isso irá iniciar um (*container*)[]. A partir deste container, basta seguir as
instruções de como rodar os coletores de dados normalmente, conforme expicado
nas seções **Como rodar o coletor de dados do Instagram** e
**Como rodar o coletor de stories do Instagram**. Os dados ficarão armazenados
nas mesmas pastas que ficariam caso o não fossem rodados os coletores via
docker.  

Para sair do conteiner, digite o comando abaixo ou mantenha pressionado a
tecla *Ctrl*/*Cmd* e, enquanto isso, aperte a tecla *D*.

```
$	exit
```

## Leitura recomendada

- [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [pós-instalação](https://docs.docker.com/install/linux/linux-postinstall/)
- [docker-compose](https://docs.docker.com/compose/install/#prerequisites)

No caso de o seu sistema não ser Linux, siga as
(instruções específicas)[https://docs.docker.com/install] para o seu sistema.
