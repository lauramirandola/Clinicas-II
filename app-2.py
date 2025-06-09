# %%
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Aplica o estilo global para mudar a cor da letra para preto
st.markdown("""
    <style>
        body, div, p, span, h1, h2, h3, h4, h5, h6 {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)


dados = pd.read_csv('teste_dashboard.csv')
df_completo = pd.read_csv('df_completo.csv')

# Configurações do Streamlit
st.title('Analises casos do CADE')
st.sidebar.header('Filtros')

# Sidebar com filtros
anos = sorted(dados['ano_documento'].dropna().unique())
faixas = sorted(dados['faixa_multa'].dropna().unique())
setores = sorted(dados['setor_categoria'].dropna().unique())

anos_selecionados = st.sidebar.multiselect("Ano do documento", anos, default=anos)
faixas_selecionadas = st.sidebar.multiselect("Faixa de multa", faixas, default=faixas)
setores_selecionados = st.sidebar.multiselect("Setor econômico", setores, default=setores)

# Aplicação dos filtros
df_filtrado = dados[
    dados['ano_documento'].isin(anos_selecionados) &
    dados['faixa_multa'].isin(faixas_selecionadas) &
    dados['setor_categoria'].isin(setores_selecionados)
]

# Função para atualizar layout do gráfico
def aplicar_layout_preto(fig):
    fig.update_layout(
        font=dict(color='black'),
        title_font=dict(color='black'),
        xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black'))
    )
    return fig

# Gráfico 1: Valor médio da multa por ano
st.subheader("Tendência do valor médio das multas (R$) por ano")
graf1 = df_filtrado.groupby("ano_documento")["valor_em_reais_x"].mean().reset_index()
fig1 = px.line(graf1, x="ano_documento", y="valor_em_reais_x", markers=True)
st.plotly_chart(aplicar_layout_preto(fig1))

# Gráfico 2: Percentual médio da multa por ano
st.subheader("Multa média como % do faturamento por ano")
graf2 = df_filtrado.groupby("ano_documento")["percentual_faturamento_x"].mean().reset_index()
fig2 = px.line(graf2, x="ano_documento", y="percentual_faturamento_x", markers=True)
st.plotly_chart(aplicar_layout_preto(fig2))

# Gráfico 3: Multa média por faixa
st.subheader("Valor médio da multa por faixa de severidade")
# Legenda explicativa
st.markdown("""
**Legenda das faixas de severidade:**
- Leve: percentual da multa < 5%
- Moderada: entre 5% e 10%
- Grave: acima de 10%
""")
graf3 = df_filtrado.groupby("faixa_multa")["valor_em_reais_x"].mean().reset_index()
fig3 = px.bar(graf3, x="faixa_multa", y="valor_em_reais_x", text_auto=True)
st.plotly_chart(aplicar_layout_preto(fig3))


# Gráfico 4: Duração média por decisão (completo)
st.subheader("Duração média dos processos por tipo de decisão")
# Filtra apenas anos selecionados e remove valores vazios ou com listas vazias
df_decisao = df_completo[df_completo['ano_documento'].isin(anos_selecionados)].copy()
df_decisao['decisao_tribunal'] = df_decisao['decisao_tribunal'].astype(str)
df_decisao = df_decisao[~df_decisao['decisao_tribunal'].isin(["['']", '[]', '', 'nan'])]
# Gera o gráfico
graf4 = df_decisao.groupby("decisao_tribunal")["duracao_dias_completo"].mean().reset_index()
fig4 = px.bar(graf4, x="decisao_tribunal", y="duracao_dias_completo", text_auto=True)
st.plotly_chart(aplicar_layout_preto(fig4))


# Gráfico 5: Multa média por setor
st.subheader("Multa média por setor econômico")
graf5 = df_filtrado.groupby("setor_categoria")["valor_em_reais_x"].mean().reset_index()
fig5 = px.bar(graf5, x="setor_categoria", y="valor_em_reais_x", text_auto=True)
fig5.update_layout(xaxis_tickangle=-45)
st.plotly_chart(aplicar_layout_preto(fig5))

# Tabela final
st.subheader("Tabela com dados filtrados")
st.dataframe(df_filtrado[['ano_documento', 'valor_em_reais_x', 'percentual_faturamento_x',
                          'faixa_multa', 'duracao_dias']])

# Contagem
st.write("Quantidade de registros filtrados:", len(df_filtrado))










# Configurações ajustáveis pelo usuário
#num_tentativas_por_mes = st.sidebar.slider('Número de tentativas por mês', min_value=1, max_value=50, value=30)
#orcamento = st.sidebar.slider('Orçamento disponível para acordos', min_value=1e5, max_value = 6e6, value=2e6, step=1e5)
#alcada = st.sidebar.slider('Alçada para a estratégia de acordo', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
#p_minima = st.sidebar.slider('Probabilidade mínima de derrota', min_value=0.1, max_value=0.9, value=0.5, step=0.1)
#n_simulacoes = st.sidebar.slider('Número de simulações', min_value=100, max_value=1000, value=100, step=100)



# Simulação de processos
#np.random.seed(42)
#n_processos = 300
#valores_causa = np.random.uniform(5000, 80000, n_processos)
#prob_derrota = np.random.uniform(0.1, 0.9, n_processos)
#tempos_esperados = np.random.uniform(1, 5, n_processos) * 12  # Convertendo anos para meses
#max_meses = 60  # Definindo o número máximo de meses

# Função para calcular a probabilidade de sucesso do acordo
#def probabilidade_acordo(alcada):
    #return 1 / (1 + np.exp(10 - 15 * alcada))

# Função para simular uma estratégia mês a mês
#def simular_estrategia(alcada, num_tentativas_por_mes, orcamento, max_meses):
    #gastos_acumulados = np.zeros(max_meses)  # Inicializa array de gastos acumulados com tamanho fixo
    #total_gastos = 0
    #processos_por_tentar = np.argsort(-prob_derrota)  # Ordena por maior probabilidade de derrota
    #tempos_restantes = tempos_esperados.copy()  # Copia os tempos esperados para atualizar
    #finalizados = np.zeros(n_processos, dtype=bool)  # Para marcar processos finalizados
    #perdido = np.random.rand(n_processos) < prob_derrota  # Processos perdidos

    #for mes in range(1, max_meses + 1):
        #tentativas = 0

        # Finalizar processos cujo tempo já passou
       # for processo in range(n_processos):
        #    if tempos_restantes[processo] <= mes and not finalizados[processo]:
         #       if perdido[processo]:
          #          total_gastos += valores_causa[processo]
           #     finalizados[processo] = True

        # Tentativas de acordo em processos que ainda não foram finalizados
       # for processo in processos_por_tentar:
        #    if tentativas >= num_tentativas_por_mes or total_gastos >= orcamento:
         #       break  # Limita o número de tentativas e o orçamento

          #  if prob_derrota[processo] > p_minima and tempos_restantes[processo] > mes and not finalizados[processo]:
           #     valor_acordo = valores_causa[processo] * alcada
            #    sucesso = np.random.rand() < probabilidade_acordo(alcada)
             #   tentativas += 1
              #  if sucesso and total_gastos + valor_acordo <= orcamento:
               #     total_gastos += valor_acordo
                #    finalizados[processo] = True  # O processo é encerrado

       # gastos_acumulados[mes-1] = total_gastos

   #return gastos_acumulados

# Simulação de cenários para 100 simulações mês a mês
#def simular_varios_cenarios(num_simulacoes, alcada, num_tentativas_por_mes, orcamento, max_meses):
 #   resultados = []
  #  for _ in range(num_simulacoes):
   #     gastos_acumulados = simular_estrategia(alcada, num_tentativas_por_mes, orcamento, max_meses)
    #    resultados.append(gastos_acumulados)
    #return np.mean(resultados, axis=0)


# Executando simulações
#np.random.seed(42)
#gastos_com_acordo = simular_varios_cenarios(n_simulacoes, alcada, num_tentativas_por_mes, orcamento, max_meses)
#np.random.seed(42)
#gastos_sem_acordo = simular_varios_cenarios(n_simulacoes, 0.0, num_tentativas_por_mes, orcamento, max_meses)


# %%

# Gráficos
#st.subheader('Gastos acumulados ao longo do tempo')
#plt.figure(figsize=(10, 6))
#plt.plot(gastos_com_acordo, label='Com Acordo', color='blue')
#plt.plot(gastos_sem_acordo, label='Sem Acordo', color='green')
#plt.xlabel('Tempo (meses)')
#plt.ylabel('Gastos Acumulados')
#plt.legend()
#st.pyplot(plt)

#st.subheader('Lucro: Diferença (Sem Acordo - Com Acordo)')
#plt.figure(figsize=(10, 6))
#plt.plot(gastos_sem_acordo - gastos_com_acordo, label='Diferença de Gastos', color='blue')
#plt.xlabel('Tempo (meses)')
#plt.ylabel('Sem Acordo - Com Acordo')
#plt.hlines(0, 0, max_meses, color='red', linestyle='--')
#plt.legend()
#st.pyplot(plt)