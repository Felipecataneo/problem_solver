import streamlit as st
import google.generativeai as genai
from typing import Dict, List
import json

# Configuração da página

st.set_page_config(
page_title=“Problem Solver AI”,
page_icon=“🔍”,
layout=“wide”
)

# Mapeamento de objetivos e métodos

PROBLEM_METHODS = {
“Encontrar causas raiz”: {
“methods”: [“Issue Tree”, “Fishbone Diagram”, “5 Whys”],
“description”: “Identifica as causas fundamentais de um problema através de análise estruturada”
},
“Brainstorm criativo”: {
“methods”: [“Mind Map clássico”, “Spider Map”, “6-3-5 Brainwriting”],
“description”: “Gera ideias criativas e inovadoras através de técnicas de brainstorming”
},
“Analisar relações complexas”: {
“methods”: [“Concept Map”, “Argument Map”],
“description”: “Mapeia e analisa relacionamentos complexos entre conceitos e argumentos”
},
“Planejar soluções passo a passo”: {
“methods”: [“Fluxograma”, “Mapa de Processo”],
“description”: “Estrutura um plano de ação detalhado com etapas sequenciais”
},
“Estratégia/Visão geral”: {
“methods”: [“SWOT em Mapa Mental”],
“description”: “Desenvolve estratégias através de análise estruturada de forças, fraquezas, oportunidades e ameaças”
},
“Abordar problemas vagos/complexos”: {
“methods”: [“Design Thinking”],
“description”: “Aborda problemas mal-definidos através de processo centrado no usuário”
}
}

def configure_gemini(api_key: str):
“”“Configura o Gemini com a API key fornecida”””
try:
genai.configure(api_key=api_key)
return genai.GenerativeModel(‘gemini-pro’)
except Exception as e:
st.error(f”Erro ao configurar Gemini: {str(e)}”)
return None

def classify_problem(model, problem_description: str) -> str:
“”“Classifica o problema e retorna o objetivo mais adequado”””
objectives = list(PROBLEM_METHODS.keys())

```
prompt = f"""
Analise o seguinte problema e determine qual objetivo se adequa melhor:

Problema: {problem_description}

Objetivos disponíveis:
{chr(10).join([f"- {obj}" for obj in objectives])}

Responda apenas com o nome exato do objetivo mais adequado da lista acima.
"""

try:
    response = model.generate_content(prompt)
    classification = response.text.strip()
   
    # Verifica se a resposta está na lista de objetivos
    if classification in objectives:
        return classification
    else:
        # Se não encontrou correspondência exata, tenta encontrar a mais similar
        for obj in objectives:
            if obj.lower() in classification.lower() or classification.lower() in obj.lower():
                return obj
        return "Abordar problemas vagos/complexos"  # Default
except Exception as e:
    st.error(f"Erro na classificação: {str(e)}")
    return "Abordar problemas vagos/complexos"
```

def generate_approach(model, problem_description: str, objective: str, methods: List[str]) -> str:
“”“Gera abordagem detalhada usando os métodos recomendados”””

```
prompt = f"""
Você é um consultor especialista em resolução de problemas e metodologias estruturadas. Analise o problema abaixo e crie uma abordagem completa e prática.

PROBLEMA: {problem_description}

OBJETIVO: {objective}

MÉTODOS RECOMENDADOS: {', '.join(methods)}

Crie uma resposta estruturada e detalhada seguindo EXATAMENTE este formato:

## 🎯 Análise do Problema
[Análise detalhada do problema, identificando elementos-chave, stakeholders envolvidos e complexidade]

## 🔧 Abordagem Detalhada dos Métodos

### {methods[0]}
**O que é:** [Definição clara do método]
**Como aplicar:** [Passo a passo específico para este problema]
**Ferramentas necessárias:** [Materiais/recursos necessários]
**Tempo estimado:** [Duração aproximada]

### {methods[1] if len(methods) > 1 else "Método Complementar"}
**O que é:** [Definição clara do método]
**Como aplicar:** [Passo a passo específico para este problema]
**Ferramentas necessárias:** [Materiais/recursos necessários]
**Tempo estimado:** [Duração aproximada]

{f'''### {methods[2]}
**O que é:** [Definição clara do método]
**Como aplicar:** [Passo a passo específico para este problema]
**Ferramentas necessárias:** [Materiais/recursos necessários]
**Tempo estimado:** [Duração aproximada]''' if len(methods) > 2 else ""}

## 📊 Aplicação Prática dos Métodos

### Resultado da Aplicação do {methods[0]}
[Demonstre como seria o resultado concreto aplicando este método ao problema específico. Inclua exemplos práticos, diagramas textuais, listas, estruturas que surgiriam da aplicação]

### Resultado da Aplicação do {methods[1] if len(methods) > 1 else "Método Complementar"}
[Demonstre como seria o resultado concreto aplicando este método ao problema específico. Inclua exemplos práticos, diagramas textuais, listas, estruturas que surgiriam da aplicação]

{f'''### Resultado da Aplicação do {methods[2]}
[Demonstre como seria o resultado concreto aplicando este método ao problema específico. Inclua exemplos práticos, diagramas textuais, listas, estruturas que surgiriam da aplicação]''' if len(methods) > 2 else ""}

## 🚀 Plano de Implementação

**Fase 1:** [Primeira etapa com métodos específicos]
**Fase 2:** [Segunda etapa com métodos específicos]
**Fase 3:** [Terceira etapa com métodos específicos]

## 📋 Checklist de Execução
- [ ] [Item específico 1]
- [ ] [Item específico 2]
- [ ] [Item específico 3]
- [ ] [Item específico 4]
- [ ] [Item específico 5]

## 💡 Insights e Dicas Avançadas
[Dicas práticas, armadilhas a evitar, como maximizar efetividade]

## 🎯 Indicadores de Sucesso
[Como medir se a aplicação dos métodos está funcionando]

INSTRUÇÕES ESPECÍFICAS:
- Para cada método, forneça exemplos concretos aplicados ao problema
- Na seção "Aplicação Prática", mostre resultados reais que surgiriam (listas, diagramas, estruturas)
- Seja específico e detalhado, evite generalidades
- Use exemplos práticos e contextualizados
- Forneça templates ou estruturas quando apropriado
"""

try:
    response = model.generate_content(prompt)
    return response.text
except Exception as e:
    return f"Erro ao gerar abordagem: {str(e)}"
```

def main():
st.title(“🔍 Problem Solver AI”)
st.markdown(“Encontre a melhor abordagem para resolver seu problema usando métodos estruturados”)

```
# Sidebar para configuração
with st.sidebar:
    st.header("⚙️ Configuração")
   
    # Input para API key
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        help="Insira sua API key do Google Gemini"
    )
   
    if api_key:
        st.success("API Key configurada!")
       
    st.markdown("---")
   
    # Informações sobre métodos
    st.header("📚 Métodos Disponíveis")
    for objective, info in PROBLEM_METHODS.items():
        with st.expander(f"🎯 {objective}"):
            st.write(f"**Métodos:** {', '.join(info['methods'])}")
            st.write(f"**Descrição:** {info['description']}")

# Área principal
if not api_key:
    st.warning("⚠️ Por favor, insira sua API key do Gemini na sidebar para começar.")
    st.markdown("""
    ### Como obter sua API key:
    1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
    2. Faça login com sua conta Google
    3. Clique em "Create API Key"
    4. Copie e cole a key na sidebar
    """)
    return

# Configurar modelo
model = configure_gemini(api_key)
if not model:
    return

# Input do problema
st.header("🔍 Descreva seu Problema")

# Adicionar exemplos
with st.expander("💡 Exemplos de Problemas"):
    st.markdown("""
    **Encontrar causas raiz:**
    - "Nossa equipe tem alta rotatividade de funcionários"
    - "O sistema apresenta falhas constantes"
   
    **Brainstorm criativo:**
    - "Precisamos de ideias inovadoras para nosso produto"
    - "Como melhorar a experiência do cliente?"
   
    **Analisar relações complexas:**
    - "Entender a relação entre diferentes departamentos"
    - "Mapear argumentos sobre uma decisão estratégica"
   
    **Planejar soluções:**
    - "Implementar um novo sistema de gestão"
    - "Organizar um evento corporativo"
   
    **Estratégia/Visão geral:**
    - "Definir estratégia de entrada em novo mercado"
    - "Análise competitiva do setor"
   
    **Problemas vagos/complexos:**
    - "Nossos clientes não estão satisfeitos"
    - "Precisamos inovar mas não sabemos como"
    """)

problem_description = st.text_area(
    "Problema:",
    placeholder="Descreva detalhadamente o problema que você está enfrentando. Inclua contexto, stakeholders envolvidos, restrições e objetivos esperados...",
    height=150
)

if st.button("🚀 Analisar Problema", type="primary"):
    if not problem_description.strip():
        st.warning("Por favor, descreva o problema antes de continuar.")
        return
   
    with st.spinner("Analisando problema e gerando abordagem..."):
        # Classificar problema
        objective = classify_problem(model, problem_description)
       
        # Obter métodos recomendados
        methods_info = PROBLEM_METHODS[objective]
        methods = methods_info["methods"]
       
        # Gerar abordagem
        approach = generate_approach(model, problem_description, objective, methods)
   
    # Mostrar resultados
    st.markdown("### 🎯 Resultado da Análise")
   
    # Mostrar objetivo identificado
    st.success(f"**Objetivo Identificado:** {objective}")
    st.info(f"**Métodos Recomendados:** {', '.join(methods)}")
   
    # Criar abas para organizar o conteúdo
    tab1, tab2, tab3 = st.tabs(["📋 Abordagem Completa", "🔧 Métodos Detalhados", "📊 Resultados Práticos"])
   
    with tab1:
        st.markdown(approach)
   
    with tab2:
        st.markdown("### 🔧 Resumo dos Métodos")
        for i, method in enumerate(methods, 1):
            st.markdown(f"**{i}. {method}**")
            st.markdown(f"*{methods_info['description']}*")
            st.markdown("---")
   
    with tab3:
        st.markdown("### 📊 Aplicação Prática")
        st.markdown("*Esta seção contém os resultados concretos da aplicação dos métodos recomendados, conforme detalhado na aba 'Abordagem Completa'.*")
        st.markdown("**Principais benefícios:**")
        st.markdown("• Resultados tangíveis e aplicáveis")
        st.markdown("• Estruturas práticas para implementação")
        st.markdown("• Exemplos contextualizados ao seu problema")
        st.markdown("• Templates e checklists prontos para uso")

# Footer
st.markdown("---")
st.markdown(
    "💡 **Dica:** Seja específico na descrição do problema para obter melhores recomendações!"
)
```

if **name** == “**main**”:
main()
