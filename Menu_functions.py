from Colors import Colors
import os


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_user_input():
    """Get user input with styled prompt"""
    prompt = f"{Colors.CYAN}🎯 Seleccione una opción (1-8): {Colors.ENDC}"
    return input(prompt).strip()

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