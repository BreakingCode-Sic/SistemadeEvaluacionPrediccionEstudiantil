import os
import sys
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
    """Print the main menu with beautiful formatting"""
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



# Main menu loop
def main():
    """Main program loop"""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = get_user_input()
        
        if choice == '1':
            print_info_message("Función: Seleccionar estudiante por ID")
            # TODO: Implementar función para seleccionar estudiante
            wait_for_enter()
            
        elif choice == '2':
            print_info_message("Función: Agregar nuevo estudiante")
            # TODO: Implementar función para agregar estudiante
            wait_for_enter()
            
        elif choice == '3':
            print_info_message("Función: Eliminar estudiante")
            # TODO: Implementar función para eliminar estudiante
            wait_for_enter()
            
        elif choice == '4':
            print_info_message("Función: Modificar estudiante")
            # TODO: Implementar función para modificar estudiante
            wait_for_enter()
            
        elif choice == '5':
            print_info_message("Función: Listar estudiantes")
            # TODO: Implementar función para listar estudiantes
            wait_for_enter()
            
        elif choice == '6':
            print_info_message("Función: Predecir calificaciones")
            # TODO: Implementar función de predicción
            wait_for_enter()
            
        elif choice == '7':
            print_info_message("Función: Ver estadísticas")
            # TODO: Implementar función de estadísticas
            wait_for_enter()
            
        elif choice == '8':
            clear_screen()
            print_goodbye()
            print_success_message("Sistema cerrado correctamente")
            sys.exit(0)
            
        else:
            print_error_message("Opción no válida. Por favor, seleccione una opción del 1 al 8.")
            wait_for_enter()

if __name__ == "__main__":
    main()

