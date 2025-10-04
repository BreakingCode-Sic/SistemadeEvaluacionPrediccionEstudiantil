
#this is the data base of students for the project:

import pandas as pd


# Temporal database for testing
students_data = {
    'ID': [1, 2, 3, 4],
    'Name': ['Ana', 'Luis', 'Maria', 'Carlos'],
    'Age': [25, 30, 28, 35],
    'Score': [89, 71, 91, 85]
}

df = pd.DataFrame(students_data)


def get_student_by_id(student_id):
    """Find student by ID"""
    try:
        student_id = int(student_id)
        student = df[df['ID'] == student_id]
        if not student.empty:
            return student
        else:
            print(f"❌ No se encontró estudiante con ID {student_id}")
            return None
    except ValueError:
        print("❌ ID debe ser un número válido")
        return None


def add_student(name, age, score):
    """Add new student to database"""
    global df
    try:
        age = int(age)
        score = float(score)
        
        # Get next available ID
        next_id = df['ID'].max() + 1 if not df.empty else 1
        
        new_student = pd.DataFrame({
            'ID': [next_id],
            'Name': [name],
            'Age': [age],
            'Score': [score]
        })

        df = pd.concat([df, new_student], ignore_index=True)
        print(f"✅ Estudiante {name} agregado correctamente con ID {next_id}")
        return new_student
        
    except ValueError as e:
        print(f"❌ Error en los datos: {e}")
        return None


def delete_student(student_id):
    """Delete student by ID"""
    global df
    try:
        student_id = int(student_id)
        if student_id in df['ID'].values:
            student_name = df[df['ID'] == student_id]['Name'].iloc[0]
            df = df[df['ID'] != student_id].reset_index(drop=True)
            print(f"✅ Estudiante {student_name} (ID: {student_id}) eliminado correctamente")
            return True
        else:
            print(f"❌ No se encontró estudiante con ID {student_id}")
            return False
    except ValueError:
        print("❌ ID debe ser un número válido")
        return False


def list_all_students():
    """Display all students in a formatted way"""
    if df.empty:
        print("❌ No hay estudiantes registrados")
        return
    
    print("\n📋 LISTA DE ESTUDIANTES:")
    print("=" * 50)
    for _, student in df.iterrows():
        print(f"🆔 ID: {student['ID']} | 👤 {student['Name']} | 🎂 {student['Age']} años | 📊 Score: {student['Score']}")
    print("=" * 50)


def get_database_stats():
    """Get database statistics"""
    if df.empty:
        return "No hay estudiantes registrados"
    
    stats = {
        'total_students': len(df),
        'average_age': df['Age'].mean(),
        'average_score': df['Score'].mean(),
        'highest_score': df['Score'].max(),
        'lowest_score': df['Score'].min()
    }
    return stats


