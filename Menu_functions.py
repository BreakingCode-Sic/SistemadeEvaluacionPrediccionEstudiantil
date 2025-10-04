from Colors import Colors
import os
from students import *

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

  
def get_user_input(choice):
    """Process user choice using match statement"""
    
    match choice:
        case '1':    
            print_info_message("Seleccionar estudiante por ID")
            student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante: {Colors.ENDC}")
            student = get_student_by_id(student_id)
            if student is not None:
                print(f"\n✅ Estudiante encontrado:")
                print(student.to_string(index=False))
            wait_for_enter()
            return 1
            
        case '2':
            print_info_message("Agregar nuevo estudiante")
            try:
                name = input(f"{Colors.CYAN}👤 Nombre: {Colors.ENDC}")
                age = input(f"{Colors.CYAN}🎂 Edad: {Colors.ENDC}")
                score = input(f"{Colors.CYAN}📊 Calificación: {Colors.ENDC}")
                add_student(name, age, score)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")
            wait_for_enter()
            return 2
            
        case '3':
            print_info_message("Eliminar estudiante")
            # First show all students
            list_all_students()
            student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante a eliminar: {Colors.ENDC}")
            delete_student(student_id)
            wait_for_enter()
            return 3
            
        case '4':
            print_info_message("Modificar estudiante")
            # TODO: Implementar función para modificar estudiante
            print("🚧 Función en desarrollo")
            wait_for_enter()
            return 4
            
        case '5':
            print_info_message("Listar estudiantes")
            list_all_students()
            wait_for_enter()
            return 5
            
        case '6':
            print_info_message("Predecir calificaciones")
            # TODO: Implementar función de predicción
            print("🚧 Función en desarrollo")
            wait_for_enter()
            return 6
            
        case '7':
            print_info_message("Ver estadísticas")
            stats = get_database_stats()
            if isinstance(stats, dict):
                print(f"\n📊 ESTADÍSTICAS GENERALES:")
                print(f"👥 Total estudiantes: {stats['total_students']}")
                print(f"🎂 Edad promedio: {stats['average_age']:.1f} años")
                print(f"📊 Calificación promedio: {stats['average_score']:.1f}")
                print(f"🏆 Calificación más alta: {stats['highest_score']}")
                print(f"📉 Calificación más baja: {stats['lowest_score']}")
            else:
                print(stats)
            wait_for_enter()
            return 7
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