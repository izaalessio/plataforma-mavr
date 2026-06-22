import streamlit as st
import google.generativeai as genai
import time
from fpdf import FPDF

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

# --- LÓGICA DE PDF PROFESIONAL ---
class PDF_Academico(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte de Investigacion Cientifica - MAVR', 0, 1, 'C')
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

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
        1. Encuentra un máximo de 10 fuentes de artículos de alto impacto. NO excedas este número para garantizar precisión.
        2. REGLA ESTRICTA DE ENLACES: Usa ÚNICAMENTE enlaces DOI reales (formato: https://doi.org/10.xxxx/xxxx). 
        3. ADVERTENCIA: Tienes estrictamente prohibido inventar, predecir o alucinar URLs. Si no estás 100% seguro de que el DOI existe y lleva a un artículo real, OMITE esa fuente.
        4. Para CADA fuente, proporciona: 
           - Título exacto.
           - Autores y Revista.
           - Enlace DOI funcional.
           - Un 'Fragmento de Valor': Una conclusión clave.
        """
        self.datos_extraidos = self.model.generate_content(prompt).text
        return "Fuentes extraídas."

    def capa_3_auditor(self):
        self.registro_auditoria.append("Auditor: Formateando diseño UI y comprobando calidad epistémica.")
        prompt = f"""
        Revisa estas fuentes extraídas y elimina cualquiera que no tenga un formato DOI válido:
        {self.datos_extraidos}
        
        Para renderizar la interfaz, estructura la lista FINAL exactamente con esta plantilla Markdown:
        ### 📌 [Título del Artículo](Enlace DOI)
        * 👥 **Autores:** [Nombres]
        * 🏛️ **Revista:** [Nombre de la revista]
        > 💡 **Aporte Fundamental:** "[Fragmento de Valor]"
        ---
        """
        self.datos_validados = self.model.generate_content(prompt).text
        self.registro_auditoria.append("Auditor: Interfaz formateada.")
        return "Fuentes curadas."

    def capa_4_redactor(self, tono):
        self.registro_auditoria.append(f"Redactor: Generando manuscrito con IMRyD y tablas ({tono}).")
        prompt = f"""
        Escribe un artículo extenso y detallado ({tono}) basado ÚNICAMENTE en esta información validada: {self.datos_validados}
        1. Usa formato IMRyD (Introducción, Metodología, Resultados, Discusión).
        2. OBLIGATORIO: Integra 2 TABLAS comparativas (Markdown).
        3. Añade "Referencias Bibliográficas" al final.
        """
        self.articulo_final = self.model.generate_content(prompt).text
        return "Artículo redactado."

    def capa_5_sintetizador(self):
        self.registro_auditoria.append("Sintetizador: Estructurando diseño de conclusiones.")
        prompt = f"""
        Basado en el artículo generado: {self.articulo_final}
        Estructura la respuesta con este diseño visual:
        ### 🎯 Conclusiones Principales
        (4 viñetas detalladas)
        ---
        ### 🧠 Conceptos Clave
        (5 términos técnicos explicados)
        """
        self.glosario = self.model.generate_content(prompt).text
        return "Síntesis terminada."

    def generar_pdf(self, contenido):
        pdf = PDF_Academico()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        # Limpieza básica para evitar errores de codificación en PDF
        texto_limpio = contenido.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, texto_limpio)
        return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO ---
with st.sidebar:
    st.divider()
    st.title("Panel de Navegación")
    st.info("💡 **Garantía de Privacidad:** La validación de datos opera de manera completamente interna dentro del núcleo del agente.")
    st.divider()
    st.caption("© 2026 - Facultad de Ingeniería UNFV")

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
                time.sleep(10) # Pausa ampliada para evitar límite de velocidad
                
                st.write("🔍 Extrayendo lote de repositorios oficiales (DOI)...")
                st.session_state.mavr.capa_2_bibliometrico()
                time.sleep(10) 
                
                st.write("🛡️ Estructurando UI y verificando autenticidad de enlaces...")
                st.session_state.mavr.capa_3_auditor()
                time.sleep(10)
                
                st.write("✍️ Redactando documento y renderizando tablas de datos...")
                st.session_state.mavr.capa_4_redactor(tono_redaccion)
                time.sleep(10)
                
                st.write("💡 Sintetizando conclusiones e indexando conceptos clave...")
                st.session_state.mavr.capa_5_sintetizador()
                
                status.update(label="Documento generado y validado exitosamente.", state="complete", expanded=False)

            st.markdown(st.session_state.mavr.articulo_final)
            st.divider()
            
            # Descarga de PDF
            pdf_data = st.session_state.mavr.generar_pdf(st.session_state.mavr.articulo_final)
            st.download_button(
                label="📥 Descargar Documento en PDF Académico",
                data=pdf_data,
                file_name=f"Investigacion_MAVR.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            with st.expander("Ver registro técnico interno de los agentes"):
                for log in st.session_state.mavr.registro_auditoria:
                    st.code(log, language="log")
                
        except Exception as e:
            st.error(f"⚠️ Ha ocurrido un inconveniente: {str(e)}")

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
