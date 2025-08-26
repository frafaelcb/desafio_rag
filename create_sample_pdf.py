#!/usr/bin/env python3
"""
Script para criar um PDF de exemplo para testar o sistema RAG
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os

def create_sample_pdf():
    """Cria um PDF de exemplo com conteúdo sobre inteligência artificial"""
    
    # Criar diretório se não existir
    os.makedirs("data/documents", exist_ok=True)
    
    # Nome do arquivo
    filename = "data/documents/exemplo_ia.pdf"
    
    # Criar o PDF
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, 10*inch, "Inteligência Artificial: Uma Visão Geral")
    
    # Subtítulo
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, 9.5*inch, "Por: Sistema RAG de Exemplo")
    
    # Conteúdo
    c.setFont("Helvetica", 10)
    
    content = [
        "O que é Inteligência Artificial?",
        "",
        "Inteligência Artificial (IA) é um campo da ciência da computação que busca",
        "criar sistemas capazes de realizar tarefas que normalmente requerem",
        "inteligência humana. Essas tarefas incluem aprendizado, raciocínio,",
        "percepção, resolução de problemas e tomada de decisões.",
        "",
        "Tipos de IA:",
        "",
        "1. IA Fraca (Narrow AI): Sistemas projetados para tarefas específicas",
        "   como reconhecimento de voz, processamento de linguagem natural",
        "   ou jogos de xadrez.",
        "",
        "2. IA Forte (General AI): Sistemas com inteligência humana geral,",
        "   capazes de realizar qualquer tarefa intelectual que um humano",
        "   pode fazer.",
        "",
        "Aplicações da IA:",
        "",
        "• Assistentes virtuais (Siri, Alexa, Google Assistant)",
        "• Carros autônomos",
        "• Diagnóstico médico",
        "• Recomendação de produtos",
        "• Análise de dados",
        "• Processamento de linguagem natural",
        "",
        "Técnicas de IA:",
        "",
        "• Machine Learning: Algoritmos que aprendem com dados",
        "• Deep Learning: Redes neurais com múltiplas camadas",
        "• Processamento de Linguagem Natural (NLP)",
        "• Visão Computacional",
        "• Robótica",
        "",
        "Desafios da IA:",
        "",
        "• Viés nos dados e algoritmos",
        "• Privacidade e segurança",
        "• Impacto no emprego",
        "• Responsabilidade e ética",
        "• Transparência e explicabilidade",
        "",
        "O futuro da IA:",
        "",
        "A IA continuará evoluindo rapidamente, integrando-se cada vez mais",
        "em nossas vidas diárias. É importante desenvolver e usar a IA",
        "de forma responsável e ética, considerando seus impactos sociais,",
        "econômicos e ambientais."
    ]
    
    y_position = 9*inch
    for line in content:
        if y_position < 1*inch:  # Nova página se necessário
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = 10*inch
        
        c.drawString(1*inch, y_position, line)
        y_position -= 0.25*inch
    
    c.save()
    print(f"✅ PDF criado com sucesso: {filename}")
    return filename

if __name__ == "__main__":
    create_sample_pdf()
