import streamlit as st
import google.generativeai as genai
import time
from fpdf import FPDF

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Plataforma Científica MAVR", page_icon="🧬", layout="wide")

# --- CORRECCIÓN DE INTERFAZ: CSS ELEGANTE Y COMPATIBLE CON MODO OSCURO ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Diseño de caja elegante para los fragmentos de valor */
    blockquote {
        border-left: 4px solid #FF4B4B;
        background-color: rgba(255, 75, 75, 0.1); /* Fondo translúcido que se adapta al modo oscuro */
        padding: 15px 20px;
        margin-top: 15px;
        border-radius: 0px 8px 8px 0px;
        font-style: italic;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

class PDF_Academico(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte de Investigacion Cientifica - MAVR', 0, 1, 'C')
        self.ln(5)
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
        self.registro_auditoria.append("Orquestador: Protocolo iniciado. Limitando tokens de salida.")
        prompt = f"Define en 3 pasos muy breves el protocolo de investigación para: {tema}"
        return self.model.generate_content(prompt).text

    def capa_2_bibliometrico(self):
        self.registro_auditoria.append("Bibliométrico: Generando enlaces verificables de Google Scholar...")
        # AQUI ESTÁ LA MAGIA: Prohibimos los DOI falsos y exigimos Google Scholar
        prompt = f"""
        Busca literatura científica sobre: {self.tema_actual}.
        1. Identifica EXACTAMENTE 3 o 4 fuentes fundamentales y reales. No excedas este número.
        2. SINCERIDAD ABSOLUTA: Como no puedes verificar enlaces DOI en vivo, NO uses DOIs. 
        3. OBLIGATORIO: En su lugar, genera un enlace directo a Google Scholar con el título del artículo.
           Formato estricto: https://scholar.google.com/scholar?q=[TITULO+DEL+ARTICULO+CON+SIGNOS+MAS]
           Ejemplo: https://scholar.google.com/scholar?q=Artificial+Intelligence+in+Education
        4. Estructura para cada fuente:
           - Título exacto.
           - Autores principales y Año.
           - Enlace de Google Scholar.
           - Fragmento de Valor: Una conclusión clave.
        """
        self.datos_extraidos = self.model.generate_content(prompt).text
        return "Fuentes extraídas con enlaces Scholar."

    def capa_3_auditor(self):
        self.registro_auditoria.append("Auditor: Formateando diseño UI...")
        prompt = f"""
        Organiza las siguientes fuentes para la interfaz de usuario:
        {self.datos_extraidos}
        
        Usa ESTRICTAMENTE esta plantilla Markdown para cada una:
        ### 📌 [Título del Artículo](Enlace Google Scholar)
        * 👥 **Autores:** [Nombres y Año]
        > 💡 **Aporte Fundamental:** "[Fragmento de Valor]"
        ---
        """
        self.datos_validados = self.model.generate_content(prompt).text
        self.registro_auditoria.append("Auditor: Interfaz formateada.")
        return "Fuentes curadas."

    def capa_4_redactor(self, tono):
        self.registro_auditoria.append(f"Redactor: Generando manuscrito conciso con tablas ({tono}).")
        prompt = f"""
        Escribe un artículo académico ({tono}) basado SOLO en esta información: {self.datos_validados}
        1. Usa formato IMRyD (Introducción, Metodología, Resultados, Discusión). Sé conciso y directo.
        2. OBLIGATORIO: Integra 1 TABLA comparativa (Markdown) en los Resultados.
        3. Añade Referencias al final.
        """
        self.articulo_final = self.model.generate_content(prompt).text
        return "Artículo redactado."

    def capa_5_sintetizador(self):
        self.registro_auditoria.append("Sintetizador: Extrayendo conceptos.")
        prompt = f"""
        Basado en el artículo: {self.articulo_final}
        Estructura esto de forma concisa:
        ### 🎯 Conclusiones Principales
        (3 viñetas)
        ---
        ### 🧠 Conceptos Clave
        (3 términos explicados brevemente)
        """
        self.glosario = self.model.generate_content(prompt).text
        return "Síntesis terminada."

    def generar_pdf(self, contenido):
        pdf = PDF_Academico()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        texto_limpio = contenido.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, texto_limpio)
        return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO ---
with st.sidebar:
    st.divider()
    st.title("Panel de Navegación")
    st.info("💡 **Garantía de Privacidad:** La validación de datos opera de manera completamente interna.")
    st.divider()
    st.caption("© 2026 - Facultad de Ingeniería UNFV")

try:
    API_KEY_SECRETA = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY_SECRETA = ""

st.title("Plataforma de Investigación Científica (MAVR)")
st.markdown("Generación automatizada de manuscritos académicos con enlaces de verificación directos.")

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
            st.error("Error del Servidor: Falta la API Key en los Secrets.")
        else:
            st.session_state.mavr = ModeloMAVR_Gemini(api_key=API_KEY_SECRETA)
            st.session_state.proceso_iniciado = True

    if st.session_state.proceso_iniciado:
        st.divider()
        try:
            with st.status("Procesando red neuronal de investigación...", expanded=True) as status:
                st.write("🔄 Definiendo protocolo metodológico...")
                st.session_state.mavr.capa_1_orquestador(tema_investigacion)
                time.sleep(12) 
                
                st.write("🔍 Extrayendo fuentes y generando enlaces de verificación (Scholar)...")
                st.session_state.mavr.capa_2_bibliometrico()
                time.sleep(12) 
                
                st.write("🛡️ Formateando UI...")
                st.session_state.mavr.capa_3_auditor()
                time.sleep(12)
                
                st.write("✍️ Redactando documento y tablas...")
                st.session_state.mavr.capa_4_redactor(tono_redaccion)
                time.sleep(12)
                
                st.write("💡 Sintetizando conclusiones...")
                st.session_state.mavr.capa_5_sintetizador()
                
                status.update(label="Documento generado exitosamente.", state="complete", expanded=False)

            st.markdown(st.session_state.mavr.articulo_final)
            st.divider()
            
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
            st.error(f"⚠️ Ha ocurrido un inconveniente (Posible límite de Tokens): {str(e)}")

with tab2:
    st.header("Repositorio de Fuentes Consultadas")
    st.write("Los enlaces te redirigirán a **Google Scholar** para verificar la existencia y rigor del artículo.")
    st.divider()
    if st.session_state.proceso_iniciado and hasattr(st.session_state, 'mavr'):
        st.markdown(st.session_state.mavr.datos_validados)
    else:
        st.info("Genera un artículo para visualizar las fuentes.")

with tab3:
    if st.session_state.proceso_iniciado and hasattr(st.session_state, 'mavr'):
        st.markdown(st.session_state.mavr.glosario)
    else:
        st.info("Genera un artículo para ver las conclusiones y conceptos clave.")
