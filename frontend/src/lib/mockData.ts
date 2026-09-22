import type { LoginCredentials, RegisterPayload, User, AuthResponse, UserRole, AddPeopleResponse } from '@/types/auth';
import type {
  Classroom,
  Competency,
  Quiz,
  NewQuizPayload,
  Question,
  GenerateQuizFromDocumentPayload,
  GenerateQuizFromTextPayload,
  TypeQuestion,
  StudentResult,
  Character,
  StoreCharacterData,
  QuizSubmissionSummary,
  StudentQuizAttempt,
  QuestionAttempt,
  SaveFeedbackPayload,
  QuizForTaking,
  StudentQuizSubmissionPayload,
} from '@/types/entities';
// Mock data
export const mockUsers: Record<string, User> = {
  '1': {
    id: '1',
    name: 'Cristhian',
    last_name: 'Paz',
    email: 'teacher@gmail.com',
    role: 'TEACHER',
    cel_phone: null,
    registration_date: '2025-06-11T09:49:45.783000Z',
  },
  '2': {
    id: '2',
    name: 'Alex',
    last_name: 'Student',
    email: 'student@gmail.com',
    role: 'STUDENT',
    cel_phone: '123-456-7890',
    registration_date: '2025-07-01T10:00:00.000Z',
    emotion: 'Feliz',
    coin_earned: 100,
    coin_available: 50,
  },
  'student1': { id: 'student1', name: 'Ana', last_name: 'García', email: 'ana.garcia@example.com', role: 'STUDENT', cel_phone: '555-0101', emotion: 'Concentrada', registration_date: '2023-01-10T10:00:00Z', coin_earned: 150, coin_available: 75 },
  'student2': { id: 'student2', name: 'Luis', last_name: 'Martinez', email: 'luis.martinez@example.com', role: 'STUDENT', cel_phone: '555-0102', emotion: 'Curioso', registration_date: '2023-01-11T10:00:00Z', coin_earned: 200, coin_available: 120 },
  'student3': { id: 'student3', name: 'Sofia', last_name: 'Rodriguez', email: 'sofia.rodriguez@example.com', role: 'STUDENT', cel_phone: null, emotion: 'Entusiasmada', registration_date: '2023-01-12T10:00:00Z', coin_earned: 80, coin_available: 30 },
  'student4': { id: 'student4', name: 'Carlos', last_name: 'Hernandez', email: 'carlos.h@example.com', role: 'STUDENT', cel_phone: '555-0104', emotion: 'Motivado', registration_date: '2023-01-13T10:00:00Z', coin_earned: 120, coin_available: 100 },
  'student5': { id: 'student5', name: 'Laura', last_name: 'Lopez', email: 'laura.lopez@example.com', role: 'STUDENT', cel_phone: '555-0105', emotion: 'Alegre', registration_date: '2023-01-14T10:00:00Z', coin_earned: 50, coin_available: 50 },
  'teacher2': { id: 'teacher2', name: 'Maria', last_name: 'Gonzales', email: 'maria.gonzales@example.com', role: 'TEACHER', cel_phone: '555-0201', registration_date: '2023-01-15T10:00:00Z' },
};

export const mockClassroomTeachers: Record<string, User[]> = {
    'c1': [mockUsers['1']],
    'c2': [mockUsers['1'], mockUsers['teacher2']],
    'c3': [mockUsers['teacher2']],
};

export const mockClassroomStudents: Record<string, User[]> = {
    'c1': [mockUsers['student1'], mockUsers['student2'], mockUsers['student3'], mockUsers['2']], // Alex Student in c1
    'c2': [mockUsers['student4'], mockUsers['student5']],
    'c3': [mockUsers['student1'], mockUsers['student2'], mockUsers['student3'], mockUsers['student4'], mockUsers['student5']],
};


export const mockTeacherClassrooms: Record<string, Omit<Classroom, 'quiz' | 'competences'>[]> = {
  '1': [
    { id: 'c1', name: 'Salon de prueba', description: 'Clase de prueba' },
    { id: 'c2', name: 'Matematica', description: 'Salon de prueba de Matematicas' },
    { id: 'c3', name: 'Comunicacion', description: 'Salon de prueba de Comunicacion' },
  ],
  'teacher2': [
    { id: 'c2-maria', name: 'Matematica Avanzada', description: 'Clase avanzada de Matematicas impartida por Maria' },
    { id: 'c3-maria', name: 'Taller de Escritura Creativa', description: 'Taller para desarrollar habilidades de escritura' },
  ]
};

export const mockStudentClassroomEnrollments: Record<string, string[]> = {
  'student1': ['c1', 'c3'],
  'student2': ['c1', 'c3'],
  'student3': ['c1', 'c3'],
  'student4': ['c2', 'c3'],
  'student5': ['c2', 'c3'],
  '2': ['c1'], // Alex Student
};

export const mockClassroomDetailsData: Record<string, Classroom> = {
  'c1': {
    id: 'c1',
    name: "Salon de prueba",
    description: "Clase de prueba. En este curso introductorio, exploraremos los fundamentos de la materia, sentando las bases para conceptos más avanzados. Participa activamente y no dudes en preguntar.",
    quiz: [
      {
        id: 'q1',
        classroom_id: 'c1',
        title: "Quiz de Bienvenida",
        instruction: "Completa este quiz para empezar y familiarizarte con la plataforma. Cubre los temas básicos de la primera semana.",
        total_points: 20,
        start_time: "2025-06-15T09:00:00Z",
        end_time: "2025-06-16T23:59:00Z",
        created_at: "2025-06-10T18:49:18.757Z",
        updated_at: "2025-06-10T18:49:18.757Z",
        questions: [
            { id: 'q1-ques1', statement: "Pregunta 1 de bienvenida (texto)", answer_correct: "Respuesta correcta 1", points: 10, answer_base: { type: "base_text" }, competences_id: ['comp1-c1'] },
            { id: 'q1-ques2', statement: "Pregunta 2 de bienvenida (opción múltiple)", answer_correct: "Opción A", points: 10, answer_base: { type: "base_multiple_option", options: ["Opción A", "Opción B", "Opción C"] }, competences_id: ['comp1-c1'] }
        ]
      },
      {
        id: 'q2',
        classroom_id: 'c1',
        title: "Quiz Intermedio: Unidad 1",
        instruction: "Este quiz evalúa tu comprensión de los conceptos clave presentados en la Unidad 1. Asegúrate de repasar el material antes de comenzar.",
        total_points: 25,
        start_time: "2025-06-20T10:00:00Z",
        end_time: "2025-06-22T23:59:00Z",
        created_at: "2025-06-11T10:00:00Z",
        updated_at: "2025-06-11T10:00:00Z",
        questions: []
      }
    ],
    competences: [
      { id: 'comp-general-1', name: 'Resolución de problemas General', description: 'Aplicación lógica y estructurada' },
      { id: 'comp1-c1', name: 'Pensamiento Crítico (Clase 1)', description: 'Análisis y evaluación de información para C1' }
    ]
  },
  'c2': {
    id: 'c2',
    name: "Matematica",
    description: "Salon de prueba de Matematicas. Exploraremos álgebra, geometría y cálculo, desarrollando habilidades analíticas y de resolución de problemas complejos.",
    quiz: [
      {
        id: 'q3',
        classroom_id: 'c2',
        title: "Prueba de Álgebra Básica",
        instruction: "Demuestra tus habilidades fundamentales en álgebra resolviendo estos problemas.",
        total_points: 30,
        start_time: "2025-07-01T09:00:00Z",
        end_time: "2025-07-03T23:59:00Z",
        created_at: "2025-06-20T10:00:00Z",
        updated_at: "2025-06-20T10:00:00Z",
        questions: []
      },
    ],
    competences: [
       { id: 'comp-general-2', name: 'Pensamiento Crítico General', description: 'Análisis y evaluación de información' },
       { id: 'comp2-c2', name: 'Geometría Espacial (Clase 2)', description: 'Competencia de geometría para C2' },
    ]
  },
  'c3': {
    id: 'c3',
    name: "Comunicacion",
    description: "Salon de prueba de Comunicacion. Enfocado en mejorar habilidades de escritura, expresión oral y comprensión lectora efectiva.",
    quiz: [],
    competences: [
      { id: 'comp1-c3', name: 'Oratoria (Clase 3)', description: 'Habilidad de hablar en público para C3' }
    ]
  },
   'c2-maria': {
    id: 'c2-maria',
    name: "Matematica Avanzada",
    description: "Clase avanzada de Matematicas impartida por Maria, cubriendo temas de cálculo integral y diferencial, y sus aplicaciones.",
    quiz: [],
    competences: [
       { id: 'comp-general-3', name: 'Planificación Estratégica', description: 'Definición de objetivos y planes de acción.' },
    ]
  },
  'c3-maria': {
    id: 'c3-maria',
    name: "Taller de Escritura Creativa",
    description: "Taller para desarrollar habilidades de escritura, explorando géneros como la narrativa corta, poesía y ensayo.",
    quiz: [],
    competences: [
      { id: 'comp1-c3-maria', name: 'Narrativa Corta', description: 'Creación de historias breves.' }
    ]
  }
};

export const mockTeacherGeneralCompetencies: Record<string, Competency[]> = {
  '1': [ // Cristhian Paz
    { id: 'comp-general-1', name: 'Resolución de problemas General', description: 'Aplicación lógica y estructurada' },
    { id: 'comp1-c1', name: 'Pensamiento Crítico (Clase 1)', description: 'Análisis y evaluación de información para C1' }, // Simulating it was also a general one
    { id: 'comp-unique-cris-1', name: 'Análisis de Datos', description: 'Interpretación y modelado de datos.' },
    { id: 'comp-unique-cris-2', name: 'Programación Python', description: 'Desarrollo de aplicaciones con Python.' },
  ],
  'teacher2': [ // Maria Gonzales
     { id: 'comp-general-3', name: 'Planificación Estratégica', description: 'Definición de objetivos y planes de acción.' },
     { id: 'comp2-c2', name: 'Geometría Espacial (Clase 2)', description: 'Competencia de geometría para C2' }, // Simulating
     { id: 'comp-unique-maria-1', name: 'Liderazgo de Equipos', description: 'Gestión y motivación de equipos de trabajo.' },
     { id: 'comp-unique-maria-2', name: 'Comunicación Efectiva', description: 'Transmisión clara de ideas.' },
  ]
};

export const mockStudentCurrentCharacter: Record<string, Character> = {
  'student1': {
    id: "35a36131-5548-4378-96ca-c5cb909c7450",
    name: "Donkey",
    modelUrl: "https://mscharacters.s3.us-east-1.amazonaws.com/Donkey.glb",
    price: 0, // Assuming current character is already owned
    type: "ANIMAL",
  },
   '2': { // Alex Student - Default character
    id: "c2aebc34-d5b8-4411-908a-293e644c3c79",
    name: "Fox",
    modelUrl: "https://mscharacters.s3.us-east-1.amazonaws.com/Fox.glb",
    price: 0,
    type: "ANIMAL",
  },
};

export const mockStoreCharacters: StoreCharacterData = {
  ANIMAL: [
    {
      id: "35a36131-5548-4378-96ca-c5cb909c7450",
      name: "Donkey",
      modelUrl: "https://mscharacters.s3.us-east-1.amazonaws.com/Donkey.glb",
      price: 10,
      type: "ANIMAL",
    },
    {
      id: "c2aebc34-d5b8-4411-908a-293e644c3c79",
      name: "Fox",
      modelUrl: "https://mscharacters.s3.us-east-1.amazonaws.com/Fox.glb",
      price: 12,
      type: "ANIMAL",
    }
  ],
  HUMAN: [
    {
      id: "58a998f1-a706-4870-b288-fe34b007846a",
      name: "Business Man",
      modelUrl: "https://mscharacters.s3.us-east-1.amazonaws.com/Business%20Man.glb",
      price: 20,
      type: "HUMAN",
    },
    {
      id: "829f34b4-a538-40d3-82bf-1f571d73bcdd",
      name: "Mech-Zorro",
      modelUrl: "https://mscharacters.s3.us-east-1.amazonaws.com/Mech-Zorro.glb",
      price: 25,
      type: "HUMAN",
    }
  ],
};


export const mockQuizSubmissionsList: Record<string, QuizSubmissionSummary[]> = {
  'q1': [ // Submissions for "Quiz de Bienvenida"
    { student_id: 'student1', student_name: 'Ana', student_last_name: 'García', points_obtained: 18, submission_date: '2025-06-15T10:00:00Z' },
    { student_id: 'student2', student_name: 'Luis', student_last_name: 'Martinez', points_obtained: 15, submission_date: '2025-06-15T11:00:00Z' },
    { student_id: '2', student_name: 'Alex', student_last_name: 'Student', points_obtained: 20, submission_date: '2025-06-15T09:30:00Z' },
  ],
  'q2': [ // Submissions for "Quiz Intermedio: Unidad 1"
    { student_id: 'student1', student_name: 'Ana', student_last_name: 'García', points_obtained: 22, submission_date: '2025-06-20T12:00:00Z' },
  ],
   'q3': [ 
    { student_id: 'student4', student_name: 'Carlos', student_last_name: 'Hernandez', points_obtained: 25, submission_date: '2025-07-01T10:00:00Z' },
  ],
};

export const mockStudentQuizAttemptsData: Record<string, StudentQuizAttempt> = {
  'q1_student1': { 
    id: 'attempt-q1-s1',
    title: "Quiz de Bienvenida",
    instruction: "Completa este quiz para empezar y familiarizarte con la plataforma...",
    start_time: "2025-06-15T09:00:00Z",
    end_time: "2025-06-16T23:59:00Z",
    created_at: "2025-06-15T10:00:00Z", 
    updated_at: "2025-06-15T10:00:00Z",
    feedback_automated: "Buen trabajo completando el quiz de bienvenida.",
    feedback_teacher: null,
    points_obtained: 18,
    quiz_id: 'q1',
    student_id: 'student1',
    questions: [
      {
        ...(mockClassroomDetailsData['c1'].quiz![0].questions![0] as QuestionAttempt), 
        id: 'q1-ques1',
        feedback_automated: "Respuesta parcialmente correcta.",
        feedback_teacher: null,
        points_obtained: 8,
        answer_submitted: { type: "submitted_text", answer_written: "Respuesta de Ana" },
      },
      {
        ...(mockClassroomDetailsData['c1'].quiz![0].questions![1] as QuestionAttempt), 
        id: 'q1-ques2',
        feedback_automated: "¡Correcto!",
        feedback_teacher: "Bien hecho en esta.",
        points_obtained: 10,
        answer_submitted: { type: "submitted_multiple_option", option_select: "Opción A" },
      }
    ]
  },
  'q1_2': { 
    id: 'attempt-q1-s2', 
    title: "Quiz de Bienvenida",
    instruction: "Completa este quiz para empezar y familiarizarte con la plataforma...",
    start_time: "2025-06-15T09:00:00Z",
    end_time: "2025-06-16T23:59:00Z",
    created_at: "2025-06-15T09:30:00Z", 
    updated_at: "2025-06-15T09:30:00Z",
    feedback_automated: "¡Excelente! Puntuación perfecta.",
    feedback_teacher: "Muy buen inicio, Alex.",
    points_obtained: 20,
    quiz_id: 'q1',
    student_id: '2',
    questions: [
      {
        ...(mockClassroomDetailsData['c1'].quiz![0].questions![0] as QuestionAttempt),
        id: 'q1-ques1',
        feedback_automated: "Correcto.",
        feedback_teacher: null,
        points_obtained: 10,
        answer_submitted: { type: "submitted_text", answer_written: "Respuesta correcta 1" },
      },
      {
        ...(mockClassroomDetailsData['c1'].quiz![0].questions![1] as QuestionAttempt),
        id: 'q1-ques2',
        feedback_automated: "¡Correcto!",
        feedback_teacher: null,
        points_obtained: 10,
        answer_submitted: { type: "submitted_multiple_option", option_select: "Opción A" },
      }
    ]
  },
};