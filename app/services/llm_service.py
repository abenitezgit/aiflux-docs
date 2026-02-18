"""
LLM Service - Integración con Groq vía LiteLLM

RESPONSABILIDADES:
- Preparar prompts en contexto
- Llamar Groq API
- Manejo de errores y retries
- Logging de uso

ARQUITECTURA:
- Minimal: Solo Groq por ahora
- Extensible: Fácil agregar Claude, DeepSeek, OpenAI después
- Async-ready: Para streaming futuro
"""

import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Servicio centralizado para llamadas a LLM
    
    Interfaz:
    - groq_generate(content: str, prompt: str) -> str
    """
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = "llama-3.3-70b-versatile"  # Modelo activo (llama-3.1-70b fue deprecado)
        
        if not self.api_key:
            logger.warning("⚠️  GROQ_API_KEY no configurada")
    
    def groq_generate(self, content: str, prompt: str, context_hierarchy: str = None) -> str:
        """
        Genera una respuesta usando Groq
        
        Args:
            content: Texto plano completo de la nota activa
            prompt: Pregunta del usuario
            context_hierarchy: Jerarquía de bibliotecas/cuadernos/temas/notas (JSON string)
        
        Returns:
            Respuesta de texto de Groq
        
        Raises:
            Exception: Si hay error con la API
        """
        import litellm
        
        if not self.api_key:
            raise Exception("GROQ_API_KEY no configurada")
        
        try:
            # System prompt: contexto para la IA
            system_prompt = """Eres un asistente inteligente para un sistema de notas.

Tu propósito es ayudar al usuario con preguntas sobre sus notas, su estructura y contenido.

ESTRUCTURA DE LA INFORMACIÓN QUE RECIBES:
1. NOTA ACTIVA: La nota en la que estás trabajando actualmente (contenido completo)
2. JERARQUÍA: Tu biblioteca completa organizada como:
   - Bibliotecas (Categorías)
     └─ Cuadernos
       └─ Temas
         └─ Notas (solo títulos, sin contenido)

INSTRUCCIONES CRÍTICAS - DETERMINA QUÉ RESPONDER:

A. Si la pregunta es sobre BIBLIOTECAS, CUADERNOS, TEMAS o la ESTRUCTURA:
   → Responde DIRECTAMENTE sobre la jerarquía
   → Ejemplo: "cuales bibliotecas tengo?" → Lista todas las bibliotecas de la jerarquía
   → Ejemplo: "cuales notas tengo en X cuaderno?" → Lista las notas en ese cuaderno
   → NO necesitas mencionar la nota activa

B. Si la pregunta es sobre la NOTA ACTIVA:
   → Responde enfocándote en el contenido de la nota activa
   → Puedes sugerir notas relacionadas en la jerarquía

C. Si la pregunta es GENERAL o pide CONEXIONES:
   → Usa ambos: nota activa como contexto + jerarquía como referencias
   → Sugiere notas relacionadas si es relevante

FORMATO DE RESPUESTA:
- Texto plano limpio (sin markdown, sin HTML)
- Mantén saltos de línea naturales
- Si mencionas otras notas: "tu nota 'nombre' en Biblioteca > Cuaderno > Tema"
- Sé conciso y directo"""

            # Preparar el mensaje de usuario
            user_message = f"""JERARQUÍA DE TUS NOTAS:
{context_hierarchy or "No hay jerarquía disponible"}

"""
            
            # Agregar nota activa solo si hay contenido
            if content and content.strip():
                user_message += f"""NOTA ACTIVA (opcional, para contexto):
{content}

"""
            
            user_message += f"""PREGUNTA DEL USUARIO:
{prompt}

Responde según las instrucciones: si es sobre estructura/bibliotecas, responde eso directamente. Si es sobre la nota activa, responde sobre ella."""

            # 🔍 LOG DETALLADO para debugging
            logger.info(f"\n{'='*80}")
            logger.info(f"🤖 GROQ REQUEST DETAILS")
            logger.info(f"{'='*80}")
            logger.info(f"\n📋 SYSTEM PROMPT:\n{system_prompt}\n")
            logger.info(f"\n👤 USER MESSAGE:\n{user_message}\n")
            logger.info(f"{'='*80}\n")

            # Llamar a Groq vía LiteLLM
            response = litellm.completion(
                model=f"groq/{self.model}",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1024,
                api_key=self.api_key,
                timeout=30
            )
            
            # Extraer respuesta
            answer = response.choices[0].message.content
            
            logger.info(f"✅ Groq response generada ({len(answer)} chars)")
            
            return answer
            
            
        except Exception as e:
            logger.error(f"❌ Error en Groq: {str(e)}")
            raise Exception(f"Error generando respuesta: {str(e)}")