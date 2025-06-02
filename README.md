# Projeto Final Flask - Fundamentos de Programação em Python (UNIESP)

Este projeto consiste no desenvolvimento de uma aplicação web interativa utilizando o framework Flask. O objetivo é criar um site informativo sobre os fundamentos da programação em Python, incluindo uma funcionalidade de perguntas e respostas integrada com a API do Gemini e um dicionário interativo de termos de programação com persistência em arquivo de texto.

## Equipe

*   [Nome do Aluno 1] - [Link LinkedIn/Website (opcional)]
*   [Nome do Aluno 2] - [Link LinkedIn/Website (opcional)]
*   ... (adicionar todos os membros)

## 1. Estrutura do Site e Conteúdo de Cada Seção

*   **`/` (Página Inicial):** Apresentação do projeto.
*   **`/equipe`:** Informações sobre os desenvolvedores do projeto.
*   **`/python/selecao`:** Conteúdo sobre Estruturas de Seleção em Python (conceito, aplicação, exemplo).
*   **`/python/repeticao`:** Conteúdo sobre Estruturas de Repetição em Python.
*   **`/python/vetores`:** Conteúdo sobre Vetores e Matrizes em Python.
*   **`/python/funcoes`:** Conteúdo sobre Funções e Procedimentos em Python.
*   **`/python/excecoes`:** Conteúdo sobre Tratamento de Exceções em Python.
*   **`/tirar-duvidas`:** Seção para submeter perguntas sobre Python e obter respostas da API do Gemini.
*   **`/dicionario`:** Seção do Dicionário de Termos:
    *   Visualização de todos os termos.
    *   Opção para adicionar, alterar e deletar termos.
    *   Persistência dos dados em `dicionario.json`.

**Arquivos Principais:**
*   `app.py`: Lógica principal da aplicação Flask, rotas, integração com Gemini e CRUD do dicionário.
*   `dicionario.json`: Arquivo de texto (JSON) para armazenar os termos e definições do dicionário.
*   `templates/`: Contém os arquivos HTML.
    *   `base.html`: Template base com a estrutura comum (navegação, rodapé).
    *   `index.html`, `equipe.html`, `python_*.html`, `tirar_duvidas.html`, `dicionario_*.html`: Páginas específicas.
*   `static/`: Contém arquivos estáticos.
    *   `css/style.css`: Folha de estilos principal.
*   `.env`: Arquivo para armazenar a chave da API do Gemini (NÃO versionado).
*   `requirements.txt`: Lista de dependências Python.
*   `.gitignore`: Especifica arquivos e pastas a serem ignorados pelo Git.

## 2. Tecnologias Utilizadas

*   **Linguagem de Programação:** Python 3.x
*   **Framework Web:** Flask
*   **Bibliotecas Python:**
    *   `Flask`: Para a estrutura da aplicação web.
    *   `python-dotenv`: Para carregar variáveis de ambiente (API Key).
    *   `google-generativeai`: Para interação com a API do Gemini.
*   **Frontend:** HTML5, CSS3
*   **Persistência de Dados:** Arquivo JSON (`dicionario.json`)
*   **Controle de Versão:** Git

## 3. Integração com a API do Gemini

A integração com a API do Gemini é realizada na rota `/tirar-duvidas` no arquivo `app.py`.
1.  A chave da API é carregada de forma segura do arquivo `.env` utilizando a biblioteca `python-dotenv`.
2.  O modelo `gemini-1.5-flash-latest` (ou similar) da biblioteca `google-generativeai` é inicializado.
3.  Quando um usuário submete uma pergunta através do formulário na página `tirar_duvidas.html`, a pergunta é enviada para o backend Flask.
4.  Um prompt é construído, instruindo a IA a agir como um especialista em Python e responder à pergunta do usuário.
5.  A função `gemini_model.generate_content()` é chamada com o prompt.
6.  A resposta textual da API é então retornada e exibida na página HTML.
7.  Tratamento de erros básico é implementado para casos onde a API não está configurada ou ocorre um erro na comunicação.

## 4. Como Executar a Aplicação Flask Localmente

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    # Se estiver usando git
    # git clone <URL_DO_REPOSITORIO>
    # cd <NOME_DA_PASTA_DO_PROJETO>
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Crie o arquivo `.env`:**
    Na raiz do projeto, crie um arquivo chamado `.env` e adicione sua chave da API do Gemini:
    ```
    GEMINI_API_KEY="SUA_CHAVE_API_DO_GEMINI_AQUI"
    ```
5.  **Execute a aplicação Flask:**
    ```bash
    flask run
    # Ou
    # python app.py
    ```
6.  Abra seu navegador e acesse: `http://127.0.0.1:5000`

## 5. Breve Descrição das Principais Partes do Código Python (`app.py`)

*   **Configuração Inicial:** Importação de bibliotecas, inicialização do Flask app, configuração da `secret_key` para flash messages, e carregamento de variáveis de ambiente com `load_dotenv()`.
*   **Configuração da API Gemini:** Carregamento da `GEMINI_API_KEY` e inicialização do `GenerativeModel`.
*   **Funções do Dicionário (`carregar_dicionario`, `salvar_dicionario`):** Lógica para ler e escrever dados no arquivo `dicionario.json`, garantindo a persistência dos termos. Os termos são ordenados alfabeticamente.
*   **Rotas de Navegação e Conteúdo (`/`, `/equipe`, `/python/*`):** Rotas simples que renderizam os templates HTML correspondentes com o conteúdo informativo.
*   **Rota `/tirar-duvidas`:**
    *   Métodos `GET` (exibir formulário) e `POST` (processar pergunta).
    *   Coleta a pergunta do usuário.
    *   Envia a pergunta para a API do Gemini após construir um prompt adequado.
    *   Exibe a resposta da IA ou mensagens de erro/aviso usando `flash`.
*   **Rotas do Dicionário (`/dicionario`, `/dicionario/adicionar`, `/dicionario/alterar/<termo>`, `/dicionario/deletar/<termo>`):**
    *   Implementam as funcionalidades CRUD (Create, Read, Update, Delete) para o dicionário.
    *   Utilizam formulários HTML para entrada de dados.
    *   Validam entradas (termos e definições não vazios, verificação de termos duplicados).
    *   Usam `flash messages` para feedback ao usuário.
    *   Redirecionam o usuário após as operações.
*   **Execução da Aplicação:** O bloco `if __name__ == '__main__':` inicia o servidor de desenvolvimento do Flask.