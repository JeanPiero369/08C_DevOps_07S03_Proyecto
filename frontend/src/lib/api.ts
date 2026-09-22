
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
  quizStudentDetails,
} from '@/types/entities';

import {
    mockUsers,
    mockClassroomTeachers,
    mockClassroomStudents,
    mockTeacherClassrooms,
    mockStudentClassroomEnrollments,
    mockClassroomDetailsData,
    mockTeacherGeneralCompetencies,
    mockStudentCurrentCharacter,
    mockStoreCharacters,
    mockQuizSubmissionsList,
    mockStudentQuizAttemptsData,
} from '@/lib/mockData';

import axios from "axios";

// Usa variables de entorno de Next.js
// NEXT_PUBLIC_API_URL es accesible tanto en el cliente como en el servidor
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"; 

const api = axios.create({ baseURL: API_URL });

// Añade automatiamente el token en el header
api.interceptors.request.use((config) => {
  const token =
    localStorage.getItem("token") || sessionStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token);
  }
};

const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
};


// Bloque try-catch para copy paste

/*
try {
 
} catch (error) {
  console.error('Error al obtener datos:', error);
  // Este `catch` se activará para:
  // 1. Errores de red (como se mencionó antes).
  // 2. Errores lanzados explícitamente por `throw new Error()` dentro del `try`
  //    cuando `response.ok` es false (ej. 404, 500).
}

try {
  
  } catch (error) {
    console.error('Error al obtener datos:', error);
  }
  finally {
  }
*/
export const loginUser = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await api.post(`/auth/login`,credentials)
    setToken(response.data.token)
    console.log(response.data.token)
    return {
      success: true,
      message: 'Login successful',
      token: response.data.token,
      //user: foundUser,
    };
 
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return {
      success: false,
      message: 'Invalid email or password',
    };
  }
};

export const registerUser = async (payload: RegisterPayload): Promise<AuthResponse> => {
  if (!payload.email || !payload.password || !payload.name || !payload.last_name || !payload.role) {
    return {
      success: false,
      message: 'All fields are required',
    };
  }
  try {
    //console.log(payload)
    const response = await api.post(`/auth/register`,payload)
    return {
      success: true,
      message: 'Registration successful. Please log in.',
      //user: newUser,
    };
  } catch (error) {
    if (axios.isAxiosError(error) && error.response.status===409) {
       return { success: false, message: "Ya existe un usuario con este correo electrónico." };
    }
    console.error('Error al obtener datos:', error);
    // Este `catch` se activará para:
    // 1. Errores de red (como se mencionó antes).
    // 2. Errores lanzados explícitamente por `throw new Error()` dentro del `try`
    //    cuando `response.ok` es false (ej. 404, 500).
  }
};

export const logoutUser = (): void => {
  removeToken();
};

export const fetchUserProfile = async (): Promise<User | null> => {
  const token = getToken();
  if (!token) {
    return null;
  }
  try {
    const data = await api.get(`/teacher/me`).then((res) => res.data).catch((error) => {})
    if(data){
      return data;
    }
    const data2 = await api.get(`/student/me`).then((res) => res.data)
    if(data2){
            console.log(data2)

      return data2;
    }
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return null;
  }
};

export const updateUserProfile = async (userId: string, data: Partial<Pick<User, 'name' | 'last_name' | 'cel_phone'>>): Promise<User | null> => {
  await new Promise(resolve => setTimeout(resolve, 500));
  if (mockUsers[userId]) {
    mockUsers[userId] = { ...mockUsers[userId], ...data };
    return { ...mockUsers[userId] };
  }
  return null;
};

export const fetchTeacherClassrooms = async (userId: string): Promise<Omit<Classroom, 'quiz' | 'competences'>[]> => {
  try{
    return await api.get(`classroom/user/${userId}`).then((res) => res.data)
    //return classrooms.map(c => ({...c})); 
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return []
  }
};

export const createTeacherClassroom = async (userId: string, classroomData: { name: string; description: string }): Promise<Omit<Classroom, 'quiz' | 'competences'>> => {
  try {
    const data = await api.post(`teacher/${userId}/classroom`,classroomData).then((res) => res.data)
    return data;
  } catch (error) {
    console.error('Error al obtener datos:', error);
  }
};

export const updateTeacherClassroom = async (classroomId: string, classroomData: { name: string; description: string }): Promise<Omit<Classroom, 'quiz' | 'competences'>> => {
  await new Promise(resolve => setTimeout(resolve, 500));

  if (mockClassroomDetailsData[classroomId]) {
    mockClassroomDetailsData[classroomId] = {
      ...mockClassroomDetailsData[classroomId],
      name: classroomData.name,
      description: classroomData.description,
    };
  } else {
    throw new Error("Classroom not found in details data for update.");
  }

  let updatedClassroomSummary: Omit<Classroom, 'quiz' | 'competences'> | null = null;
  for (const teacherId in mockTeacherClassrooms) {
    const classroomIndex = mockTeacherClassrooms[teacherId].findIndex(c => c.id === classroomId);
    if (classroomIndex !== -1) {
      mockTeacherClassrooms[teacherId][classroomIndex] = {
        ...mockTeacherClassrooms[teacherId][classroomIndex],
        name: classroomData.name,
        description: classroomData.description,
      };
      updatedClassroomSummary = { ...mockTeacherClassrooms[teacherId][classroomIndex] };
      break;
    }
  }

  if (updatedClassroomSummary) {
    return updatedClassroomSummary;
  } else {
    throw new Error("Classroom not found in any teacher's list for update.");
  }
};


export const fetchTeacherCompetencies = async (userId: string): Promise<Competency[]> => {
  try {
    return  await api.get(`teacher/${userId}/competences`).then((res) => res.data)
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return []
  }
};

export const createTeacherCompetency = async (userId: string, competencyData: Omit<Competency, 'id'>): Promise<Competency> => {
  try {
    const data = await api.post(`teacher/${userId}/competences`,competencyData).then((res) => res.data)
    return data;
  } catch (error) {
    console.error('Error al obtener datos:', error);
  }
};

export const updateTeacherCompetency = async (competencyId: string, competencyData: { name: string; description: string }): Promise<Competency> => {
  await new Promise(resolve => setTimeout(resolve, 500));
  let updatedCompetency: Competency | null = null;

  for (const userId in mockTeacherGeneralCompetencies) {
    const competencyIndex = mockTeacherGeneralCompetencies[userId].findIndex(c => c.id === competencyId);
    if (competencyIndex !== -1) {
      mockTeacherGeneralCompetencies[userId][competencyIndex] = {
        ...mockTeacherGeneralCompetencies[userId][competencyIndex],
        name: competencyData.name,
        description: competencyData.description,
      };
      updatedCompetency = { ...mockTeacherGeneralCompetencies[userId][competencyIndex] };
      for (const classroomId_ in mockClassroomDetailsData) {
        const classroom = mockClassroomDetailsData[classroomId_];
        if (classroom.competences) {
            const classCompIndex = classroom.competences.findIndex(c => c.id === competencyId);
            if (classCompIndex !== -1) {
                classroom.competences[classCompIndex] = {
                    ...classroom.competences[classCompIndex],
                    name: competencyData.name,
                    description: competencyData.description,
                };
            }
        }
      }
      break;
    }
  }

  if (updatedCompetency) {
    return updatedCompetency;
  } else {
    throw new Error("Competency not found for update.");
  }
};


export const fetchClassroomDetails = async (classroomId: string, studentId?: string, studentRole?: UserRole): Promise<Classroom | null> => {
  try {
    const data = await api.get(`classroom/${classroomId}`).then((res) => res.data)
    return data;
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return null;
  }
};

export const updateClassroomCompetencies = async (classroomId: string, competenceIds: string[]): Promise<Classroom | null> => {
  const payload={ competences_id: competenceIds}
  try{
    return await api.post(`teacher/classroom/${classroomId}/competences-associate`,payload).then((res) => res.data)
  }catch(e){
    console.error('Error al obtener datos:', e);
    return null
  }
};


export const fetchClassroomCompetenciesForQuiz = async (classroomId: number): Promise<Competency[]> => {
  try {
    const data=await api.get(`classroom/${classroomId}/competences`).then((res) => res.data)
    const transformedData = data.map(comp => {
    const { id_competence, ...rest } = comp;
    return {id: id_competence,...rest};});
    return transformedData
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return []
  }
};

export const fetchStudentClassrooms = async (studentId: string): Promise<Omit<Classroom, 'quiz' | 'competences'>[]> => {
  try{
    return await api.get(`classroom/user/${studentId}`).then((res) => res.data)
    //return classrooms.map(c => ({...c})); 
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return []
  }
};

export const fetchStudentListQuiz = async (classroomId: string,studentId: string): Promise<quizStudentDetails[]> => {
  try{
    return await api.get(`student/classroom/${classroomId}/student/${studentId}/quiz-list`).then((res) => res.data)
    //return classrooms.map(c => ({...c})); 
  } catch (error) {
    console.error('Error al obtener datos:', error);
    return []
  }
};


export const createQuiz = async (payload: NewQuizPayload,classroom_id: number): Promise<Quiz> => {
  const res = await api.post(`teacher/classroom/${classroom_id}/quiz/create`,payload);
  return res.data;
};

export const generateQuizFromDocument = async (payload: GenerateQuizFromDocumentPayload, file: File): Promise<Partial<Quiz>> => {  
  const formData = new FormData();
  //console.log(payload)
  //console.log(JSON.stringify(payload))
  formData.append("input_data_json", JSON.stringify(payload));
  formData.append("pdf_file", file);

  const data= api.post("/teacher/quiz/generate-from-pdf", formData, {headers: { "Content-Type": "multipart/form-data" },}).then((res) => res.data);
  console.log(data)
  return data;
};

export const generateQuizFromText = async (payload: GenerateQuizFromTextPayload): Promise<Partial<Quiz>> => {
  if (typeof payload.classroom_id === 'string') {
    payload.classroom_id = parseInt(payload.classroom_id, 10);
  }
  const payloadToSend = { ...payload }; // Copia superficial
  if (payloadToSend.type_question && 'criticas' in payloadToSend.type_question) {
      // Guarda el valor, elimina la clave incorrecta y añade la clave correcta
      const value = payloadToSend.type_question.criticas;
      delete payloadToSend.type_question.criticas;
      payloadToSend.type_question.críticas = value; // Añade la clave con tilde
  }
  console.log("API: Generating quiz from text:", payload);
  return api.post("/teacher/quiz/generate-from-text", payload).then((res) => res.data);

};


const allStudentResults: StudentResult[] = [
  { ranking: 1, obtained_points: 95, student: mockUsers['student1'] as User },
  { ranking: 2, obtained_points: 88, student: mockUsers['student2'] as User },
  { ranking: 3, obtained_points: 85, student: mockUsers['student3'] as User },
  { ranking: 4, obtained_points: 72, student: mockUsers['student4'] as User },
  { ranking: 5, obtained_points: 60, student: mockUsers['student5'] as User },
];

export const fetchGeneralResults = async (classroomId: string): Promise<StudentResult[]> => {
  console.log(`API: Fetching general results for classroom ${classroomId}`);
  try{
    return await api.get(`classroom/${classroomId}/ranking`).then((res) => res.data)
  }catch(e){
    return [];
  }
};

export const fetchCompetencyResults = async (classroomId: string, competencyId: string): Promise<StudentResult[]> => {
  console.log(`API: Fetching results for classroom ${classroomId}, competency ${competencyId}`);
  try{
    return await api.get(`classroom/${classroomId}/competence/${competencyId}/ranking`).then((res) => res.data)
  }catch(e){
    return [];
  }
};

export const fetchClassroomTeachers = async (classroomId: string): Promise<User[]> => {
  try{
    return await api.get(`classroom/${classroomId}/teacher`).then((res) => res.data)
    
  } catch(e){
    console.log(`API: Fetching teachers for classroom ${classroomId}`);
    return []
  }
};

export const fetchClassroomStudents = async (classroomId: string): Promise<User[]> => {
  try{
    return await api.get(`classroom/${classroomId}/student`).then((res) => res.data)
  } catch(e){
    console.log(`API: Fetching teachers for classroom ${classroomId}`);
    return []
  }
};

export const addPeopleToClassroom = async (classroomId: string, emails: string[], role: UserRole): Promise<AddPeopleResponse> => {
  const added: User[] = [];
  const failed: { email: string; reason: string }[] = [];
  const payload={ emails: emails}
  try{
    if (emails.length <=0){
      return { success: false, message: 'No se proporcionaron correos para agregar.', added, failed };
    }
    await api.post(`/teacher/classroom/${classroomId}/add-users`,payload).then((res) => res.data)
    return { success: true, message: 'Personas agregadas exitosamente.', added, failed };
  }catch(e){
    console.error('Error al obtener datos:', e);
    return { success: false, message: 'No se pudieron agregar las personas.', added, failed };
  }
};


//------------------------------------------
export const fetchStudentCurrentCharacter = async (studentId: string): Promise<Character | null> => {
  await new Promise(resolve => setTimeout(resolve, 300));
  return mockStudentCurrentCharacter[studentId] ? { ...mockStudentCurrentCharacter[studentId] } : (mockStudentCurrentCharacter['2'] ? {...mockStudentCurrentCharacter['2']} : null); // Default to Alex Student if specific not found
};

export const fetchStoreCharacters = async (): Promise<StoreCharacterData> => {
  await new Promise(resolve => setTimeout(resolve, 500));
  const copiedStore: StoreCharacterData = {};
  for (const type in mockStoreCharacters) {
    copiedStore[type as keyof StoreCharacterData] = mockStoreCharacters[type as keyof StoreCharacterData]!.map(char => ({ ...char }));
  }
  return copiedStore;
};

export const purchaseCharacter = async (studentId: string, characterId: string, price: number): Promise<{ success: boolean; message: string; updatedUser?: User }> => {
  await new Promise(resolve => setTimeout(resolve, 700));
  const student = mockUsers[studentId];
  if (!student || student.role !== 'STUDENT') {
    return { success: false, message: "Estudiante no encontrado." };
  }

  if ((student.coin_available || 0) < price) {
    return { success: false, message: "Monedas insuficientes." };
  }

  let characterToPurchase: Character | null = null;
  for (const type in mockStoreCharacters) {
    const found = mockStoreCharacters[type as keyof StoreCharacterData]!.find(char => char.id === characterId);
    if (found) {
      characterToPurchase = found;
      break;
    }
  }

  if (!characterToPurchase) {
    return { success: false, message: "Personaje no encontrado en la tienda." };
  }

  student.coin_available = (student.coin_available || 0) - price;
  mockStudentCurrentCharacter[studentId] = { ...characterToPurchase }; // Update student's current character
  mockUsers[studentId] = { ...student }; // Save updated student info (coins)


  return { success: true, message: `¡Has comprado ${characterToPurchase.name}!`, updatedUser: { ...student } };
};

export const fetchQuizSubmissions = async (quizId: string): Promise<QuizSubmissionSummary[]> => {
  try{
    return await api.get(`quiz/${quizId}/results`).then((res) => res.data)
  } catch(e){
    console.log(`API: Fetching quiz for classroom ${quizId}`);
    return []
  }
};

export const fetchStudentQuizAttemptDetails = async (quizId: string, studentId: string): Promise<StudentQuizAttempt | null> => {
  console.log(`API: Fetching attempt details for quiz ${quizId}, student ${studentId}`);
  try{
    const data =await api.get(`quiz/${quizId}/student/${studentId}/result`).then((res) => res.data)
    console.log(data);
    return data;
  } catch(e){
    console.log(`Error ${e}`);
    return null
  }
};

export const saveTeacherFeedback = async (payload: SaveFeedbackPayload): Promise<{ success: boolean; message: string }> => {
  console.log("API: Saving teacher feedback:", payload);
  await new Promise(resolve => setTimeout(resolve, 700));

  const attemptKey = `${payload.quiz_id}_${payload.student_id}`;
  const attempt = mockStudentQuizAttemptsData[attemptKey];

  if (!attempt) {
    return { success: false, message: "No se encontró la entrega del estudiante." };
  }

  attempt.feedback_teacher = payload.general_feedback;
  attempt.updated_at = new Date().toISOString();

  payload.question_feedbacks.forEach(qf => {
    const questionAttempt = attempt.questions.find(q => q.id === qf.question_id);
    if (questionAttempt) {
      questionAttempt.feedback_teacher = qf.feedback_text;
    }
  });
  
  mockStudentQuizAttemptsData[attemptKey] = attempt;

  return { success: true, message: "Retroalimentación guardada exitosamente." };
};

export const fetchQuizForTaking = async (quizId: string): Promise<QuizForTaking | null> => {
  console.log(`API: Fetching quiz for taking: ${quizId}`);
    try{
    return await api.get(`quiz/${quizId}`).then((res) => res.data)
  } catch(e){
    console.log(`Error ${e}`);
    return null
  }
};

export const submitStudentQuizAttempt = async (classroomId:number,payload: StudentQuizSubmissionPayload): Promise<{ success: boolean; message: string; points_obtained?: number }> => {
  console.log("API: Submitting student quiz attempt:", JSON.stringify(payload, null, 2));
  
  try{
    console.log(payload)
    console.log(classroomId)
   await api.post(`/student/classroom/${classroomId}/quiz-submit`,payload).then((res) => res.data)
   return { success: true, message: "Quiz enviado exitosamente.", points_obtained: undefined };
  } catch(e){
    console.log(`Error ${e}`);
    return { success: false, message: "No se pudo envia el Quiz" };
  }

};
