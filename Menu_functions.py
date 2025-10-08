from Colors import Colors
import os
from students import *
def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

  
def get_user_input(choice, df):
    """Process user choice using match statement"""
    
    match choice:
        case '1':    
            print_info_message("Seleccionar estudiante por ID")
            student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante: {Colors.ENDC}")
            student = get_student_by_id(df, student_id)
            if student is not None:
                print(f"\n✅ Estudiante encontrado:")
                print(student.to_string(index=False))
            wait_for_enter()
            return df, 1
            
        case '2':
            print_info_message("Agregar nuevo estudiante")
            try:
                nombre_estudiante = input(f"{Colors.CYAN}👤 Nombre del estudiante: {Colors.ENDC}")
                id_profesor = input(f"{Colors.CYAN}👨‍🏫 ID del profesor: {Colors.ENDC}")
                aula = input(f"{Colors.CYAN}🏫 Aula: {Colors.ENDC}")
                area = input(f"{Colors.CYAN}📚 Área (Ciencias, Matemáticas, etc.): {Colors.ENDC}")
                asignatura = input(f"{Colors.CYAN}📖 Asignatura: {Colors.ENDC}")
                nota = input(f"{Colors.CYAN}📝 Nota: {Colors.ENDC}")
                df = add_student(df, nombre_estudiante, id_profesor, aula, area, asignatura, nota)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")
            wait_for_enter()
            return df, 2
            
        case '3':
            print_info_message("Eliminar estudiante")
            # First show all students
            list_all_students(df)
            student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante a eliminar: {Colors.ENDC}")
            df = delete_student(df, student_id)
            wait_for_enter()
            return df, 3
            
        case '4':
            print_info_message("Modificar estudiante")
            try:
                # Mostrar todos los estudiantes primero
                list_all_students(df)
                
                # Pedir ID del estudiante a modificar
                student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante a modificar: {Colors.ENDC}")
                student = get_student_by_id(df, student_id)
                
                if student is None:
                    wait_for_enter()
                    return df, 4
                
                # Mostrar campos disponibles para modificar
                campos = ['nombre_estudiante', 'id_profesor', 'aula', 'area', 'asignatura', 'nota']
                print("\nCampos disponibles para modificar:")
                for i, campo in enumerate(campos, start=1):
                    print(f"{i}. {campo}")
                
                # Seleccionar campo
                opcion = input(f"{Colors.CYAN}Ingrese el número del campo a modificar: {Colors.ENDC}")
                if not opcion.isdigit() or int(opcion) not in range(1, len(campos)+1):
                    print("❌ Opción inválida")
                    wait_for_enter()
                    return df, 4
                
                campo_seleccionado = campos[int(opcion)-1]
                
                # Nuevo valor
                nuevo_valor = input(f"{Colors.CYAN}Ingrese el nuevo valor para {campo_seleccionado}: {Colors.ENDC}")
                
                # Validar tipo si es numérico
                if campo_seleccionado in ['id_profesor', 'nota']:
                    try:
                        nuevo_valor = float(nuevo_valor) if campo_seleccionado == 'nota' else int(nuevo_valor)
                    except ValueError:
                        print("❌ Valor inválido para el campo seleccionado")
                        wait_for_enter()
                        return df, 4
                
                # Llamar a la función de actualización
                df = update_student(df, int(student_id), campo_seleccionado, nuevo_valor)
        
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")

            wait_for_enter()
            return df, 4
            
        case '5':
            # print_info_message("Listar estudiantes")
            try:
                if df.empty:
                    print(f"{Colors.YELLOW}❌ No hay estudiantes registrados{Colors.ENDC}")
                else:
                    #dentro de esta opcion estara un mini menu con las sigientes opciones (5,8,9,10)
                    while True:
                        print("[1] Ver todos los estudiantes")
                        print("[2] Ver estudiantes por area")
                        print("[3] Ver estudiantes por asignatura")
                        print("[4] Ver Estudiantes en riego")
                        print("[0] Volver al menú principal")

                        sub_choice = input(f"{Colors.CYAN}Seleccione una opción (0-4): {Colors.ENDC}")
                    
                        if sub_choice == '0':
                            # Volver al menú principal: salir del submenu
                            break
                        elif sub_choice == '1':
                            print_info_message("Listar todos los estudiantes")
                            list_all_students(df)
                            wait_for_enter()
                        elif sub_choice == '2':
                            print_info_message("Ver estudiantes por área")
                            area_input = input(f"{Colors.CYAN}📚 Ingrese el área: {Colors.ENDC}")
                            estudiantes = get_students_by_area(df, area_input)
                            if estudiantes.empty:
                                print(f"❌ No hay estudiantes en el área {area_input}")
                            else:
                                print(f"\n📋 Estudiantes en el área {area_input}:")
                                print(estudiantes.to_string(index=False))
                            wait_for_enter()
                        elif sub_choice == '3':
                             print_info_message("Ver estudiantes por asignatura")
                             subject_input = input(f"{Colors.CYAN}📖 Ingrese la asignatura: {Colors.ENDC}")
                             estudiantes = get_students_by_subject(df, subject_input)
                             if estudiantes.empty:
                                print(f"❌ No hay estudiantes en la asignatura {subject_input}")
                             else:
                                print(f"\n📋 Estudiantes en la asignatura {subject_input}:")
                                print(estudiantes.to_string(index=False))
                             wait_for_enter()
                        elif sub_choice == '4':
                            print_info_message("Ver Estudiantes en riesgo")
                            try:
                                umbral_input = input(f"{Colors.CYAN}⚠️ Ingrese el umbral de riesgo (por defecto 60): {Colors.ENDC}")
                                umbral = float(umbral_input) if umbral_input.strip() != "" else 60
                            except ValueError:
                                print("❌ Valor inválido, se usará el umbral por defecto (60)")
                                umbral = 60
                            riesgo = students_at_risk(df, umbral)
                            if riesgo:
                                print(f"📝 IDs de estudiantes en riesgo: {riesgo}")
                            wait_for_enter()
                        elif sub_choice != '0' and sub_choice != '1' and sub_choice != '2' and sub_choice != '3' and sub_choice != '4':
                            print("❌ Opción inválida, por favor seleccione una opción del 0 al 4.")    
                    
                    # fin while

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")
            # Al salir del submenu volver al menú principal
            return df, 5
            
        #       case '8':
        #     print_info_message("Ver estudiantes por área")
        #     area_input = input(f"{Colors.CYAN}📚 Ingrese el área: {Colors.ENDC}")
        #     estudiantes = get_students_by_area(df, area_input)
            
        #     if estudiantes.empty:
        #         print(f"❌ No hay estudiantes en el área {area_input}")
        #     else:
        #         print(f"\n📋 Estudiantes en el área {area_input}:")
        #         print(estudiantes.to_string(index=False))
            
        #     wait_for_enter()
        #     return df, 8
        
        # case '9':
        #     print_info_message("Ver estudiantes por asignatura")
        #     subject_input = input(f"{Colors.CYAN}📖 Ingrese la asignatura: {Colors.ENDC}")
        #     estudiantes = get_students_by_subject(df, subject_input)
            
        #     if estudiantes.empty:
        #         print(f"❌ No hay estudiantes en la asignatura {subject_input}")
        #     else:
        #         print(f"\n📋 Estudiantes en la asignatura {subject_input}:")
        #         print(estudiantes.to_string(index=False))
            
        #     wait_for_enter()
        #     return df, 9
        
        # case '10':
        #     print_info_message("Estudiantes en riesgo")
            # try:
            #     umbral_input = input(f"{Colors.CYAN}⚠️ Ingrese el umbral de riesgo (por defecto 60): {Colors.ENDC}")
            #     umbral = float(umbral_input) if umbral_input.strip() != "" else 60
            # except ValueError:
            #     print("❌ Valor inválido, se usará el umbral por defecto (60)")
            #     umbral = 60
            # #Arreglo de la funcion students_at_risk (umbral estaba declarado 2 veces por defecto)
            # riesgo = students_at_risk(df, umbral)
            # if riesgo:
            #     print(f"📝 IDs de estudiantes en riesgo: {riesgo}")
            
        #     wait_for_enter()
        #     return df, 10
        #     return df, 5
            
        case '6':
            print_info_message("Predecir calificaciones")
            
            try:
                # Pedir ID del estudiante
                student_id = input(f"{Colors.CYAN}🆔 Ingrese el ID del estudiante para predecir su nota: {Colors.ENDC}")
                student = get_student_by_id(df, student_id)
                
                if student is None:
                    wait_for_enter()
                    return df, 6

                # Mostrar las notas actuales del estudiante
                notas_actuales = student['nota'].tolist()
                print(f"\n📊 Notas actuales del estudiante:")
                print(notas_actuales)

                # Preguntar si quiere simular una nueva nota
                nueva_nota_input = input(f"{Colors.CYAN}📝 Ingrese una nota hipotética para proyectar promedio (ENTER para omitir): {Colors.ENDC}")
                if nueva_nota_input.strip() != "":
                    try:
                        nueva_nota = float(nueva_nota_input)
                        # Llamar a la función de predicción
                        predict_student_score(df, int(student_id), nueva_nota)
                    except ValueError:
                        print("❌ Valor inválido, se ignorará la nota hipotética.")
                else:
                    print("⚠️ No se ingresó nota hipotética, mostrando promedio actual.")
                    promedio_actual = sum(notas_actuales) / len(notas_actuales)
                    print(f"📈 Promedio actual del estudiante: {round(promedio_actual, 2)}")
            
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}⚠️ Operación cancelada{Colors.ENDC}")

            wait_for_enter()
            return df, 6
            
        case '7':
            print_info_message("Ver estadísticas")
            stats = get_database_stats(df)
            if not stats:
                print(f"{Colors.YELLOW}❌ No hay estudiantes registrados{Colors.ENDC}")
                wait_for_enter()
                return df, 7

            # Estadísticas generales
            print("\n📊 ESTADÍSTICAS GENERALES:")
            print("=" * 40)
            print(f"👥 Total estudiantes: {Colors.CYAN}{stats['total_students']}{Colors.ENDC}")
            print(f"📊 Calificación promedio: {Colors.CYAN}{stats['average_score']:.2f}{Colors.ENDC}")
            print(f"🏆 Calificación más alta: {Colors.GREEN}{stats['highest_score']}{Colors.ENDC}")
            print(f"📉 Calificación más baja: {Colors.RED}{stats['lowest_score']}{Colors.ENDC}")
            print("=" * 40)

            # Estadísticas por área
            areas = df['area'].dropna().unique()
            print("\n📚 Promedio por área:")
            for area in areas:
                promedio_area = average_by_area(df, area)
                if promedio_area is not None:
                    print(f"📌 {area}: {Colors.CYAN}{promedio_area:.2f}{Colors.ENDC}")

            # Estadísticas por asignatura
            asignaturas = df['asignatura'].dropna().unique()
            print("\n📖 Promedio por asignatura:")
            for asignatura in asignaturas:
                promedio_asig = average_by_subject(df, asignatura)
                if promedio_asig is not None:
                    print(f"📌 {asignatura}: {Colors.CYAN}{promedio_asig:.2f}{Colors.ENDC}")
            
            wait_for_enter()
            return df, 7

      
                    
        case  '0':
            clear_screen()
            print_goodbye()
            print_success_message("Sistema cerrado correctamente")
            return df, 0  # Signal to exit
            
        case _:
            print_error_message("Opción no válida. Por favor, seleccione una opción del 0 al 7.")
            wait_for_enter()
            return df, -1  # Signal invalid option
    


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