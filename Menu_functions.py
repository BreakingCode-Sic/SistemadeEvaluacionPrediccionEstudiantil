from Colors import Colors
import os
import sys

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_user_input(choice):
    """Process user choice using match statement"""
    
    match choice:
        case '1':    
            print_info_message("Seleccionar estudiante por ID")
            # TODO: Implementar función para seleccionar estudiante
            wait_for_enter()
            return 1
            
        case '2':
            print_info_message("Agregar nuevo estudiante")
            # TODO: Implementar función para agregar estudiante
            wait_for_enter()
            return 2
            
        case '3':
            print_info_message("Eliminar estudiante")
            # TODO: Implementar función para eliminar estudiante
            wait_for_enter()
            return 3
            
        case '4':
            print_info_message("Modificar estudiante")
            # TODO: Implementar función para modificar estudiante
            wait_for_enter()
            return 4
            
        case '5':
            print_info_message("Listar estudiantes")
            # TODO: Implementar función para listar estudiantes
            wait_for_enter()
            return 5
            
        case '6':
            print_info_message("Predecir calificaciones")
            # TODO: Implementar función de predicción
            wait_for_enter()
            return 6
            
        case '7':
            print_info_message("Ver estadísticas")
            # TODO: Implementar función de estadísticas
            wait_for_enter()
            return 7
            
        case '8':
            clear_screen()
            print_goodbye()
            print_success_message("Sistema cerrado correctamente")
            return 0  # Signal to exit
            
        case _:
            print_error_message("Opción no válida. Por favor, seleccione una opción del 1 al 8.")
            wait_for_enter()
            return -1  # Signal invalid option
    


def print_success_message(message):
    """ success message with green styling"""
    print(f"\n{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error_message(message):
    """error message with red styling"""
    print(f"\n{Colors.RED}❌ {message}{Colors.ENDC}")


def print_info_message(message):
    """ info message with blue styling"""
    print(f"\n{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")


def wait_for_enter():
    """Wait for user to press Enter"""
    input(f"\n{Colors.YELLOW}📱 Presione Enter para continuar...{Colors.ENDC}")

def print_goodbye():
    """Print a goodbye message"""
 
    goodbye = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                       ¡HASTA LUEGO! 👋                       ║
║                                                              ║
║          Gracias por usar el Sistema de Predicción           ║
║                    de Calificaciones                         ║
║                                                              ║
║                 ¡Que tengas un buen día!                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(goodbye)