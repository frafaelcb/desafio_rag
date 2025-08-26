"""
Builder para construção de menus
Implementa Builder Pattern
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class MenuOption:
    """Representa uma opção de menu"""
    key: str
    description: str
    action: Optional[str] = None
    icon: str = ""
    
    def __str__(self) -> str:
        return f"{self.key}. {self.icon}{self.description}"


@dataclass
class Menu:
    """Representa um menu completo"""
    title: str
    options: List[MenuOption]
    subtitle: str = ""
    separator: str = "-"
    separator_length: int = 30
    
    def get_options_dict(self) -> Dict[str, str]:
        """Retorna opções como dicionário"""
        return {opt.key: f"{opt.icon}{opt.description}" for opt in self.options}
    
    def get_option_by_key(self, key: str) -> Optional[MenuOption]:
        """Busca opção por chave"""
        for option in self.options:
            if option.key == key:
                return option
        return None


class MenuBuilder:
    """Builder para construção de menus"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reseta o builder"""
        self._title = ""
        self._subtitle = ""
        self._options = []
        self._separator = "-"
        self._separator_length = 30
        return self
    
    def set_title(self, title: str) -> 'MenuBuilder':
        """Define o título do menu"""
        self._title = title
        return self
    
    def set_subtitle(self, subtitle: str) -> 'MenuBuilder':
        """Define o subtítulo do menu"""
        self._subtitle = subtitle
        return self
    
    def set_separator(self, separator: str, length: int = 30) -> 'MenuBuilder':
        """Define o separador do menu"""
        self._separator = separator
        self._separator_length = length
        return self
    
    def add_option(self, key: str, description: str, icon: str = "", action: str = None) -> 'MenuBuilder':
        """Adiciona uma opção ao menu"""
        option = MenuOption(key=key, description=description, icon=icon, action=action)
        self._options.append(option)
        return self
    
    def add_back_option(self, key: str = "0", description: str = "Voltar") -> 'MenuBuilder':
        """Adiciona opção de voltar"""
        return self.add_option(key, description, icon="⬅️ ")
    
    def add_exit_option(self, key: str = "0", description: str = "Sair") -> 'MenuBuilder':
        """Adiciona opção de sair"""
        return self.add_option(key, description, icon="🚪 ")
    
    def add_separator(self) -> 'MenuBuilder':
        """Adiciona separador visual"""
        separator_option = MenuOption(
            key="", 
            description=self._separator * self._separator_length,
            icon=""
        )
        self._options.append(separator_option)
        return self
    
    def build(self) -> Menu:
        """Constrói o menu"""
        menu = Menu(
            title=self._title,
            subtitle=self._subtitle,
            options=self._options.copy(),
            separator=self._separator,
            separator_length=self._separator_length
        )
        self.reset()
        return menu


class MenuFactory:
    """Factory para criação de menus comuns"""
    
    @staticmethod
    def create_main_menu() -> Menu:
        """Cria menu principal"""
        return (MenuBuilder()
                .set_title("Sistema RAG - Menu Interativo")
                .set_separator("=", 50)
                .add_option("1", "Ver informações do sistema", "📊")
                .add_option("2", "Indexar um PDF", "📄")
                .add_option("3", "Fazer uma pergunta", "💬")
                .add_option("4", "Buscar documentos similares", "🔍")
                .add_option("5", "Modo chat interativo", "🤖")
                .add_option("6", "Testar conexões", "🧪")
                .add_option("7", "Ver ajuda", "📖")
                .add_exit_option("0", "Sair")
                .build())
    
    @staticmethod
    def create_index_menu(pdf_files: List[str], indexed_pdfs: List[str]) -> Menu:
        """Cria menu de indexação"""
        builder = (MenuBuilder()
                  .set_title("Menu de Indexação")
                  .set_separator("=", 50))
        
        # Adicionar PDFs encontrados
        for i, pdf_path in enumerate(pdf_files, 1):
            pdf_name = pdf_path.split('/')[-1]
            is_indexed = pdf_path in indexed_pdfs
            status = "✅ Indexado" if is_indexed else "❌ Não indexado"
            builder.add_option(str(i), f"{pdf_name} - {status}")
        
        # Adicionar opções extras
        builder.add_option(str(len(pdf_files) + 1), "Especificar caminho manualmente", "📁")
        builder.add_option(str(len(pdf_files) + 2), "Reindexar documento existente", "🔄")
        builder.add_option(str(len(pdf_files) + 3), "Remover documento indexado", "🗑️")
        builder.add_back_option(str(len(pdf_files) + 4), "Voltar ao menu principal")
        
        return builder.build()
    
    @staticmethod
    def create_pdf_options_menu(pdf_name: str, is_indexed: bool, chunks_count: int = 0) -> Menu:
        """Cria menu de opções para um PDF específico"""
        builder = (MenuBuilder()
                  .set_title(f"Opções para: {pdf_name}")
                  .set_separator("-", 40))
        
        if is_indexed:
            builder.add_option("1", f"Reindexar (substituir) - {chunks_count} chunks", "🔄")
            builder.add_option("2", "Ver informações", "📊")
        else:
            builder.add_option("1", "Indexar", "📥")
        
        builder.add_back_option("3", "Voltar")
        
        return builder.build()
    
    @staticmethod
    def create_confirm_menu(action: str, item_name: str, warning: str = "") -> Menu:
        """Cria menu de confirmação"""
        builder = (MenuBuilder()
                  .set_title(f"{action}: {item_name}")
                  .set_separator("-", 40))
        
        if warning:
            builder.add_option("", warning, "⚠️")
            builder.add_separator()
        
        builder.add_option("s", "Sim", "✅")
        builder.add_option("n", "Não", "❌")
        
        return builder.build()
