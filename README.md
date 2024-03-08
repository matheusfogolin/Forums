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
  - execute o comando: python3 -m'venv 'nome_do_ambiente_virtual'
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
