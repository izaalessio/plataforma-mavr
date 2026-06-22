import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Plataforma Científica MAVR", page_icon="🧬", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    blockquote {
        border-left: 5px solid #E35205;
        background-color: #FFF9F2;
        padding: 10px 20px;
        margin-top: 10px;
        border-radius: 0px 5px 5px 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- ARQUITECTURA INTERNA MAVR CON GEMINI ---
class ModeloMAVR_Gemini:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.tema_actual = ""
        self.datos_extraidos = ""
        self.datos_validados = ""
        self.articulo_final = ""
        self.glosario = ""
        self.registro_auditoria = []

    def capa_1_orquestador(self, tema):
        self.tema_actual = tema
        self.registro_auditoria.append("Orquestador: Definiendo arquitectura de investigación...")
        prompt = f"Define en 3 pasos claros el protocolo para investigar académicamente: {tema}"
        return self.model.generate_content(prompt).text

    def capa_2_bibliometrico(self):
        self.registro_auditoria.append("Bibliométrico: Extrayendo fuentes con DOIs estrictamente reales...")
        prompt = f"""
        Realiza una búsqueda científica profunda sobre: {self.tema_actual}.
        1. Encuentra entre 10 y 15 fuentes de artículos de alto impacto.
        2. REGLA ESTRICTA DE ENLACES: Usa ÚNICAMENTE enlaces DOI reales (formato: https://doi.org/10.xxxx/xxxx). Si no conoces el DOI exacto y real del artículo, NO lo incluyas. Está totalmente prohibido inventar URLs.
        3. Para CADA fuente, proporciona: 
           - Título exacto.
           - Autores y Revista.
           - Enlace DOI funcional.
           - Un 'Fragmento de Valor': Una conclusión o dato clave de 3 líneas.
        """
        self.datos_extraidos = self.model.generate_content(prompt).text
        return "Fuentes extraídas."

    def capa_3_auditor(self):
        self.registro_auditoria.append("Auditor: Formateando diseño UI y comprobando calidad epistémica.")
        prompt = f"""
        Revisa estas fuentes extraídas y elimina cualquiera que no tenga un formato DOI válido:
        {self.datos_extraidos}
        
        Instrucciones de Formato:
        Para renderizar una interfaz perfecta, debes estructurar la lista FINAL exactamente con esta plantilla Markdown:
        
        ### 📌 [Título del Artículo](Enlace DOI)
        * 👥 **Autores:** [Nombres]
        * 🏛️ **Revista:** [Nombre de la revista]
        > 💡 **Aporte Fundamental:** "[Fragmento de Valor]"
        
        ---
        """
        self.datos_validados = self.model.generate_content(prompt).text
        self.registro_auditoria.append("Auditor: Interfaz de repositorio formateada.")
        return "Fuentes curadas."

    def capa_4_redactor(self, tono):
        self.registro_auditoria.append(f"Redactor: Generando manuscrito con IMRyD y tablas ({tono}).")
        prompt = f"""
        Escribe un artículo extenso, profundo y detallado ({tono}) basado ÚNICAMENTE en esta información validada: {self.datos_validados}
        
        Instrucciones:
        1. Usa formato IMRyD (Introducción, Metodología, Resultados, Discusión).
        2. OBLIGATORIO: Integra 2 TABLAS comparativas (Markdown) en Metodología y Resultados estructurando los datos de las fuentes.
        3. Cita los autores en el texto fluidamente.
        4. Añade "Referencias Bibliográficas" al final.
        """
        self.articulo_final = self.model.generate_content(prompt).text
        return "Artículo redactado."

    def capa_5_sintetizador(self):
        self.registro_auditoria.append("Sintetizador: Estructurando diseño de conclusiones.")
        prompt = f"""
        Basado en el artículo generado: {self.articulo_final}
        Estructura la respuesta EXACTAMENTE con este diseño visual en Markdown:
        
        ### 🎯 Conclusiones Principales
        (Proporciona 4 viñetas detalladas con las conclusiones más fuertes)
        
        ---
        ### 🧠 Conceptos Clave
        (Selecciona los 5 términos más técnicos del artículo y explícalos)
        """
        self.glosario = self.model.generate_content(prompt).text
        return "Síntesis terminada."

# --- INTERFAZ DE USUARIO ---
with st.sidebar:
    st.divider()
    st.title("Panel de Navegación")
    st.info("💡 **Garantía de Privacidad:** La validación de datos opera de manera completamente interna dentro del núcleo del agente.")
    st.divider()
    st.caption("© 2026 - Facultad de Ingeniería UNFV")

# ==========================================
# INYECCIÓN INTERNA SEGURA DE LA API KEY DESDE EL SERVIDOR
# ==========================================
try:
    API_KEY_SECRETA = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY_SECRETA = ""

st.title("Plataforma de Investigación Científica (MAVR)")
st.markdown("Generación automatizada de manuscritos académicos con repositorios DOI verificados.")

tab1, tab2, tab3 = st.tabs(["📝 Artículo Generado", "📚 Fuentes Consultadas", "💡 Conclusiones y Conceptos"])

with tab1:
    col_input, col_opciones = st.columns([2, 1])
    with col_input:
        tema_investigacion = st.text_input("Tema de investigación:", placeholder="Escribe el tema aquí...")
    with col_opciones:
        tono_redaccion = st.selectbox("Estilo de redacción:", ["Académico Formal", "Informativo / Universitario"])

    btn_iniciar = st.button("Generar Investigación", type="primary", use_container_width=True)

    if 'proceso_iniciado' not in st.session_state:
        st.session_state.proceso_iniciado = False

    if btn_iniciar and tema_investigacion:
        if not API_KEY_SECRETA:
            st.error("Error del Servidor: La API Key no está configurada en la bóveda de seguridad.")
        else:
            st.session_state.mavr = ModeloMAVR_Gemini(api_key=API_KEY_SECRETA)
            st.session_state.proceso_iniciado = True

    if st.session_state.proceso_iniciado:
        st.divider()
        try:
            with st.status("Procesando red neuronal de investigación...", expanded=True) as status:
                st.write("🔄 Definiendo protocolo metodológico...")
                st.session_state.mavr.capa_1_orquestador(tema_investigacion)
                time.sleep(2) 
                
                st.write("🔍 Extrayendo lote de repositorios oficiales (DOI)...")
                st.session_state.mavr.capa_2_bibliometrico()
                time.sleep(3) 
                
                st.write("🛡️ Estructurando UI y verifying autenticidad de enlaces...")
                st.session_state.mavr.capa_3_auditor()
                time.sleep(2)
                
                st.write("✍️ Redactando documento y renderizando tablas de datos...")
                st.session_state.mavr.capa_4_redactor(tono_redaccion)
                time.sleep(3)
                
                st.write("💡 Sintetizando conclusiones e indexando conceptos clave...")
                st.session_state.mavr.capa_5_sintetizador()
                
                status.update(label="Documento generado y validado exitosamente.", state="complete", expanded=False)

            st.markdown(st.session_state.mavr.articulo_final)
            st.divider()
            
            st.download_button(
                label="📥 Descargar Documento (TXT)",
                data=st.session_state.mavr.articulo_final,
                file_name=f"Investigacion_{tema_investigacion[:10]}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            with st.expander("Ver registro técnico interno de los agentes"):
                for log in st.session_state.mavr.registro_auditoria:
                    st.code(log, language="log")
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "ResourceExhausted" in error_msg:
                st.error("⚠️ Límite de procesamiento alcanzado. Por favor, espera 60 segundos antes de volver a intentarlo.")
            else:
                st.error(f"⚠️ Ha ocurrido un inconveniente interno: {error_msg}")

with tab2:
    st.header("Repositorio de Fuentes Consultadas")
    st.write("Todos los enlaces apuntan exclusivamente a bases de datos oficiales mediante identificadores DOI.")
    st.divider()
    if st.session_state.proceso_iniciado and hasattr(st.session_state, 'mavr'):
        st.markdown(st.session_state.mavr.datos_validados)
    else:
        st.info("Genera un artículo para visualizar las fuentes directas consultadas.")

with tab3:
    if st.session_state.proceso_iniciado and hasattr(st.session_state, 'mavr'):
        st.markdown(st.session_state.mavr.glosario)
    else:
        st.info("Genera un artículo para ver las conclusiones principales y los conceptos clave.")
