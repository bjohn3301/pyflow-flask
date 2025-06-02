from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

DICIONARIO_ARQUIVO = 'dicionario.json'

GEMINI_API_KEY_VAR = os.getenv("GEMINI_API_KEY")
gemini_model = None

if GEMINI_API_KEY_VAR:
    try:
        genai.configure(api_key=GEMINI_API_KEY_VAR)
        MODEL_NAME = 'gemini-2.5-flash-preview-05-20'
        gemini_model = genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        gemini_model = None
else:
    pass


def carregar_dicionario():
    if not os.path.exists(DICIONARIO_ARQUIVO):
        return []
    try:
        with open(DICIONARIO_ARQUIVO, 'r', encoding='utf-8') as f:
            termos = json.load(f)
        return sorted(termos, key=lambda x: x['termo'].lower())
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def salvar_dicionario(termos):
    termos_ordenados = sorted(termos, key=lambda x: x['termo'].lower())
    with open(DICIONARIO_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(termos_ordenados, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html', page_title="página inicial")

@app.route('/equipe')
def pagina_equipe():
    equipe = [
        {
            "nome": "abraão eber", 
            "linkedin": "https://github.com/abraao488", 
            "foto": "abraao.jpg", 
            "info": "dev"
        },
        {
            "nome": "brenner cordeiro", 
            "linkedin": "https://github.com/bjohn3301", 
            "foto": "brenner.jpg", 
            "info": "dev"
        }
    ]
    return render_template('equipe.html', equipe=equipe, page_title="nossa equipe")

@app.route('/python/selecao')
def conteudo_selecao():
    return render_template('python_selecao.html', page_title="estruturas de seleção")

@app.route('/python/repeticao')
def conteudo_repeticao():
    try:
        return render_template('python_repeticao.html', page_title="estruturas de repetição")
    except Exception as e:
        return f"erro ao carregar a página de repetição: {e}"


@app.route('/python/vetores')
def conteudo_vetores():
    try:
        return render_template('python_vetores.html', page_title="vetores e matrizes")
    except Exception as e:
        return f"erro ao carregar a página de vetores: {e}"

@app.route('/python/funcoes')
def conteudo_funcoes():
    try:
        return render_template('python_funcoes.html', page_title="funções e procedimentos")
    except Exception as e:
        return f"erro ao carregar a página de funções: {e}"

@app.route('/python/excecoes')
def conteudo_excecoes():
    try:
        return render_template('python_excecoes.html', page_title="tratamento de exceções")
    except Exception as e:
        return f"erro ao carregar a página de exceções: {e}"

@app.route('/tirar-duvidas', methods=['GET', 'POST'])
def tirar_duvidas():
    resposta_gemini = None
    pergunta_usuario = ""
    if request.method == 'POST':
        pergunta_usuario = request.form.get('pergunta', '').strip()
        
        if not gemini_model:
            flash("o serviço de ia não está configurado no momento. tente mais tarde.", "danger")
        elif not pergunta_usuario:
            flash("por favor, digite sua pergunta.", "warning")
        else:
            try:
                prompt_completo = f"olá, gemini. estou aprendendo python e tenho uma dúvida. poderia explicar de uma forma simples e direta, tudo em minúsculo e sem usar termos muito complicados? a pergunta é:\n\n{pergunta_usuario}\n\nobrigado!"
                response = gemini_model.generate_content(prompt_completo)
                
                texto_resposta = response.text.lower().strip()
                
                texto_resposta = re.sub(r'^\s*```[a-zA-Z]*\n?', '', texto_resposta)
                texto_resposta = re.sub(r'\n?```\s*$', '', texto_resposta)
                texto_resposta = texto_resposta.strip()

                resposta_gemini = texto_resposta

            except Exception as e:
                flash(f"ocorreu um erro ao tentar contato com a api do gemini: {str(e)}", "danger")
    return render_template('tirar_duvidas.html', page_title="tirar dúvidas com ia", resposta_gemini=resposta_gemini, pergunta_usuario=pergunta_usuario)

@app.route('/dicionario')
def dicionario_listar():
    termos = carregar_dicionario()
    return render_template('dicionario_listar.html', termos=termos, page_title="dicionário de termos")

@app.route('/dicionario/adicionar', methods=['GET', 'POST'])
def dicionario_adicionar():
    if request.method == 'POST':
        novo_termo = request.form['termo'].strip()
        nova_definicao = request.form['definicao'].strip()
        if not novo_termo or not nova_definicao:
            flash("ops, o termo e a definição precisam ser preenchidos.", 'warning')
            return render_template('dicionario_adicionar.html', page_title="adicionar novo termo", termo=novo_termo, definicao=nova_definicao)
        
        termos = carregar_dicionario()
        if any(t['termo'].lower() == novo_termo.lower() for t in termos):
            flash(f"o termo '{novo_termo}' já existe no dicionário.", 'warning')
            return render_template('dicionario_adicionar.html', page_title="adicionar novo termo", termo=novo_termo, definicao=nova_definicao)

        termos.append({'termo': novo_termo, 'definicao': nova_definicao})
        salvar_dicionario(termos)
        flash(f"termo '{novo_termo}' adicionado com sucesso!", 'success')
        return redirect(url_for('dicionario_listar'))
    return render_template('dicionario_adicionar.html', page_title="adicionar novo termo")

@app.route('/dicionario/alterar/<termo_original>', methods=['GET', 'POST'])
def dicionario_alterar(termo_original):
    termos = carregar_dicionario()
    termo_obj = next((t for t in termos if t['termo'] == termo_original), None)
    if not termo_obj:
        flash("termo não encontrado para alteração.", 'danger')
        return redirect(url_for('dicionario_listar'))

    if request.method == 'POST':
        novo_termo_str = request.form['termo'].strip()
        nova_definicao = request.form['definicao'].strip()
        if not novo_termo_str or not nova_definicao:
            flash("o termo e a definição são obrigatórios.", 'warning')
            return render_template('dicionario_alterar.html', page_title=f"alterar termo: {termo_original}", termo=termo_obj, termo_original=termo_original)

        if novo_termo_str.lower() != termo_original.lower() and \
           any(t['termo'].lower() == novo_termo_str.lower() for t in termos):
            flash(f"o termo '{novo_termo_str}' já está cadastrado.", 'warning')
            return render_template('dicionario_alterar.html', page_title=f"alterar termo: {termo_original}", termo={'termo': novo_termo_str, 'definicao': nova_definicao}, termo_original=termo_original)
        
        for i, t in enumerate(termos):
            if t['termo'] == termo_original:
                termos[i]['termo'] = novo_termo_str
                termos[i]['definicao'] = nova_definicao
                break
        
        salvar_dicionario(termos)
        flash(f"termo '{novo_termo_str}' atualizado com sucesso!", 'success')
        return redirect(url_for('dicionario_listar'))
    
    return render_template('dicionario_alterar.html', page_title=f"alterar termo: {termo_original}", termo=termo_obj, termo_original=termo_original)

@app.route('/dicionario/deletar/<termo_original>', methods=['POST'])
def dicionario_deletar(termo_original):
    termos = carregar_dicionario()
    termos_filtrados = [t for t in termos if t['termo'] != termo_original]
    if len(termos_filtrados) < len(termos):
        salvar_dicionario(termos_filtrados)
        flash(f"termo '{termo_original}' deletado com sucesso.", 'success')
    else:
        flash(f"termo '{termo_original}' não encontrado para deleção.", 'warning')
    return redirect(url_for('dicionario_listar'))

if __name__ == '__main__':
    app.run(debug=True)