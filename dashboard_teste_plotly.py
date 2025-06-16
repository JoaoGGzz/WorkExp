# Criar versão do dashboard com instalação automática de plotly
import streamlit as st
import subprocess
import sys

# Função para instalar plotly se não estiver disponível
def install_plotly():
    try:
        import plotly.express as px
        return True
    except ImportError:
        st.warning("📦 Instalando Plotly... Aguarde alguns segundos.")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly"])
            st.success("✅ Plotly instalado com sucesso!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Erro ao instalar Plotly: {e}")
            return False

# Verificar e instalar plotly
if not install_plotly():
    st.stop()

# Agora importar normalmente
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Resto do código do dashboard...
st.title("🔧 Dashboard ISN - Teste de Instalação")
st.success("✅ Todas as bibliotecas foram carregadas com sucesso!")
st.info("📊 Plotly está funcionando corretamente!")

# Teste rápido do plotly
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[1, 3, 2]))
fig.update_layout(title="Teste Plotly")
st.plotly_chart(fig)
'''

# Salvar versão de teste
with open('dashboard_teste_plotly.py', 'w', encoding='utf-8') as f:
    f.write(dashboard_com_instalacao)

print("✅ Dashboard de teste criado!")
print("\n🧪 dashboard_teste_plotly.py:")
print("- Instala Plotly automaticamente se não estiver disponível")
print("- Testa se tudo está funcionando")
print("- Use este arquivo temporariamente para testar")
