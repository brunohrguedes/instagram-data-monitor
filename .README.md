### Requisitos
	- python 3.6 ou superior
### Recomenda-se

- [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [pós-instalação](https://docs.docker.com/install/linux/linux-postinstall/)
- [docker-compose](https://docs.docker.com/compose/install/#prerequisites)
+ No caso de o seu sistema não ser Linux , veja siga as (instruções específicas)[https://docs.docker.com/install] para o seu sistema.

* Nota: as instruções abaixo supõem que se esteja utilizando um terminal em ambiente Mac/Linux e que o diretório atual é o logo acima da pasta *src* deste projeto. No caso se estar rodando via *docker*, o sistema operacional pode ser Windows 10.

##   Rodando nativamente em sua máquina

* Importante: antes de mais nada, é preciso editar o arquivo *main.py*, localizado dentro da pasta *src*, e remover, **na linha 7** deste arquivo, a sequência de caracteres **"src."**.
Além disso, excute o comando:
```shell
	pip install -r requirements.txt
``` 
Caso dê algum erro de permissão, execute o comando acima precedido pela expressão *sudo* e um espaço em branco à direita.

+ Como rodar o coletor de dados do Instagram:
	```shell
		cd src
		python main.py
	```
	Os dados coletados por esse programa ficam registrados na pasta *Dados/dados_gerais/csv/*.
+ Como rodar o coletor de stories do Instagram:
	```shell
		cd src/stories
		python stories.py
	```
	Será perguntado ao usuário qual o nome do arquivo de saída. Caso queira algum específico, basta digitá-lo e teclar ENTER, com o detalhe de que *nomes com símbolos que não letras ou números sem acento* podem causar erro na execução do programa. Portanto, use apenas letras (sem acento ou símbolos especiais (cedilha por exemplo) ) e números.
	Em caso de erro durante o download das stories, o seguinte procedimento deve ser feito:
		1. navegue até a pasta **Dados**, que se localiza no mesmo nível hierárquico que a pasta *src*.
		2. A partir dess ponto, entre pasta *dados_gerais* e depois na pasta *csv*.
		3. Delete o último arquivo criado.
		4. Volte ao *terminal* e entre novamente o nome do arquivo para guardar os dados.
	Caso queira abortar o programa em algum momento, pressione as teclas *Ctrl*/*Command* e, com elas pressionadas, pressione a tecla *C*.

## Rodando no docker
	
Primeiramente, copie os arquivos *Dockerfile* e *docker-compose.yml* para um diretório um nível acima da pasta *instagram-data-monitor*, a qual deve conter diversas pastas incluindo a *src*.  
Após isso, execute o comando:
```shell
	docker build -t insta:v0 .
```
Isso irá gerar uma imagem, a qual será usada sempre que se deseja rodar a aplicação. Após isso, digite o comando:
```shell
	docker-compose run insta bash
```
Isso irá iniciar um (*container*)[]. A partir deste container, basta seguir as instruções de como rodar os coletores de dados normalmente, conforme expicado nas seções **Como rodar o coletor de dados do Instagram** e **Como rodar o coletor de stories do Instagram**. Os dados ficarão armazenados nas mesmas pastas que ficariam caso o não fossem rodados os coletores via docker.  
Para sair do conteiner, digite o comando 
```shell
	exit
```
ou mantenha pressionado a tecla *Ctrl*/*Cmd* e, enquanto isso, aperte a tecla *D*.
