# Instruções para Configuração do Ambiente de Desenvolvimento

Este documento descreve as ferramentas e dependências necessárias para configurar o ambiente de desenvolvimento do **Projeto Nivelamento**.

---

## 🛠️ **Ferramentas Essenciais**

1. **Git**  
   Para controle de versão, faça o download e instale o Git:  
   [Baixar Git](https://git-scm.com/downloads)

2. **Docker Desktop**  
   Para gerenciar contêineres de banco de dados e serviços, instale o Docker:  
   [Baixar Docker](https://www.docker.com/products/docker-desktop)

3. **Python 3.10+**  
   O backend será desenvolvido em Python, então instale a versão 3.10 ou superior:  
   [Baixar Python](https://www.python.org/downloads/)

---

## 🗄️ **Banco de Dados**

1. **PostgreSQL**  
   Para gerenciar o banco de dados do projeto, instale o PostgreSQL:  
   [Baixar PostgreSQL](https://www.postgresql.org/download/)

   **Alternativa**: Se preferir não instalar o PostgreSQL localmente, você pode rodar o banco de dados usando Docker.

---

## ⚡ **Ferramentas de Desenvolvimento**


1. **VS Code**  
   É recomendada a utilização do [Visual Studio Code](https://code.visualstudio.com/) como editor de código.

   - **Extensões recomendadas no VS Code**:
     - Python
     - Docker
     - PostgreSQL
     - REST Client (para testar APIs)

2. **PyCharm**  
   Outra excelente opção para o desenvolvimento em Python é o [PyCharm](https://www.jetbrains.com/pycharm/), que oferece suporte completo ao Python, incluindo ferramentas de depuração, testes e mais.

3. **DBeaver ou PgAdmin**  
   Ferramentas para gerenciar o banco de dados PostgreSQL de maneira mais intuitiva.  
   - [Baixar DBeaver](https://dbeaver.io/download/)
   - [Baixar PgAdmin](https://www.pgadmin.org/download/)

4. **Insomnia**  
   Ferramenta para testar e interagir com APIs REST de forma simples e eficiente.  
   [Baixar Insomnia](https://insomnia.rest/download)

---

## 📦 **Instalação das Dependências do Projeto**

1. **Criar Ambiente Virtual (Recomendado)**  
   Para isolar as dependências do projeto, crie um ambiente virtual:

   ```sh
   python -m venv venv
