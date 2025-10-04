from Colors import Colors
from datetime import datetime
from Menu_functions import *


def print_header():
    header = f"""
{Colors.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🎓 SISTEMA INTELIGENTE DE CALIFICACIONES 🎓           ║
║                                                              ║
║              📊 Predicción de Notas Estudiantiles 📊         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.YELLOW}📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}{Colors.ENDC}
{Colors.GREEN}🖥️  Sistema: Predictor de Calificaciones v1.0{Colors.ENDC}
"""
    print(header)

def print_menu():
    menu = f"""
{Colors.BLUE}
┌───────────────────────────────────────────────────────────────────┐
│                         {Colors.BOLD}🏠 MENÚ PRINCIPAL{Colors.ENDC}{Colors.BLUE}                         │
└───────────────────────────────────────────────────────────────────┘{Colors.ENDC}

{Colors.GREEN}📋 OPCIONES DISPONIBLES:{Colors.ENDC}

{Colors.CYAN}   🔍 [1]{Colors.ENDC} {Colors.BOLD}Seleccionar estudiante por ID{Colors.ENDC}
{Colors.CYAN}   ➕ [2]{Colors.ENDC} {Colors.BOLD}Agregar nuevo estudiante{Colors.ENDC}
{Colors.CYAN}   🗑️  [3]{Colors.ENDC} {Colors.BOLD}Eliminar estudiante{Colors.ENDC}
{Colors.CYAN}   ✏️  [4]{Colors.ENDC} {Colors.BOLD}Modificar datos de estudiante por ID{Colors.ENDC}
{Colors.CYAN}   📃 [5]{Colors.ENDC} {Colors.BOLD}Listar todos los estudiantes{Colors.ENDC}
{Colors.CYAN}   🔮 [6]{Colors.ENDC} {Colors.BOLD}Predecir calificaciones y posibles fortalezas{Colors.ENDC}
{Colors.CYAN}   📊 [7]{Colors.ENDC} {Colors.BOLD}Ver estadísticas generales{Colors.ENDC}
{Colors.RED}   🚪 [8]{Colors.ENDC} {Colors.BOLD}Salir del sistema{Colors.ENDC}


"""
    print(menu)



def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        # Get user input
        prompt = f"{Colors.CYAN}🎯 Seleccione una opción (1-8): {Colors.ENDC}"
        choice = input(prompt).strip()
        
        # Process the choice using match statement
        result =   get_user_input(choice)

        if result == 0:
            break

if __name__ == "__main__":
    main()

