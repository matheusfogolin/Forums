# Forums
Forum project created with Django

# Como executar o projeto:

## Sem Docker:

## Requisitos:
- Python 3.11

Para executar o projeto, primeiro precisamos criar um ambiente virtual para o mesmo. Para isso: 
  - clone o repositório, 
  - abra o prompt de comando,
  - navegue até a raiz do projeto,
  - execute o comando: python3 -m venv 'nome_do_ambiente_virtual'
  - após criação do ambiente, execute o comando para ativa-lo.
  - (Linux): source nome_do_ambiente_virtual/bin/activate
  - (Windows): source nome_do_ambiente_virtual\Scripts\Activate

Após a ativação do ambiente virtual, devemos instalar a dependência do projeto. No mesmo prompt que está na raiz do projeto, executar o seguinte comando:
pip install -r requirements.txt

Após a instalação das dependências, devemos executar o comando para criar o banco de dados. No promp, executar o seguinte comando:
python manage.py migrate

Depois, precisamos criar o superuser(admin) para podermos fazer o gerenciamento do projeto. Para isso, executar o comando:
python manage.py createsuperuser

Ele irá pedir alguns parâmetros, que são:
Email,
Sexo(usar M ou F),
Data de nascimento(Registrar no formato YYYY-mm-dd),
Senha
Confirmação de senha

Pronto! Após esse processo, podemos executar o projeto, com o comando:
python manage.py runserver

Ele estará disponível na url http://127.0.0.1:8000/. Para acessar o painel do admin, o link é http://127.0.0.1:8000/admin.

## Com docker:
## Requisitos:
  - Docker desktop

Para executar o projeto utilizando o docker, é bem simples. Precisamos abrir o prompt de comando, navegar até a pasta do repositório e executar o seguinte comando, para criar a imagem docker:
docker build -t <nome_do_container> .

Com a imagem criada, precisamos executar o projeto, com o seguinte comando:
docker run -d -p 8000:8000 forums

Pronto! O projeto está iniciado, porém, nós precisamos criar o usuário administrador para poder administrar o forum. Para isso, precisamos do id do container docker que está executando o projeto. Podemos descobrir esse ID passando o seguinte comando no prompt:
docker ps
![image](https://github.com/matheusfogolin/Forums/assets/57686224/037c103a-1794-4f15-89c0-e3a0144de818)

O ID do container fica nesse campo que está circulado na imagem.
Com o ID em mãos, precisamos executar o comando:
docker exec -it <id do container> python manage.py createsuperuser

Após feito isso, o programa pedirá alguns parâmetros para criar o administrador, que são:
Email,
Sexo(usar M ou F),
Data de nascimento(Registrar no formato YYYY-mm-dd),
Senha
Confirmação de senha

Pronto! com o administrador criado e o projeto executando, podemos agora interagir com ele na url http://127.0.0.1:8000/ e http://127.0.0.1:8000/admin para o painel do administrador.



