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
st.markdown('''
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
    /* Remover fundo branco dos containers do Streamlit */
    .stMarkdown > div {
        background-color: transparent !important;
    }
    /* Estilo para separadores sutis */
    .subtle-separator {
        height: 1px;
        background: linear-gradient(90deg, transparent, #d0d0d0, transparent);
        margin: 2rem 0;
    }
</style>
''', unsafe_allow_html=True)

# Caminho do arquivo
ARQUIVO_BASE = r"C:\Users\joaog\Downloads\Base_ISN_Comm_Loss_Refinada.xlsx"

@st.cache_data
def load_data():
    try:
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

# Sidebar - APENAS FILTROS BÁSICOS
with st.sidebar:
    st.header("🎛️ Filtros de Análise")

    plantas_disponiveis = sorted(df['PLANTA'].unique())
    plantas_selecionadas = st.multiselect(
        "🏭 Plantas:",
        options=plantas_disponiveis,
        default=plantas_disponiveis
    )

    tipos_sensor = sorted(df['TIPO_SENSOR'].unique())
    tipos_selecionados = st.multiselect(
        "🔧 Tipo de Sensor:",
        options=tipos_sensor,
        default=tipos_sensor
    )

    data_min = df['DATA ABERTURA'].min().date()
    data_max = df['DATA ABERTURA'].max().date()
    periodo_selecionado = st.date_input(
        "📅 Período de Análise:",
        value=[data_min, data_max],
        min_value=data_min,
        max_value=data_max
    )

    status_opcoes = ['Todos', 'Resolvidos', 'Não Resolvidos']
    status_selecionado = st.selectbox("📋 Status:", status_opcoes)

    min_alertas = st.slider("⚠️ Mínimo de alertas por sensor:", 0, 10, 0)

# Aplicar filtros
try:
    df_filtrado = df[
        (df['PLANTA'].isin(plantas_selecionadas)) &
        (df['TIPO_SENSOR'].isin(tipos_selecionados)) &
        (df['DATA ABERTURA'].dt.date >= periodo_selecionado[0]) &
        (df['DATA ABERTURA'].dt.date <= periodo_selecionado[1])
    ]

    df_unicos_filtrado = df_unicos[
        (df_unicos['PLANTA'].isin(plantas_selecionadas)) &
        (df_unicos['TIPO_SENSOR'].isin(tipos_selecionados)) &
        (df_unicos['DATA ABERTURA'].dt.date >= periodo_selecionado[0]) &
        (df_unicos['DATA ABERTURA'].dt.date <= periodo_selecionado[1])
    ]

    if status_selecionado == 'Resolvidos':
        df_unicos_filtrado = df_unicos_filtrado[df_unicos_filtrado['CHECK'].str.contains('Resolvido', case=False, na=False)]
    elif status_selecionado == 'Não Resolvidos':
        df_unicos_filtrado = df_unicos_filtrado[~df_unicos_filtrado['CHECK'].str.contains('Resolvido', case=False, na=False)]

except Exception as e:
    st.error(f"Erro ao aplicar filtros: {e}")
    st.stop()

# Cálculos
try:
    total_alertas_unicos = len(df_unicos_filtrado)
    alertas_pressao = len(df_unicos_filtrado[df_unicos_filtrado['TIPO_SENSOR'].str.contains('Pressão', case=False, na=False)])
    alertas_vida_util = len(df_unicos_filtrado[df_unicos_filtrado['TIPO_SENSOR'].str.contains('Vida', case=False, na=False)])

    equipamentos_unicos = df_unicos_filtrado.groupby(['PLANTA', 'base', 'equipment']).agg({
        'QTD_RESETS': 'max'
    }).reset_index()
    total_resets_correto = equipamentos_unicos['QTD_RESETS'].sum()
    total_equipamentos = equipamentos_unicos.shape[0]

    alertas_resolvidos = df_unicos_filtrado['CHECK'].str.contains('Resolvido', case=False, na=False).sum()
    taxa_resolucao = (alertas_resolvidos / total_alertas_unicos * 100) if total_alertas_unicos > 0 else 0

    analise_correlacao = df_unicos_filtrado.groupby(['PLANTA', 'base', 'equipment', 'TIPO_SENSOR']).agg({
        'event_type': 'count',
        'QTD_RESETS': 'max',
        'CHECK': lambda x: x.str.contains('Resolvido', case=False, na=False).sum(),
        'DATA ABERTURA': ['min', 'max']
    }).reset_index()

    analise_correlacao.columns = [
        'PLANTA', 'base', 'equipment', 'TIPO_SENSOR',
        'TOTAL_ALERTAS', 'QTD_RESETS', 'ALERTAS_RESOLVIDOS',
        'PRIMEIRO_ALERTA', 'ULTIMO_ALERTA'
    ]

    analise_correlacao['ALERTAS_PENDENTES'] = analise_correlacao['TOTAL_ALERTAS'] - analise_correlacao['ALERTAS_RESOLVIDOS']
    analise_correlacao['TAXA_RESOLUCAO_SENSOR'] = (analise_correlacao['ALERTAS_RESOLVIDOS'] / analise_correlacao['TOTAL_ALERTAS'] * 100).round(1)

    if min_alertas > 0:
        analise_correlacao = analise_correlacao[analise_correlacao['TOTAL_ALERTAS'] >= min_alertas]

    sensores_criticos_alertas = analise_correlacao[analise_correlacao['TOTAL_ALERTAS'] >= 3]
    qtd_criticos_alertas = len(sensores_criticos_alertas)
    percent_criticos_alertas = (qtd_criticos_alertas / total_equipamentos * 100) if total_equipamentos > 0 else 0

    sensores_criticos_resets = analise_correlacao[analise_correlacao['QTD_RESETS'] >= 2]
    qtd_criticos_resets = len(sensores_criticos_resets)
    percent_criticos_resets = (qtd_criticos_resets / total_equipamentos * 100) if total_equipamentos > 0 else 0

    media_eficacia = (
        analise_correlacao[analise_correlacao['QTD_RESETS'] > 0]['ALERTAS_RESOLVIDOS'].sum() /
        analise_correlacao[analise_correlacao['QTD_RESETS'] > 0]['QTD_RESETS'].sum()
        if analise_correlacao[analise_correlacao['QTD_RESETS'] > 0]['QTD_RESETS'].sum() > 0 else 0
    )

except Exception as e:
    st.error(f"Erro ao calcular indicadores: {e}")
    st.stop()

# === SEÇÃO 1: INDICADORES EXECUTIVOS ===
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Indicadores Executivos</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

with col1:
    st.metric("⚠️ Alertas Únicos Totais", total_alertas_unicos)
    st.metric("🟦 PS-Alerts (Pressão)", alertas_pressao)
    st.metric("🟧 BWS-Alerts (Vida Útil)", alertas_vida_util)

with col2:
    st.metric("🔄 Total de Resets", int(total_resets_correto))
    st.metric("⚙️ Equipamentos Únicos", total_equipamentos)

with col3:
    st.metric("✅ Taxa de Resolução", f"{taxa_resolucao:.1f}%", delta=f"{alertas_resolvidos} resolvidos")
    st.metric("🎯 Eficácia dos Resets", f"{media_eficacia:.2f}")

with col4:
    st.metric("🚨 Sensores Críticos (Alertas)", f"{qtd_criticos_alertas} ({percent_criticos_alertas:.1f}%)", delta="≥3 alertas", delta_color="inverse")
    st.metric("🔩 Sensores Críticos (Resets)", f"{qtd_criticos_resets} ({percent_criticos_resets:.1f}%)", delta="≥2 resets", delta_color="inverse")

# === SEÇÃO 2: ANÁLISE DETALHADA ===
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Análise Detalhada</div>', unsafe_allow_html=True)

# ========== SUBSEÇÃO 1: ANÁLISE DE RESETS ==========
st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
st.markdown('<h3 class="subsection-header">🔄 Análise de Resets por Equipamento</h3>', unsafe_allow_html=True)

mostrar_analise_resets = st.checkbox("📊 Exibir Análise de Resets", key="show_resets_analysis", value=True)

if mostrar_analise_resets:
    # Valores padrão para resets
    min_resets_padrao = 1
    max_itens_resets_padrao = 20

    # Preparar dados para o gráfico de resets
    try:
        dados_resets_grafico = analise_correlacao[analise_correlacao['QTD_RESETS'] >= min_resets_padrao].copy()
        dados_resets_grafico = dados_resets_grafico.sort_values('QTD_RESETS', ascending=False).head(max_itens_resets_padrao)

        if len(dados_resets_grafico) > 0:
            # Criar identificador curto para melhor visualização
            dados_resets_grafico['sensor_id_display'] = (
                dados_resets_grafico['PLANTA'].str[:3] + '-' +
                dados_resets_grafico['base'] + '-' + 
                dados_resets_grafico['equipment'].str[-8:]
            )

            # GRÁFICO DE RESETS
            st.markdown(f"#### 📊 Top {len(dados_resets_grafico)} Equipamentos com Mais Resets")

            fig_resets = px.bar(
                dados_resets_grafico,
                x='QTD_RESETS',
                y='sensor_id_display',
                orientation='h',
                color='TAXA_RESOLUCAO_SENSOR',
                color_continuous_scale='RdYlGn',
                title=f"Equipamentos Ordenados por Quantidade de Resets",
                height=max(500, len(dados_resets_grafico) * 25),
                hover_data={
                    'PLANTA': True,
                    'base': True,
                    'equipment': True,
                    'TIPO_SENSOR': True,
                    'TOTAL_ALERTAS': True,
                    'ALERTAS_RESOLVIDOS': True,
                    'TAXA_RESOLUCAO_SENSOR': ':.1f'
                }
            )

            fig_resets.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                font=dict(size=12),
                title_font_size=16,
                xaxis_title="Quantidade de Resets",
                yaxis_title="Equipamentos",
                coloraxis_colorbar_title="Taxa de Resolução (%)"
            )

            st.plotly_chart(fig_resets, use_container_width=True)

            # CONTROLES DINÂMICOS PARA RESETS
            st.markdown('<div class="dynamic-control">', unsafe_allow_html=True)
            st.markdown("#### 🎛️ Controles de Filtro - Resets")

            col_reset1, col_reset2 = st.columns(2)

            with col_reset1:
                min_resets_tabela = st.slider(
                    "🔄 Mínimo de resets:",
                    min_value=0,
                    max_value=10,
                    value=1,
                    step=1,
                    key="min_resets_table",
                    help="Equipamentos com pelo menos esta quantidade de resets"
                )

            with col_reset2:
                max_itens_resets = st.slider(
                    "📊 Máximo de equipamentos:",
                    min_value=10,
                    max_value=100,
                    value=30,
                    step=5,
                    key="max_items_resets_table",
                    help="Quantidade máxima de equipamentos na tabela"
                )

            st.markdown('</div>', unsafe_allow_html=True)

            # TABELA DETALHADA DE RESETS
            try:
                tabela_resets_filtrada = analise_correlacao[analise_correlacao['QTD_RESETS'] >= min_resets_tabela].copy()
                tabela_resets_filtrada = tabela_resets_filtrada.sort_values('QTD_RESETS', ascending=False).head(max_itens_resets)

                if len(tabela_resets_filtrada) > 0:
                    st.markdown(f"#### 📋 Tabela Detalhada - Resets (≥{min_resets_tabela} resets)")

                    # Formatar tabela para exibição
                    tabela_resets_display = tabela_resets_filtrada[[
                        'PLANTA', 'base', 'equipment', 'TIPO_SENSOR', 
                        'QTD_RESETS', 'TOTAL_ALERTAS', 'ALERTAS_RESOLVIDOS', 
                        'ALERTAS_PENDENTES', 'TAXA_RESOLUCAO_SENSOR'
                    ]].copy()

                    # Renomear colunas para melhor apresentação
                    tabela_resets_display.columns = [
                        'Planta', 'Base', 'Equipamento', 'Tipo Sensor',
                        'Resets', 'Total Alertas', 'Resolvidos', 
                        'Pendentes', 'Taxa Resolução (%)'
                    ]

                    st.dataframe(
                        tabela_resets_display, 
                        use_container_width=True, 
                        height=400,
                        column_config={
                            "Taxa Resolução (%)": st.column_config.ProgressColumn(
                                "Taxa Resolução (%)",
                                help="Percentual de alertas resolvidos",
                                min_value=0,
                                max_value=100,
                            ),
                        }
                    )

                    st.success(f"✅ Exibindo {len(tabela_resets_filtrada)} equipamentos com ≥{min_resets_tabela} resets")
                else:
                    st.warning(f"⚠️ Nenhum equipamento encontrado com ≥{min_resets_tabela} resets")

            except Exception as e:
                st.error(f"Erro na tabela de resets: {e}")
        else:
            st.warning("⚠️ Nenhum equipamento encontrado com resets no período selecionado")

    except Exception as e:
        st.error(f"Erro na análise de resets: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# Divisor visual sutil
st.markdown('<div class="subtle-separator"></div>', unsafe_allow_html=True)

# ========== SUBSEÇÃO 2: ANÁLISE DE ALERTAS ==========
st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
st.markdown('<h3 class="subsection-header">⚠️ Análise de Alertas por Equipamento</h3>', unsafe_allow_html=True)

mostrar_analise_alertas = st.checkbox("📊 Exibir Análise de Alertas", key="show_alerts_analysis", value=True)

if mostrar_analise_alertas:
    # Valores padrão para alertas
    min_alertas_padrao = 2
    max_itens_alertas_padrao = 20

    # Preparar dados para o gráfico de alertas
    try:
        dados_alertas_grafico = analise_correlacao[analise_correlacao['TOTAL_ALERTAS'] >= min_alertas_padrao].copy()
        dados_alertas_grafico = dados_alertas_grafico.sort_values('TOTAL_ALERTAS', ascending=False).head(max_itens_alertas_padrao)

        if len(dados_alertas_grafico) > 0:
            # Criar identificador curto para melhor visualização
            dados_alertas_grafico['sensor_id_display'] = (
                dados_alertas_grafico['PLANTA'].str[:3] + '-' +
                dados_alertas_grafico['base'] + '-' + 
                dados_alertas_grafico['equipment'].str[-8:]
            )

            # GRÁFICO DE ALERTAS
            st.markdown(f"#### 📊 Top {len(dados_alertas_grafico)} Equipamentos com Mais Alertas")

            fig_alertas = px.bar(
                dados_alertas_grafico,
                x='TOTAL_ALERTAS',
                y='sensor_id_display',
                orientation='h',
                color='QTD_RESETS',
                color_continuous_scale='Reds',
                title=f"Equipamentos Ordenados por Quantidade de Alertas",
                height=max(500, len(dados_alertas_grafico) * 25),
                hover_data={
                    'PLANTA': True,
                    'base': True,
                    'equipment': True,
                    'TIPO_SENSOR': True,
                    'QTD_RESETS': True,
                    'ALERTAS_RESOLVIDOS': True,
                    'TAXA_RESOLUCAO_SENSOR': ':.1f'
                }
            )

            fig_alertas.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                font=dict(size=12),
                title_font_size=16,
                xaxis_title="Quantidade de Alertas",
                yaxis_title="Equipamentos",
                coloraxis_colorbar_title="Quantidade de Resets"
            )

            st.plotly_chart(fig_alertas, use_container_width=True)

            # CONTROLES DINÂMICOS PARA ALERTAS
            st.markdown('<div class="dynamic-control">', unsafe_allow_html=True)
            st.markdown("#### 🎛️ Controles de Filtro - Alertas")

            col_alert1, col_alert2 = st.columns(2)

            with col_alert1:
                min_alertas_tabela = st.slider(
                    "⚠️ Mínimo de alertas:",
                    min_value=1,
                    max_value=15,
                    value=2,
                    step=1,
                    key="min_alerts_table",
                    help="Equipamentos com pelo menos esta quantidade de alertas"
                )

            with col_alert2:
                max_itens_alertas = st.slider(
                    "📊 Máximo de equipamentos:",
                    min_value=10,
                    max_value=100,
                    value=30,
                    step=5,
                    key="max_items_alerts_table",
                    help="Quantidade máxima de equipamentos na tabela"
                )

            st.markdown('</div>', unsafe_allow_html=True)

            # TABELA DETALHADA DE ALERTAS
            try:
                tabela_alertas_filtrada = analise_correlacao[analise_correlacao['TOTAL_ALERTAS'] >= min_alertas_tabela].copy()
                tabela_alertas_filtrada = tabela_alertas_filtrada.sort_values('TOTAL_ALERTAS', ascending=False).head(max_itens_alertas)

                if len(tabela_alertas_filtrada) > 0:
                    st.markdown(f"#### 📋 Tabela Detalhada - Alertas (≥{min_alertas_tabela} alertas)")

                    # Formatar tabela para exibição
                    tabela_alertas_display = tabela_alertas_filtrada[[
                        'PLANTA', 'base', 'equipment', 'TIPO_SENSOR', 
                        'TOTAL_ALERTAS', 'QTD_RESETS', 'ALERTAS_RESOLVIDOS', 
                        'ALERTAS_PENDENTES', 'TAXA_RESOLUCAO_SENSOR'
                    ]].copy()

                    # Renomear colunas para melhor apresentação
                    tabela_alertas_display.columns = [
                        'Planta', 'Base', 'Equipamento', 'Tipo Sensor',
                        'Total Alertas', 'Resets', 'Resolvidos', 
                        'Pendentes', 'Taxa Resolução (%)'
                    ]

                    st.dataframe(
                        tabela_alertas_display, 
                        use_container_width=True, 
                        height=400,
                        column_config={
                            "Taxa Resolução (%)": st.column_config.ProgressColumn(
                                "Taxa Resolução (%)",
                                help="Percentual de alertas resolvidos",
                                min_value=0,
                                max_value=100,
                            ),
                        }
                    )

                    st.success(f"✅ Exibindo {len(tabela_alertas_filtrada)} equipamentos com ≥{min_alertas_tabela} alertas")
                else:
                    st.warning(f"⚠️ Nenhum equipamento encontrado com ≥{min_alertas_tabela} alertas")

            except Exception as e:
                st.error(f"Erro na tabela de alertas: {e}")
        else:
            st.warning("⚠️ Nenhum equipamento encontrado com alertas no período selecionado")

    except Exception as e:
        st.error(f"Erro na análise de alertas: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# === SEÇÃO 3: RESUMO EXECUTIVO ===
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Resumo Executivo</div>', unsafe_allow_html=True)

col_resumo1, col_resumo2 = st.columns(2)

with col_resumo1:
    st.markdown("#### 🎯 Indicadores Principais")
    st.markdown(f'''
    - **{total_equipamentos}** equipamentos únicos monitorados
    - **{total_alertas_unicos}** alertas únicos registrados
    - **{int(total_resets_correto)}** resets realizados no período
    - **{taxa_resolucao:.1f}%** taxa geral de resolução
    ''')

with col_resumo2:
    st.markdown("#### ⚠️ Sensores Críticos")
    st.markdown(f'''
    - **{qtd_criticos_alertas}** sensores com ≥3 alertas ({percent_criticos_alertas:.1f}%)
    - **{qtd_criticos_resets}** sensores com ≥2 resets ({percent_criticos_resets:.1f}%)
    - **{media_eficacia:.2f}** alertas resolvidos por reset (eficácia)
    ''')

# Insights
st.markdown("#### 🔍 Insights Automáticos")

insights = []

if percent_criticos_resets > 20:
    insights.append("🚨 **Alto índice de sensores críticos por resets** - Mais de 20% dos equipamentos necessitaram múltiplos resets")

if media_eficacia < 1:
    insights.append("⚠️ **Baixa eficácia dos resets** - Cada reset resolve menos de 1 alerta em média")

if taxa_resolucao < 70:
    insights.append("📉 **Taxa de resolução abaixo do ideal** - Menos de 70% dos alertas foram resolvidos")

if alertas_pressao > alertas_vida_util * 2:
    insights.append("🔧 **Predominância de alertas de pressão** - Sensores de pressão geram mais alertas que vida útil")

if len(insights) == 0:
    insights.append("✅ **Situação controlada** - Indicadores dentro dos parâmetros esperados")

for insight in insights:
    st.markdown(f"- {insight}")

# Footer
st.markdown("---")
st.markdown('''
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
🔄 Martin Engineering & Vale | 2025 | ⚡ Powered by Streamlit & Plotly
</div>
''', unsafe_allow_html=True)
