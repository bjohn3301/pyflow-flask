# Py.Flow - Fundamentos de Python (UNIESP)

Este projeto consiste no desenvolvimento de uma aplicação web interativa utilizando o framework Flask. O objetivo é criar um site informativo sobre os fundamentos da programação em Python, incluindo uma funcionalidade de perguntas e respostas integrada com a API do Gemini e um dicionário interativo de termos de programação com persistência em arquivo JSON.

<!-- Badges de Tecnologia e Status -->
<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
  <img src="https://img.shields.io/badge/Status-Concluído%20(v1.0)-brightgreen?style=for-the-badge" alt="Status do Projeto"/>
  <!-- Você pode mudar o status para "Em Desenvolvimento" se ainda estiver mexendo muito: -->
  <!-- <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange?style=for-the-badge" alt="Status do Projeto"/> -->
</p>

## Equipe

*   **Abraão** - Dev - [GitHub](https://github.com/abraao488)
*   **Brenner** - Dev - [GitHub](https://github.com/bjohn3301)

## 1. Estrutura do Site e Conteúdo de Cada Seção

*   **`/` (Página Inicial):** apresentação do projeto.
*   **`/equipe`:** informações sobre os desenvolvedores.
*   **`/python/selecao`:** conteúdo sobre estruturas de seleção em python.
*   **`/python/repeticao`:** conteúdo sobre estruturas de repetição.
*   **`/python/vetores`:** conteúdo sobre vetores e matrizes.
*   **`/python/funcoes`:** conteúdo sobre funções e procedimentos.
*   **`/python/excecoes`:** conteúdo sobre tratamento de exceções.
*   **`/tirar-duvidas`:** seção para perguntas à api do gemini.
*   **`/dicionario`:** dicionário de termos com funcionalidades crud.

**Arquivos Principais:**
*   `app.py`: lógica da aplicação flask, rotas, integração com gemini, crud do dicionário.
*   `dicionario.json`: arquivo json para persistência dos termos.
*   `templates/`: arquivos html.
    *   `base.html`: template base.
    *   demais arquivos `.html` para cada página.
*   `static/`: arquivos estáticos.
    *   `css/style.css`: folha de estilos.
    *   `js/script.js`: javascript para interatividade.
    *   `images/`: imagens da equipe (opcional).
*   `.env`: arquivo para a chave da api do gemini (não versionado).
*   `requirements.txt`: dependências python.
*   `.gitignore`: arquivos e pastas ignorados pelo git.

## 2. Tecnologias Utilizadas

*   **Linguagem Principal:** Python 3.x
*   **Framework Web:** Flask
*   **Frontend:** HTML5, CSS3, JavaScript (vanilla)
*   **API Externa:** Google Gemini API (via biblioteca `google-generativeai`)
*   **Persistência de Dados (Dicionário):** Arquivo JSON
*   **Gerenciamento de Ambiente/Dependências:** Python `venv`, `pip`, `requirements.txt`, `python-dotenv`
*   **Controle de Versão:** Git

## 3. Integração com a API do Gemini

A integração com a API do Gemini é feita na rota `/tirar-duvidas` do `app.py`.
1.  A chave da API é carregada do arquivo `.env`.
2.  O modelo `gemini-2.5-flash-preview-05-20` é inicializado.
3.  A pergunta do usuário é enviada ao modelo através de um prompt customizado para gerar respostas em tom informal e minúsculas.
4.  A resposta é processada (remoção de blocos de código markdown, conversão para minúsculas, remoção de espaços extras) antes de ser exibida.
5.  Mensagens flash informam o usuário sobre o status ou erros.

## 4. Como Executar a Aplicação Flask Localmente

1.  **Clone o repositório:**
    ```bash
    git clone <(https://github.com/bjohn3301/pyflow-flask.git)>
    cd <pyflow-flask>
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/macOS:
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Crie o arquivo `.env`:**
    Na raiz do projeto, crie um arquivo `.env` e adicione sua chave da API do Gemini:
    ```
    GEMINI_API_KEY="chave da api"
    ```
5.  **Execute a aplicação Flask:**
    ```bash
    flask run
    ```
6.  Abra seu navegador e acesse: `http://127.0.0.1:5000`

## 5. Breve Descrição das Principais Partes do Código Python (`app.py`)

*   **Configuração Inicial:** importações, inicialização do app flask, `secret_key`, carregamento de variáveis do `.env`.
*   **Configuração da API Gemini:** carrega a chave e inicializa o `GenerativeModel`.
*   **Funções do Dicionário (`carregar_dicionario`, `salvar_dicionario`):** manipulação do `dicionario.json` para o crud.
*   **Rotas de Navegação e Conteúdo (`/`, `/equipe`, `/python/*`):** renderizam os templates html correspondentes.
*   **Rota `/tirar-duvidas`:** processa a pergunta do usuário, interage com a api do gemini e exibe a resposta.
*   **Rotas do Dicionário (`/dicionario`, `/dicionario/adicionar`, etc.):** implementam as funcionalidades crud para os termos.
*   **Bloco de Execução:** `if __name__ == '__main__': app.run(debug=True)` para rodar o servidor de desenvolvimento.
