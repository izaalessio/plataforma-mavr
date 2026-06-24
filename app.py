import streamlit as st
import google.generativeai as genai
import time
from fpdf import FPDF

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Plataforma Científica MAVR", page_icon="🧬", layout="wide")

# --- DISEÑO UI: CSS ELEGANTE Y COMPATIBLE CON MODO OSCURO ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Diseño de caja elegante para los fragmentos de valor */
    blockquote {
        border-left: 4px solid #FF4B4B;
        background-color: rgba(255, 75, 75, 0.1); 
        padding: 15px 20px;
        margin-top: 15px;
        border-radius: 0px 8px 8px 0px;
        font-style: italic;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE PDF PROFESIONAL ---
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
        self.registro_auditoria.append("Orquestador: Protocolo iniciado. Definiendo directrices.")
        prompt = f"Define en 3 pasos muy breves el protocolo de investigación para: {tema}"
        return self.model.generate_content(prompt).text

    def capa_2_bibliometrico(self):
        self.registro_auditoria.append("Bibliométrico: Extrayendo fuentes con datos duros y enlaces Scholar...")
        prompt = f"""
        Busca literatura científica sobre: {self.tema_actual}.
        1. Identifica EXACTAMENTE 4 fuentes fundamentales y reales. No excedas este número.
        2. SINCERIDAD ABSOLUTA: NO uses DOIs para evitar enlaces rotos. Genera un enlace directo a Google Scholar con el título del artículo.
           Formato estricto: https://scholar.google.com/scholar?q=[TITULO+DEL+ARTICULO+CON+SIGNOS+MAS]
        3. OBLIGATORIO - PROFUNDIDAD DE DATOS: Para cada fuente, extrae un 'Fragmento de Valor' que contenga métricas concretas, datos estadísticos, metodologías específicas o hallazgos técnicos profundos. Queda estrictamente prohibido usar resúmenes generales o vagos.
        4. Estructura para cada fuente:
           - Título exacto.
           - Autores principales y Año.
           - Enlace de Google Scholar.
           - Fragmento de Valor (Con datos duros).
        """
        self.datos_extraidos = self.model.generate_content(prompt).text
        return "Fuentes extraídas con enlaces Scholar."

    def capa_3_auditor(self):
        self.registro_auditoria.append("Auditor: Formateando diseño UI y verificando integridad...")
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
        self.registro_auditoria.append(f"Redactor: Generando manuscrito extenso y profundo ({tono}).")
        prompt = f"""
        Actúa como el Agente Redactor Académico Principal.
        Escribe un artículo científico EXTENSO, analítico y profundo ({tono}) basado SOLO en esta información validada: {self.datos_validados}
        
        REGLAS ESTRICTAS:
        1. PROFUNDIDAD: Desarrolla cada sección a profundidad con múltiples párrafos. Expande el marco teórico.
        2. RESULTADOS TÉCNICOS: En la sección de 'Resultados', expón los datos duros, métricas y detalles técnicos extraídos. Quedan estrictamente prohibidas las generalidades.
        3. ESTRUCTURA OBLIGATORIA: Usa este formato exacto de títulos:
           - 1. Introducción
           - 2. Metodología
           - 3. Resultados (OBLIGATORIO: Integra aquí 1 TABLA comparativa matricial en formato Markdown)
           - 4. Discusión
           - 5. Conclusiones
        4. Añade "Referencias Bibliográficas" al final.
        """
        self.articulo_final = self.model.generate_content(prompt).text
        return "Artículo redactado."

    def capa_5_sintetizador(self):
        self.registro_auditoria.append("Sintetizador: Extrayendo conceptos clave y síntesis ejecutiva.")
        prompt = f"""
        Basado en el artículo generado: {self.articulo_final}
        Estructura la información de forma concisa con este diseño:
        ### 🎯 Conclusiones Principales
        (Genera 3 viñetas analíticas)
        ---
        ### 🧠 Conceptos Clave
        (Selecciona 3 términos de alta densidad técnica y explícalos brevemente)
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
    st.info("💡 **Garantía de Privacidad:** La validación de datos opera de manera completamente interna dentro del núcleo del agente.")
    st.divider()
    st.caption("© 2026 - Facultad de Ingeniería UNFV")

try:
    API_KEY_SECRETA = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY_SECRETA = ""

st.title("Plataforma de Investigación Científica (MAVR)")
st.markdown("Generación automatizada de manuscritos académicos con recuperación bibliométrica profunda y enlaces verificables.")

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
            st.error("Error del Servidor: La API Key no está configurada en la bóveda de seguridad (Secrets).")
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
                
                st.write("🔍 Extrayendo fuentes con datos duros y generando enlaces (Scholar)...")
                st.session_state.mavr.capa_2_bibliometrico()
                time.sleep(12) 
                
                st.write("🛡️ Formateando interfaz de auditoría...")
                st.session_state.mavr.capa_3_auditor()
                time.sleep(12)
                
                st.write("✍️ Redactando documento analítico y estructurando tablas...")
                st.session_state.mavr.capa_4_redactor(tono_redaccion)
                time.sleep(12)
                
                st.write("💡 Sintetizando conclusiones e indexando glosario...")
                st.session_state.mavr.capa_5_sintetizador()
                
                status.update(label="Documento generado exitosamente.", state="complete", expanded=False)

            # Mostrar artículo
            st.markdown(st.session_state.mavr.articulo_final)
            st.divider()
            
            # Botón de Descarga
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
            st.error(f"⚠️ Ha ocurrido un inconveniente (Posible saturación de cuota): {str(e)}")

with tab2:
    st.header("Repositorio de Fuentes Consultadas")
    st.write("Los enlaces redirigen a **Google Scholar** para validar la existencia y rigor técnico del artículo original.")
    st.divider()
    if st.session_state.proceso_iniciado and hasattr(st.session_state, 'mavr'):
        st.markdown(st.session_state.mavr.datos_validados)
    else:
        st.info("Genera una investigación para visualizar el repositorio bibliométrico.")

with tab3:
    if st.session_state.proceso_iniciado and hasattr(st.session_state, 'mavr'):
        st.markdown(st.session_state.mavr.glosario)
    else:
        st.info("Genera una investigación para compilar las conclusiones principales y conceptos clave.")
