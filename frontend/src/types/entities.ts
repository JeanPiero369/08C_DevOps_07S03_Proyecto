import { z } from 'zod';

// --- Esquemas de Tipos Base ---

const CompetencySchema = z.object({
  id_competence: z.number(),
  name: z.string(),
  description: z.string(),
});

const ClassroomSchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string(),
  quiz: z.array(z.lazy(() => QuizSchema)).optional(),
  competences: z.array(CompetencySchema).optional(),
});

const AnswerBaseSchema = z.object({
  id_answer: z.number().optional(),
  type: z.union([z.literal("base_text"), z.literal("base_multiple_option")]),
  options: z.array(z.string()).optional(),
});

const QuestionSchema = z.object({
  id: z.number().optional(),
  statement: z.string(),
  answer_correct: z.string(),
  points: z.number(),
  answer_base: AnswerBaseSchema,
  competences_id: z.array(z.number()),
});

const QuizSchema = z.object({
  id: z.number(),
  title: z.string(),
  instruction: z.string(),
  total_points: z.number().optional(),
  start_time: z.string().optional(),
  end_time: z.string().optional(),
  created_at: z.string().optional(),
  updated_at: z.string().optional(),
  questions: z.array(QuestionSchema).optional(),
  classroom_id: z.number().optional(),
});


const TypeQuestionSchema = z.object({
  textuales: z.boolean(),
  inferenciales: z.boolean(),
  críticas: z.boolean(),
});

// --- Esquemas para Payloads de Entrada ---

const GenerateQuizFromDocumentPayloadSchema = z.object({
  classroom_id: z.number(),
  num_question: z.string().transform(val => parseInt(val, 10)).pipe(z.number()),
  point_max: z.string().transform(val => parseInt(val, 10)).pipe(z.number()),
  competences: z.array(CompetencySchema),
  type_question: TypeQuestionSchema,
});

const GenerateQuizFromTextPayloadSchema = z.object({
  classroom_id: z.number(),
  num_question: z.string().transform(val => parseInt(val, 10)).pipe(z.number()),
  point_max: z.string().transform(val => parseInt(val, 10)).pipe(z.number()),
  text: z.string(),
  competences: z.array(CompetencySchema),
  type_question: TypeQuestionSchema,
});

export const NewQuizPayloadSchema = z.object({
  classroom_id: z.number(),
  title: z.string(),
  instruction: z.string(),
  start_time: z.string(), // Asumo formato ISO string (ej. "2023-10-27T10:00:00Z")
  end_time: z.string(),   // Asumo formato ISO string (ej. "2023-10-27T11:00:00Z")
  questions: z.array(QuestionSchema),
});

// --- Esquemas para Resultados y Envíos ---

const StudentSchema = z.object({
  id: z.number(),
  name: z.string(),
  last_name: z.string(),
  email: z.string().email(),
  cel_phone: z.string().nullable(),
  role: z.literal('STUDENT'),
  emotion: z.string().nullable().optional(),
  coin_earned: z.number().optional(),
  coin_available: z.number().optional(),
});

const StudentResultSchema = z.object({
  ranking: z.number(),
  obtained_points: z.number(),
  student: StudentSchema,
});

const QuizSubmissionSummarySchema = z.object({
  id: z.number(),
  name: z.string(),
  last_name: z.string(),
  points_obtained: z.number(),
  submission_date: z.string().optional(),
});

const SubmittedAnswerSchema = z.object({
  id: z.number().optional(),
  type: z.union([z.literal("submitted_text"), z.literal("submitted_multiple_option")]),
  answer_written: z.string().optional(),
  option_select: z.string().optional(),
});

const QuestionAttemptSchema = QuestionSchema.extend({
  feedback_automated: z.string().nullable(),
  feedback_teacher: z.string().nullable(),
  points_obtained: z.number(),
  answer_submitted: SubmittedAnswerSchema,
});

const StudentQuizAttemptSchema = z.object({
  id: z.number(),
  title: z.string(),
  instruction: z.string(),
  start_time: z.string(),
  end_time: z.string(),
  created_at: z.string(),
  updated_at: z.string(),
  feedback_automated: z.string().nullable(),
  feedback_teacher: z.string().nullable(),
  points_obtained: z.number(),
  questions: z.array(QuestionAttemptSchema),
  student_id: z.number().optional(),
  quiz_id: z.number().optional(),
});

const SaveFeedbackPayloadSchema = z.object({
    quiz_id: z.number(),
    student_id: z.number(),
    general_feedback: z.string().nullable(),
    question_feedbacks: z.array(z.object({
        question_id: z.number(),
        feedback_text: z.string().nullable(),
    })),
});

// --- Esquemas para la Tienda (Store) ---

const CharacterTypeSchema = z.union([
  z.literal("ANIMAL"),
  z.literal("HUMAN"),
  z.literal("OTHER"),
  z.literal("FANTASY"),
  z.literal("ROBOT"),
]);

const CharacterSchema = z.object({
  id: z.number(),
  name: z.string(),
  modelUrl: z.string().url(),
  price: z.number().positive(),
  type: CharacterTypeSchema,
});

const StoreCharacterDataSchema = z.record(CharacterTypeSchema, z.array(CharacterSchema)).optional();

export interface quizStudentDetails {
  id: number;
  title: string;
  instruction: string;
  total_points: number;
  start_time: string; // 
  end_time: string;   // 
  created_at: string; // 
  updated_at: string; // 
  student_has_attemped: boolean;
}
// --- Exporta los Tipos Inferidos de TypeScript ---

export type Classroom = z.infer<typeof ClassroomSchema>;
export type Competency = z.infer<typeof CompetencySchema>;
export type AnswerBase = z.infer<typeof AnswerBaseSchema>;
export type Question = z.infer<typeof QuestionSchema>;
export type Quiz = z.infer<typeof QuizSchema>;
export type NewQuizPayload = z.infer<typeof NewQuizPayloadSchema>;
export type TypeQuestion = z.infer<typeof TypeQuestionSchema>;
export type GenerateQuizFromDocumentPayload = z.infer<typeof GenerateQuizFromDocumentPayloadSchema>;
export type GenerateQuizFromTextPayload = z.infer<typeof GenerateQuizFromTextPayloadSchema>;
export type Student = z.infer<typeof StudentSchema>;
export type StudentResult = z.infer<typeof StudentResultSchema>;
export type QuizSubmissionSummary = z.infer<typeof QuizSubmissionSummarySchema>;
export type SubmittedAnswer = z.infer<typeof SubmittedAnswerSchema>;
export type QuestionAttempt = z.infer<typeof QuestionAttemptSchema>;
export type StudentQuizAttempt = z.infer<typeof StudentQuizAttemptSchema>;
export type SaveFeedbackPayload = z.infer<typeof SaveFeedbackPayloadSchema>;
export type CharacterType = z.infer<typeof CharacterTypeSchema>;
export type Character = z.infer<typeof CharacterSchema>;
export type StoreCharacterData = z.infer<typeof StoreCharacterDataSchema>;