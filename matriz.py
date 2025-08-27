import streamlit as st
from database import DatabaseConnection

# 🔌 Conexão com o banco
db = DatabaseConnection()
db.connect()

st.title("🔐 Gerenciar Matriz de Acesso")

# 🔍 Selecionar usuário
usuarios = db.get_usuarios()
usuario_nomes = [u["usuario"] for u in usuarios]
usuario_selecionado = st.selectbox("👤 Selecione um usuário", usuario_nomes)

usuario_id = next(u["id"] for u in usuarios if u["usuario"] == usuario_selecionado)

# 📦 Carregar módulos e acessos
modulos = db.get_modulos()
acessos_atuais = db.get_acessos_usuario(usuario_id)

st.subheader("🧭 Permissões por módulo")

# 🔁 Interface de checkboxes
for modulo in modulos:
    permitido = modulo["id"] in acessos_atuais
    novo_valor = st.checkbox(modulo["nome"], value=permitido, key=f"mod_{modulo['id']}")
    
    if novo_valor != permitido:
        db.set_acesso(usuario_id, modulo["id"], int(novo_valor))
        st.toast(f"✅ Permissão para '{modulo['nome']}' atualizada.")
        st.rerun()

db.close()