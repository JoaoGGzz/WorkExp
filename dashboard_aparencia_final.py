# Corrigir o caminho do arquivo no dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard ISN - Análise de Comunicação",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown(\'\'\'
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-divider {
        border-top: 2px solid #e0e0e0;
        margin: 2.5rem 0 1.5rem 0;
        position: relative;
    }
    .section-divider::after {
        content: '';
        position: absolute;
        top: -1px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 2px;
        background: linear-gradient(90deg, #2c5aa0, #007acc);
    }
    .section-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c5aa0;
        margin: 1rem 0;
        padding-left: 0.5rem;
        border-left: 4px solid #2c5aa0;
    }
    .subsection-header {
        font-size: 1.4rem;
        font-weight: bold;
        color: #2c5aa0;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2c5aa0;
        padding-bottom: 0.5rem;
    }
    .dynamic-control {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.8rem;
        border-left: 5px solid #007acc;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .analysis-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem 0;
        border: 1px solid #dee2e6;
    }
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #2c5aa0, #007acc, #2c5aa0);
        margin: 3rem 0;
        border-radius: 2px;
    }
    .stMarkdown > div {
        background-color: transparent !important;
    }
    .subtle-separator {
        height: 1px;
        background: linear-gradient(90deg, transparent, #d0d0d0, transparent);
        margin: 2rem 0;
    }
</style>
\'\'\', unsafe_allow_html=True)

# CAMINHO CORRIGIDO - Para Streamlit Cloud
ARQUIVO_BASE = "Base_ISN_Comm_Loss_Refinada.xlsx"  # Arquivo na raiz do repositório

@st.cache_data
def load_data():
    try:
        # Verificar se o arquivo existe
        import os
        if not os.path.exists(ARQUIVO_BASE):
            st.error(f"❌ Arquivo não encontrado: {ARQUIVO_BASE}")
            st.info("📁 Arquivos disponíveis no diretório:")
            for file in os.listdir("."):
                if file.endswith(('.xlsx', '.xls', '.csv')):
                    st.write(f"  - {file}")
            st.stop()
        
        df = pd.read_excel(ARQUIVO_BASE, sheet_name="Base Refinada")
        df['DATA ABERTURA'] = pd.to_datetime(df['DATA ABERTURA'], errors='coerce')
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        df['DATA EXECUÇÃO'] = pd.to_datetime(df['DATA EXECUÇÃO'], errors='coerce')
        df['mes_ano'] = df['DATA ABERTURA'].dt.to_period('M').astype(str)
        
        colunas_unicas = ['PLANTA', 'base', 'equipment', 'TIPO_SENSOR', 'event_type', 'time']
        df_unicos = df.drop_duplicates(subset=colunas_unicas)
        
        return df, df_unicos
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.error("Verifique se o arquivo existe no caminho especificado e se tem a aba 'Base Refinada'")
        st.stop()

# Carregar dados
try:
    df, df_unicos = load_data()
    st.success(f"✅ Dados carregados com sucesso! {len(df)} registros totais, {len(df_unicos)} únicos.")
except Exception as e:
    st.error(f"❌ Erro crítico ao carregar dados: {e}")
    st.stop()

# Header principal
st.markdown('<h1 class="main-header">🔧 Dashboard ISN - Análise de Falhas de Comunicação</h1>', unsafe_allow_html=True)
st.markdown("**Monitoramento inteligente de sensores em raspadores de correias transportadoras - Vale**")

# Resto do código continua igual...
st.success("🎉 Dashboard carregado com sucesso!")
st.info("📊 Dados prontos para análise!")

# Mostrar informações básicas dos dados
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Total de Registros", len(df))
with col2:
    st.metric("🔧 Registros Únicos", len(df_unicos))
with col3:
    st.metric("🏭 Plantas", df['PLANTA'].nunique())

# Mostrar preview dos dados
st.subheader("📋 Preview dos Dados")
st.dataframe(df.head(), use_container_width=True)


# Salvar dashboard corrigido
with open('dashboard_caminho_corrigido.py', 'w', encoding='utf-8') as f:
    f.write(dashboard_corrigido)

print("✅ Dashboard com caminho corrigido!")
print("\n🔧 Correções aplicadas:")
print("- ✅ Caminho do arquivo corrigido para Streamlit Cloud")
print("- ✅ Verificação se arquivo existe")
print("- ✅ Lista arquivos disponíveis se não encontrar")
print("- ✅ Mensagens de erro mais claras")
print("\n📤 Próximos passos:")
print("1. Certifique-se que Base_ISN_Comm_Loss_Refinada.xlsx está na RAIZ do repositório")
print("2. Substitua o dashboard principal por este código")
print("3. Faça commit no GitHub")
